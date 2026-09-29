from pathlib import Path
B=Path(__file__).resolve().parent;P=B/'stage/14690be423dc'
def write(rel,text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
write('test/oms/RegressionTests.java',r'''package oms;
import oms.domain.*;
import oms.service.*;
import oms.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
public class RegressionTests {
    static int passed,failed;
    interface Check { void run() throws Exception; }
    static void test(String name,Check check) { try { check.run();passed++;System.out.println("PASS "+name); } catch(Throwable error) { failed++;System.out.println("FAIL "+name+": "+error); } }
    static void equal(Object expected,Object actual) { if(!expected.equals(actual)) throw new AssertionError("Expected "+expected+"; got "+actual); }
    static void rejects(Class<? extends Throwable> type,Check check) throws Exception { try { check.run(); } catch(Throwable error) { if(type.isInstance(error)) return;throw error; } throw new AssertionError("Expected "+type.getSimpleName()); }
    static BigDecimal money(String value) { return new BigDecimal(value); }
    static LocalDateTime time() { return LocalDateTime.of(2026,1,2,3,4); }
    static Customer customer() { return new Customer("C","Learner","learner@example.test","",time()); }
    static Product product() { return new Product("P","Notebook","NOTE",money("10"),true); }
    static Order order() { var order=new Order("O","C",time());order.addOrMergeItem(new OrderItem("P","Notebook",2,money("10")));return order; }
    static OrderService service(Order order) { return new OrderService(List.of(order),new CustomerService(List.of(customer())),new ProductService(List.of(product()))); }
    interface WithDirectory { void run(Path directory) throws Exception; }
    static void withDirectory(WithDirectory check) throws Exception {
        Path directory=Files.createTempDirectory("j7-regression-").toAbsolutePath().normalize();
        Path root=Path.of(System.getProperty("java.io.tmpdir")).toAbsolutePath().normalize();
        if(!directory.startsWith(root) || !directory.getFileName().toString().startsWith("j7-regression-")) throw new AssertionError("Unsafe temporary path");
        try {check.run(directory);} finally {try(var files=Files.walk(directory)){for(Path file:files.sorted(java.util.Comparator.reverseOrder()).toList())Files.delete(file);}}
    }
    public static void main(String[] args) throws Exception {
        test("saved discount survives full order reload",()->withDirectory(dir->{var order=order();order.setDiscountAmount(money("5"));var store=new FileDataStore(dir);store.save(new StoreSnapshot(List.of(customer()),List.of(product()),List.of(order)));var loaded=store.load().getOrders().get(0);equal(money("5.00"),loaded.getDiscountAmount());equal(money("15.00"),loaded.getTotal());}));
        test("read order cannot mutate service state",()->{var s=service(order());s.findById("O").orElseThrow().setDiscountAmount(money("5"));equal(money("20.00"),s.findById("O").orElseThrow().getTotal());});
        test("item getter cannot invalidate aggregate totals",()->{var order=order();order.getItems().get(0).setQuantity(9);equal(2,order.getItems().get(0).getQuantity());equal(money("20.00"),order.getSubtotal());});
        test("paid order cannot be edited",()->{var s=service(order());s.updateStatus("O",OrderStatus.SUBMITTED);s.updateStatus("O",OrderStatus.PAID);rejects(IllegalArgumentException.class,()->s.addProductToOrder("O","P",1));equal(money("20.00"),s.findById("O").orElseThrow().getTotal());});
        test("sub-cent product price is rejected",()->rejects(IllegalArgumentException.class,()->new Product("P","x","x",money("0.001"),true)));
        test("clearing service all collection cannot delete records",()->{var s=new ProductService(List.of(product()));try{s.all().clear();}catch(UnsupportedOperationException expected){}equal(1,s.listProducts().size());});
        test("carriage returns round trip through field codec",()->equal("a\rb",DelimitedFileUtil.split(DelimitedFileUtil.join("a\rb")).get(0)));
        System.out.println("RESULT passed="+passed+" failed="+failed);
        if(failed!=0) System.exit(1);
    }
}
''')
write('src/oms/domain/DomainValues.java',r'''package oms.domain;
import java.math.BigDecimal;
import java.math.RoundingMode;
public final class DomainValues {
    private DomainValues() { }
    public static String text(String value, String field) {
        if (value == null || value.trim().isEmpty()) throw new IllegalArgumentException(field + " is required.");
        return value.trim();
    }
    public static BigDecimal money(BigDecimal value, boolean allowZero) {
        if (value == null) throw new IllegalArgumentException("Money value is required.");
        BigDecimal normalized;
        try { normalized = value.setScale(2, RoundingMode.UNNECESSARY); }
        catch (ArithmeticException error) { throw new IllegalArgumentException("Money must use at most 2 decimal places.", error); }
        if (normalized.signum() < 0 || (!allowZero && normalized.signum() == 0))
            throw new IllegalArgumentException(allowZero ? "Money cannot be negative." : "Money must be greater than zero.");
        return normalized;
    }
}
''')
write('src/oms/domain/Order.java',r'''package oms.domain;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;

/** Owns its item values; every accepted mutation preserves totals and status rules. */
public class Order {
    private final String id;
    private final String customerId;
    private final List<OrderItem> items = new ArrayList<>();
    private OrderStatus status;
    private BigDecimal discountAmount;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Order(String id, String customerId, LocalDateTime createdAt) {
        this(id, customerId, OrderStatus.DRAFT, BigDecimal.ZERO, createdAt, createdAt, List.of());
    }

    private Order(String id, String customerId, OrderStatus status, BigDecimal discount,
                  LocalDateTime createdAt, LocalDateTime updatedAt, Collection<OrderItem> restoredItems) {
        this.id = DomainValues.text(id, "Order id");
        this.customerId = DomainValues.text(customerId, "Customer id");
        this.status = Objects.requireNonNull(status, "Status is required.");
        this.createdAt = Objects.requireNonNull(createdAt, "Created time is required.");
        this.updatedAt = Objects.requireNonNull(updatedAt, "Updated time is required.");
        var productIds = new HashSet<String>();
        for (OrderItem item : restoredItems) {
            if (!productIds.add(item.getProductId())) throw new IllegalArgumentException("Duplicate product in order.");
            items.add(item.copy());
        }
        this.discountAmount = DomainValues.money(discount, true);
        validateSubtotal(getSubtotal());
        if (requiresItems(status) && items.isEmpty()) throw new IllegalArgumentException("This order status requires items.");
    }

    public static Order restore(String id, String customerId, OrderStatus status, BigDecimal discount,
                                LocalDateTime createdAt, LocalDateTime updatedAt, Collection<OrderItem> items) {
        // Restore the complete aggregate once, then validate the saved discount.
        return new Order(id, customerId, status, discount, createdAt, updatedAt, items);
    }

    public Order copy() {
        return restore(id, customerId, status, discountAmount, createdAt, updatedAt, items);
    }

    public void addOrMergeItem(OrderItem newItem) {
        ensureEditable();
        Objects.requireNonNull(newItem, "Item is required.");
        for (OrderItem item : items) {
            if (item.getProductId().equals(newItem.getProductId())) {
                // Existing line keeps its original price and name snapshot.
                item.increaseQuantity(newItem.getQuantity());
                touch();
                return;
            }
        }
        items.add(newItem.copy());
        touch();
    }

    public void setItemQuantity(String productId, int quantity) {
        ensureEditable();
        for (int index = 0; index < items.size(); index++) {
            OrderItem current = items.get(index);
            if (current.getProductId().equals(productId)) {
                OrderItem candidate = new OrderItem(productId, current.getProductName(), quantity, current.getUnitPrice());
                validateSubtotal(getSubtotal().subtract(current.getLineTotal()).add(candidate.getLineTotal()));
                items.set(index, candidate);
                touch();
                return;
            }
        }
        throw new IllegalArgumentException("Product was not found in the order.");
    }

    public boolean removeItemByProductId(String productId) {
        ensureEditable();
        for (int index = 0; index < items.size(); index++) {
            OrderItem item = items.get(index);
            if (item.getProductId().equals(productId)) {
                if (status == OrderStatus.SUBMITTED && items.size() == 1)
                    throw new IllegalArgumentException("A submitted order must keep at least one item.");
                validateSubtotal(getSubtotal().subtract(item.getLineTotal()));
                items.remove(index);
                touch();
                return true;
            }
        }
        return false;
    }

    public void setDiscountAmount(BigDecimal discount) {
        ensureEditable();
        BigDecimal candidate = DomainValues.money(discount, true);
        if (candidate.compareTo(getSubtotal()) > 0) throw new IllegalArgumentException("Discount cannot exceed subtotal.");
        discountAmount = candidate;
        touch();
    }

    public void setStatus(OrderStatus target) {
        if (target == null || !status.canTransitionTo(target)) throw new IllegalArgumentException("Invalid order status transition.");
        if (requiresItems(target) && !hasItems()) throw new IllegalArgumentException("An empty order cannot enter that status.");
        status = target;
        touch();
    }

    private boolean requiresItems(OrderStatus value) {
        return value == OrderStatus.SUBMITTED || value == OrderStatus.PAID || value == OrderStatus.SHIPPED;
    }
    private void validateSubtotal(BigDecimal subtotal) {
        if (discountAmount.compareTo(subtotal) > 0) throw new IllegalArgumentException("Reduce the discount before reducing the subtotal.");
    }
    private void ensureEditable() {
        if (!isEditable()) throw new IllegalArgumentException("Orders in " + status + " status cannot be edited.");
    }
    private void touch() { updatedAt = LocalDateTime.now(); }
    public boolean isEditable() { return status == OrderStatus.DRAFT || status == OrderStatus.SUBMITTED; }
    public boolean hasItems() { return !items.isEmpty(); }
    public String getId() { return id; }
    public String getCustomerId() { return customerId; }
    public List<OrderItem> getItems() { return items.stream().map(OrderItem::copy).toList(); }
    public OrderStatus getStatus() { return status; }
    public BigDecimal getSubtotal() { return items.stream().map(OrderItem::getLineTotal).reduce(new BigDecimal("0.00"), BigDecimal::add); }
    public BigDecimal getDiscountAmount() { return discountAmount; }
    public BigDecimal getTotal() { return getSubtotal().subtract(discountAmount); }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
''')
p=P/'src/oms/domain/OrderItem.java';s=p.read_text()
s=s.replace('import java.math.RoundingMode;\n','')
s=s.replace('Objects.requireNonNull(productId, "productId must not be null")','DomainValues.text(productId, "Product id")').replace('Objects.requireNonNull(productName, "productName must not be null")','DomainValues.text(productName, "Product name")')
s=s.replace('        setQuantity(this.quantity + additionalQuantity);','''        if (additionalQuantity <= 0) throw new IllegalArgumentException("Additional quantity must be positive.");
        try { setQuantity(Math.addExact(this.quantity, additionalQuantity)); }
        catch (ArithmeticException error) { throw new IllegalArgumentException("Quantity is too large.", error); }''')
a=s.index('        Objects.requireNonNull(unitPrice');b=s.index('\n    }',a)
s=s[:a]+'        this.unitPrice = DomainValues.money(unitPrice, false);'+s[b:]
s=s.replace('.setScale(2, RoundingMode.HALF_UP)','.setScale(2)')
s=s.replace('    public String getProductId() {','''    public OrderItem copy() {
        return new OrderItem(productId, productName, quantity, unitPrice);
    }

    public String getProductId() {''')
s=s.replace('import java.util.Objects;\n','');p.write_text(s)
p=P/'src/oms/domain/Product.java';s=p.read_text()
for field,label in [('id','Product id'),('name','Product name'),('sku','SKU')]:s=s.replace(f'Objects.requireNonNull({field}, "{field} must not be null")',f'DomainValues.text({field}, "{label}")')
a=s.index('        Objects.requireNonNull(value');b=s.index('\n    }',a);s=s[:a]+'        return DomainValues.money(value, false);'+s[b:];s=s.replace('import java.math.RoundingMode;\n','').replace('import java.util.Objects;\n','');p.write_text(s)
p=P/'src/oms/domain/Customer.java';s=p.read_text()
for field,label in [('id','Customer id'),('name','Customer name'),('email','Email')]:s=s.replace(f'Objects.requireNonNull({field}, "{field} must not be null")',f'DomainValues.text({field}, "{label}")')
s=s.replace('        this.phone =','        if (!this.email.contains("@")) throw new IllegalArgumentException("Email must contain @.");\n        this.phone =');p.write_text(s)
for name,entity,plural in [('CustomerService','Customer','customers'),('ProductService','Product','products')]:
 p=P/f'src/oms/service/{name}.java';s=p.read_text();singular=entity.lower()
 s=s.replace(f'            {plural}ById.put({singular}.getId(), {singular});',f'            if ({plural}ById.putIfAbsent({singular}.getId(), {singular}) != null) throw new IllegalArgumentException("Duplicate {singular} id.");',1)
 s=s.replace(f'        return {plural}ById.values();',f'        return List.copyOf({plural}ById.values());');p.write_text(s)
p=P/'src/oms/service/OrderService.java';s=p.read_text()
s=s.replace('            ordersById.put(order.getId(), order);','''            if (customerService.findById(order.getCustomerId()).isEmpty()) throw new IllegalArgumentException("Order references a missing customer.");
            for (OrderItem item : order.getItems()) {
                if (productService.findById(item.getProductId()).isEmpty()) throw new IllegalArgumentException("Order item references a missing product.");
            }
            if (ordersById.putIfAbsent(order.getId(), order.copy()) != null) throw new IllegalArgumentException("Duplicate order id.");''',1)
s=s.replace('        return order;','        return order.copy();',1)
s=s.replace('return Optional.ofNullable(ordersById.get(id));','return Optional.ofNullable(ordersById.get(id)).map(Order::copy);')
s=s.replace('return new ArrayList<>(ordersById.values());','return ordersById.values().stream().map(Order::copy).toList();').replace('return ordersById.values();','return listOrders();')
a=s.index('        if (discountAmount.compareTo');b=s.index('        order.setDiscountAmount',a);s=s[:a]+s[b:]
s=s.replace('    public void removeProductFromOrder','''    public void updateItemQuantity(String orderId, String productId, int quantity) {
        requireOrder(orderId).setItemQuantity(productId, quantity);
    }

    public void removeProductFromOrder''')
p.write_text(s)
