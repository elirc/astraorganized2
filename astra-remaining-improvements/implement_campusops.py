from pathlib import Path
B=Path(__file__).resolve().parent
S=B/'stage'/'8228fda84db1'
def put(path,text):
 p=S/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
put('src/CampusOps.Core/Inventory/Part.cs',r'''
using CampusOps.Core.Common;
using CampusOps.Core.WorkOrders;

namespace CampusOps.Core.Inventory;

public sealed class Part
{
    public Part(Guid id, string sku, string name, int onHand)
    {
        if (id == Guid.Empty || string.IsNullOrWhiteSpace(sku) || string.IsNullOrWhiteSpace(name))
            throw new DomainException("part.details_required", "Part ID, SKU, and name are required.");
        if (onHand < 0) throw new DomainException("part.quantity_invalid", "Quantity cannot be negative.");
        Id = id;
        Sku = sku.Trim().ToUpperInvariant();
        Name = name.Trim();
        OnHand = onHand;
    }

    public Guid Id { get; }
    public string Sku { get; }
    public string Name { get; }
    public int OnHand { get; private set; }
    public int Reserved { get; private set; }
    public int Available => OnHand - Reserved;

    public void Receive(int quantity)
    {
        Positive(quantity);
        if (quantity > int.MaxValue - OnHand)
            throw new DomainException("part.quantity_overflow", "Received quantity exceeds supported stock capacity.");
        OnHand += quantity;
    }

    public void Reserve(int quantity)
    {
        Positive(quantity);
        if (quantity > Available) throw new DomainException("part.stock_insufficient", "Not enough available stock.");
        Reserved += quantity;
    }

    public void Release(int quantity)
    {
        Positive(quantity);
        if (quantity > Reserved) throw new DomainException("part.release_invalid", "Cannot release more than reserved.");
        Reserved -= quantity;
    }

    public void Consume(int quantity)
    {
        Positive(quantity);
        if (quantity > Reserved) throw new DomainException("part.consume_invalid", "Parts must be reserved before consumption.");
        Reserved -= quantity;
        OnHand -= quantity;
    }

    // All fields are values or immutable strings; callers receive detached state.
    public Part Snapshot() => (Part)MemberwiseClone();

    private static void Positive(int quantity)
    {
        if (quantity <= 0) throw new DomainException("part.quantity_invalid", "Quantity must be positive.");
    }
}

public sealed record PartReservation(Guid Id, Guid WorkOrderId, Guid PartId, int Quantity, DateTimeOffset ReservedAt);

public interface IPartStore
{
    Task AddAsync(Part part, CancellationToken token);
    Task<Part?> GetAsync(Guid id, CancellationToken token);
    Task<IReadOnlyCollection<Part>> ListAsync(CancellationToken token);
    // Stock and the reservation record are one commit, or neither is changed.
    Task<PartReservation?> ReserveForWorkOrderAsync(Guid workOrderId, Guid partId, int quantity, DateTimeOffset at, CancellationToken token);
}

public interface IPartReservationStore
{
    Task<IReadOnlyCollection<PartReservation>> ListForWorkOrderAsync(Guid id, CancellationToken token);
}

public sealed class PartsService(IPartStore parts, IWorkOrderStore workOrders, IClock clock)
{
    public async Task<PartReservation> ReserveAsync(Guid workOrderId, Guid partId, int quantity, CancellationToken token)
    {
        token.ThrowIfCancellationRequested();
        if (workOrderId == Guid.Empty || partId == Guid.Empty)
            throw new DomainException("part.reservation_identity_required", "Work order and part IDs are required.");
        if (quantity <= 0) throw new DomainException("part.quantity_invalid", "Quantity must be positive.");
        if (await workOrders.GetAsync(workOrderId, token) is null)
            throw new DomainException("work_order.not_found", "Work order was not found.");
        return await parts.ReserveForWorkOrderAsync(workOrderId, partId, quantity, clock.UtcNow, token)
            ?? throw new DomainException("part.stock_insufficient", "Part was not found or stock is insufficient.");
    }
}
''')
put('src/CampusOps.Infrastructure/Inventory/InMemoryPartsStores.cs',r'''
using CampusOps.Core.Common;
using CampusOps.Core.Inventory;

namespace CampusOps.Infrastructure.Inventory;

// Both interfaces must resolve to this SAME singleton instance (see Program.cs).
public sealed class InMemoryPartStore : IPartStore, IPartReservationStore
{
    private readonly object _gate = new();
    private readonly Dictionary<Guid, Part> _parts = new();
    private readonly Dictionary<Guid, PartReservation> _reservations = new();

    public Task AddAsync(Part part, CancellationToken token)
    {
        lock (_gate)
        {
            token.ThrowIfCancellationRequested();
            if (!_parts.TryAdd(part.Id, part.Snapshot()))
                throw new DomainException("part.already_exists", "A part with this ID already exists.");
        }
        return Task.CompletedTask;
    }

    public Task<Part?> GetAsync(Guid id, CancellationToken token)
    {
        lock (_gate)
        {
            token.ThrowIfCancellationRequested();
            return Task.FromResult(_parts.TryGetValue(id, out var part) ? part.Snapshot() : null);
        }
    }

    public Task<IReadOnlyCollection<Part>> ListAsync(CancellationToken token)
    {
        lock (_gate)
        {
            token.ThrowIfCancellationRequested();
            return Task.FromResult<IReadOnlyCollection<Part>>(_parts.Values.OrderBy(x => x.Sku).Select(x => x.Snapshot()).ToArray());
        }
    }

    public Task<PartReservation?> ReserveForWorkOrderAsync(Guid workOrderId, Guid partId, int quantity, DateTimeOffset at, CancellationToken token)
    {
        lock (_gate)
        {
            // Cancellation is honored before commit, never reported after mutation.
            token.ThrowIfCancellationRequested();
            if (workOrderId == Guid.Empty || partId == Guid.Empty)
                throw new DomainException("part.reservation_identity_required", "Work order and part IDs are required.");
            if (quantity <= 0) throw new DomainException("part.quantity_invalid", "Quantity must be positive.");
            if (!_parts.TryGetValue(partId, out var current) || quantity > current.Available)
                return Task.FromResult<PartReservation?>(null);

            var updated = current.Snapshot();
            updated.Reserve(quantity);
            var reservation = new PartReservation(Guid.NewGuid(), workOrderId, partId, quantity, at.ToUniversalTime());
            // Prepare and validate first. No await, callback or external store between writes.
            _reservations.Add(reservation.Id, reservation);
            _parts[partId] = updated;
            return Task.FromResult<PartReservation?>(reservation);
        }
    }

    public Task<IReadOnlyCollection<PartReservation>> ListForWorkOrderAsync(Guid id, CancellationToken token)
    {
        lock (_gate)
        {
            token.ThrowIfCancellationRequested();
            return Task.FromResult<IReadOnlyCollection<PartReservation>>(_reservations.Values
                .Where(x => x.WorkOrderId == id).OrderBy(x => x.ReservedAt).ThenBy(x => x.Id).ToArray());
        }
    }
}
''')
p=S/'src/CampusOps.Api/Program.cs';t=p.read_text(encoding='utf-8');t=t.replace('builder.Services.AddSingleton<IPartStore, InMemoryPartStore>();\nbuilder.Services.AddSingleton<IPartReservationStore, InMemoryPartReservationStore>();','builder.Services.AddSingleton<InMemoryPartStore>();\nbuilder.Services.AddSingleton<IPartStore>(provider => provider.GetRequiredService<InMemoryPartStore>());\nbuilder.Services.AddSingleton<IPartReservationStore>(provider => provider.GetRequiredService<InMemoryPartStore>());');p.write_text(t,encoding='utf-8')
put('src/CampusOps.Api/Inventory/PartEndpoints.cs',r'''
using CampusOps.Api.Security;
using CampusOps.Contracts.Inventory;
using CampusOps.Core.Inventory;

namespace CampusOps.Api.Inventory;

public static class PartEndpoints
{
    public static IEndpointRouteBuilder MapPartEndpoints(this IEndpointRouteBuilder endpoints)
    {
        var group = endpoints.MapGroup("/api/v1/parts").WithTags("Parts")
            .RequireAuthorization(SecurityPolicies.Operations);
        group.MapPost("/", async (CreatePartRequest body, IPartStore store, CancellationToken token) =>
        {
            var part = new Part(Guid.NewGuid(), body.Sku, body.Name, body.OnHand);
            await store.AddAsync(part, token);
            return Results.Created($"/api/v1/parts/{part.Id}", Map(part));
        });
        group.MapGet("/", async (IPartStore store, CancellationToken token) =>
            Results.Ok((await store.ListAsync(token)).Select(Map)));
        group.MapGet("/{id:guid}", async (Guid id, IPartStore store, CancellationToken token) =>
        {
            var part = await store.GetAsync(id, token);
            return part is null ? Results.NotFound() : Results.Ok(Map(part));
        });
        var workOrders = endpoints.MapGroup("/api/v1/work-orders/{id:guid}/parts")
            .WithTags("Work orders").RequireAuthorization(SecurityPolicies.Operations);
        workOrders.MapPost("/", async (Guid id, ReservePartRequest body, PartsService service, CancellationToken token) =>
            Results.Ok(await service.ReserveAsync(id, body.PartId, body.Quantity, token)));
        workOrders.MapGet("/", async (Guid id, IPartReservationStore store, CancellationToken token) =>
            Results.Ok(await store.ListForWorkOrderAsync(id, token)));
        return endpoints;
    }

    private static PartResponse Map(Part x) => new(x.Id, x.Sku, x.Name, x.OnHand, x.Reserved, x.Available);
}
''')
p=S/'web/CampusOps.Web/vite.config.ts';p.write_text(p.read_text(encoding='utf-8').replace('http://localhost:5000','http://localhost:5110'),encoding='utf-8')
print('CampusOps implementation staged')
