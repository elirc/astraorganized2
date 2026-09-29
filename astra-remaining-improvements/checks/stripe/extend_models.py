from pathlib import Path
root=Path(__file__).resolve().parents[2]/'stage/af19f6e32dba'
p=root/'src/Billing.Api/Domain/BillingModels.cs'
s=p.read_text(encoding='utf-8')
names=['Customer','Plan','Coupon','Subscription','UsageEvent','Invoice','Payment','PaymentJob','WebhookEvent']
for name in names:
    start=s.index('public sealed record '+name+'(')
    end=s.index(')',start)
    common='\n    public Guid WorkspaceId { get; init; }\n    public long Version { get; init; } = 1;\n'
    extra={'Customer':'    public bool IsArchived { get; init; }\n','Plan':'    public string Metric { get; init; } = "api_calls";\n','Coupon':'    public bool IsActive { get; init; } = true;\n','Subscription':'    public int AnchorDay { get; init; }\n    public bool CancelAtPeriodEnd { get; init; }\n','PaymentJob':'    public Guid PaymentId { get; init; }\n'}.get(name,'')
    if s[end+1]==';':s=s[:end+1]+' : IBillingEntity\n{'+common+extra+'}'+s[end+2:]
    else:
        brace=s.index('{',end)
        s=s[:end+1]+' : IBillingEntity'+s[end+1:brace+1]+common+extra+s[brace+1:]
p.write_text(s,encoding='utf-8')
p=root/'src/Billing.Api/Domain/Money.cs'
s=p.read_text(encoding='utf-8').replace('    public decimal MajorUnits','    [JsonIgnore]\n    public decimal MajorUnits')
p.write_text(s,encoding='utf-8')
print('Extended nine immutable entity records; Money JSON contains persisted fields only.')
