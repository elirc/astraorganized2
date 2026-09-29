from pathlib import Path
P=Path(__file__).resolve().parent/'stage/14690be423dc'
(P/'src/oms/persistence/StoreSnapshot.java').write_text(r'''package oms.persistence;
import oms.domain.Customer;
import oms.domain.Order;
import oms.domain.Product;
import oms.service.CustomerService;
import oms.service.ProductService;
import oms.service.OrderService;
import java.util.List;

/** A detached, referentially valid snapshot for the single-threaded CLI. */
public class StoreSnapshot {
    private final List<Customer> customers;
    private final List<Product> products;
    private final List<Order> orders;
    public StoreSnapshot(List<Customer> customers, List<Product> products, List<Order> orders) {
        this.customers = List.copyOf(customers);
        this.products = List.copyOf(products);
        this.orders = orders.stream().map(Order::copy).toList();
        // Reuse the service constructors' duplicate and reference checks.
        new OrderService(this.orders, new CustomerService(this.customers), new ProductService(this.products));
    }
    public List<Customer> getCustomers() { return customers; }
    public List<Product> getProducts() { return products; }
    public List<Order> getOrders() { return orders.stream().map(Order::copy).toList(); }
}
''',encoding='utf-8')
(P/'src/oms/persistence/FileDataStore.java').write_text(r'''package oms.persistence;

import oms.domain.*;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** One atomic snapshot replaces the legacy four-file save operation. */
public class FileDataStore {
    private static final String HEADER = "# oms-snapshot-v1";
    private final Path directory;
    private final Path snapshotFile;
    public FileDataStore(Path dataDirectory) {
        directory = dataDirectory.toAbsolutePath().normalize();
        snapshotFile = directory.resolve("oms.snapshot.txt");
    }
    public StoreSnapshot load() {
        try {
            var rows = new ArrayList<String>();
            if (!Files.notExists(snapshotFile)) {
                List<String> lines = Files.readAllLines(snapshotFile);
                if (lines.size() < 2 || !HEADER.equals(lines.get(0))) throw new IOException("Missing or unsupported snapshot header.");
                rows.addAll(lines.subList(1, lines.size() - 1));
                StoreSnapshot snapshot = parseRows(rows);
                String expected = footer(snapshot);
                if (!expected.equals(lines.get(lines.size() - 1))) throw new IOException("Missing footer or incorrect record counts.");
                return snapshot;
            }
            String[] files = {"customers.txt", "products.txt", "orders.txt", "order_items.txt"};
            String[] tags = {"C|", "P|", "O|", "I|"};
            int present = 0;
            for (String file : files) if (!Files.notExists(directory.resolve(file))) present++;
            if (present != 0 && present != files.length) throw new IOException("Incomplete legacy dataset: all four files are required.");
            if (present != 0) {
                for (int index = 0; index < files.length; index++) {
                    for (String line : Files.readAllLines(directory.resolve(files[index]))) {
                        if (!line.isBlank() && !line.startsWith("#")) rows.add(tags[index] + line);
                    }
                }
            }
            return parseRows(rows);
        } catch (IOException | RuntimeException error) {
            throw new IllegalStateException("Failed to load order data: " + error.getMessage(), error);
        }
    }

    private StoreSnapshot parseRows(List<String> rows) {
        var customers = new ArrayList<Customer>();
        var products = new ArrayList<Product>();
        var orderRows = new LinkedHashMap<String, List<String>>();
        var itemRows = new LinkedHashMap<String, List<OrderItem>>();
        for (int index = 0; index < rows.size(); index++) {
            try {
                List<String> fields = DelimitedFileUtil.split(rows.get(index));
                switch (fields.get(0)) {
                    case "C" -> {
                        count(fields, 6);
                        customers.add(new Customer(fields.get(1), fields.get(2), fields.get(3), fields.get(4), LocalDateTime.parse(fields.get(5))));
                    }
                    case "P" -> {
                        count(fields, 6);
                        String active = fields.get(5);
                        if (!active.equals("true") && !active.equals("false")) throw new IllegalArgumentException("Active must be true or false.");
                        products.add(new Product(fields.get(1), fields.get(2), fields.get(3), new BigDecimal(fields.get(4)), Boolean.parseBoolean(active)));
                    }
                    case "O" -> {
                        count(fields, 7);
                        if (orderRows.putIfAbsent(fields.get(1), fields) != null) throw new IllegalArgumentException("Duplicate order id.");
                    }
                    case "I" -> {
                        count(fields, 6);
                        itemRows.computeIfAbsent(fields.get(1), key -> new ArrayList<>()).add(new OrderItem(fields.get(2), fields.get(3), Integer.parseInt(fields.get(4)), new BigDecimal(fields.get(5))));
                    }
                    default -> throw new IllegalArgumentException("Unknown record type.");
                }
            } catch (RuntimeException error) {
                throw new IllegalArgumentException("Invalid data record " + (index + 1) + ": " + error.getMessage(), error);
            }
        }
        for (String orderId : itemRows.keySet()) if (!orderRows.containsKey(orderId)) throw new IllegalArgumentException("Item references a missing order.");
        var orders = new ArrayList<Order>();
        for (Map.Entry<String, List<String>> entry : orderRows.entrySet()) {
            List<String> fields = entry.getValue();
            orders.add(Order.restore(fields.get(1), fields.get(2), OrderStatus.valueOf(fields.get(3)), new BigDecimal(fields.get(4)),
                    LocalDateTime.parse(fields.get(5)), LocalDateTime.parse(fields.get(6)), itemRows.getOrDefault(entry.getKey(), List.of())));
        }
        return new StoreSnapshot(customers, products, orders);
    }
    private void count(List<String> fields, int expected) {
        if (fields.size() != expected) throw new IllegalArgumentException("Unexpected field count.");
    }
    private String footer(StoreSnapshot snapshot) {
        long items = snapshot.getOrders().stream().mapToLong(order -> order.getItems().size()).sum();
        return "END|" + snapshot.getCustomers().size() + "|" + snapshot.getProducts().size() + "|" + snapshot.getOrders().size() + "|" + items;
    }
    public void save(StoreSnapshot snapshot) {
        try {
            // Constructor rechecks references and copies mutable order aggregates.
            StoreSnapshot validated = new StoreSnapshot(snapshot.getCustomers(), snapshot.getProducts(), snapshot.getOrders());
            var lines = new ArrayList<String>();
            lines.add(HEADER);
            for (Customer customer : validated.getCustomers()) lines.add(DelimitedFileUtil.join("C", customer.getId(), customer.getName(), customer.getEmail(), customer.getPhone(), customer.getCreatedAt().toString()));
            for (Product product : validated.getProducts()) lines.add(DelimitedFileUtil.join("P", product.getId(), product.getName(), product.getSku(), product.getPrice().toPlainString(), String.valueOf(product.isActive())));
            for (Order order : validated.getOrders()) {
                lines.add(DelimitedFileUtil.join("O", order.getId(), order.getCustomerId(), order.getStatus().name(), order.getDiscountAmount().toPlainString(), order.getCreatedAt().toString(), order.getUpdatedAt().toString()));
                for (OrderItem item : order.getItems()) lines.add(DelimitedFileUtil.join("I", order.getId(), item.getProductId(), item.getProductName(), String.valueOf(item.getQuantity()), item.getUnitPrice().toPlainString()));
            }
            lines.add(footer(validated));
            Files.createDirectories(directory);
            Path temporary = Files.createTempFile(directory, ".oms-", ".tmp");
            try {
                Files.write(temporary, lines);
                Files.move(temporary, snapshotFile, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            } finally { Files.deleteIfExists(temporary); }
        } catch (IOException | RuntimeException error) {
            throw new IllegalStateException("Failed to save order data: " + error.getMessage(), error);
        }
    }
}
''',encoding='utf-8')
p=P/'src/oms/persistence/DelimitedFileUtil.java';s=p.read_text()
s=s.replace('''                } else {
                    current.append(ch);
                }''','''                } else if (ch == 'r') {
                    current.append('\\r');
                } else if (ch == '|' || ch == '\\\\') {
                    current.append(ch);
                } else {
                    throw new IllegalArgumentException("Unknown escape sequence.");
                }''',1)
s=s.replace('        parts.add(current.toString());','        if (escaping) throw new IllegalArgumentException("Incomplete escape sequence.");\n        parts.add(current.toString());',1 if False else 0) if False else s
# The final append, not each delimiter branch, checks a dangling slash.
s=s.replace('''        parts.add(current.toString());
        return parts;''','''        if (escaping) throw new IllegalArgumentException("Incomplete escape sequence.");
        parts.add(current.toString());
        return parts;''')
s=s.replace('.replace("\\r", "")','.replace("\\r", "\\\\r")');p.write_text(s,encoding='utf-8')
p=P/'src/oms/App.java';s=p.read_text();s=s.replace('import java.util.Scanner;', 'import java.util.Scanner;\nimport java.util.NoSuchElementException;\nimport oms.domain.DomainValues;')
a=s.index('        dataStore = new FileDataStore');b=s.index('        customerService =',a)
s=s[:a]+'''        this(Path.of("data"));
    }

    public App(Path dataDirectory) {
        dataStore = new FileDataStore(dataDirectory);
        StoreSnapshot snapshot = dataStore.load();
'''+s[b:]
s=s.replace('        new App().run();','''        try {
            new App(args.length == 0 ? Path.of("data") : Path.of(args[0])).run();
        } catch (RuntimeException error) {
            System.out.println("Startup stopped: " + error.getMessage());
            System.out.println("Existing data was not replaced. Repair a separate copy before retrying.");
        }''')
s=s.replace('Data loads from ./data on startup and auto-saves on exit.','Data loads from the selected directory. Save with 12 or exit with 13.')
s=s.replace('        while (running) {','        try {\n        while (running) {',1)
s=s.replace('                case "13" -> running = exitApplication();','                case "13" -> running = exitApplication();\n                case "14" -> updateItemQuantity();')
s=s.replace('''        }
    }

    private void printMenu()''','''        }
        } catch (NoSuchElementException error) {
            System.out.println("Input ended. Saving completed changes.");
            saveNow();
        } finally {
            scanner.close();
        }
    }

    private void printMenu()''',1)
s=s.replace('        System.out.println("13. Exit");','        System.out.println("13. Exit");\n        System.out.println("14. Update item quantity");')
s=s.replace('''            System.out.println("Goodbye. Data could not be saved.");''','''            System.out.println("Data could not be saved. Session stays open so you can retry.");
            return true;''')
s=s.replace('''        } catch (RuntimeException e) {
            return false;''','''        } catch (RuntimeException e) {
            System.out.println(e.getMessage());
            return false;''',1)
s=s.replace('return new BigDecimal(value).setScale(2, RoundingMode.HALF_UP);','return DomainValues.money(new BigDecimal(value), true);').replace('''        } catch (NumberFormatException e) {
            System.out.println("Please enter a valid money amount, for example 19.99.");''','''        } catch (IllegalArgumentException e) {
            System.out.println("Please enter a non-negative amount with at most 2 decimal places, for example 19.99.");''')
a=s.index('    private void saveNow()');s=s[:a]+'''    private void updateItemQuantity() {
        try {
            String orderId = prompt("Order ID: ");
            String productId = prompt("Product ID: ");
            Integer quantity = readPositiveInt("New quantity: ");
            if (quantity == null) return;
            orderService.updateItemQuantity(orderId, productId, quantity);
            System.out.println("Item quantity updated.");
        } catch (IllegalArgumentException error) {
            System.out.println("Could not update quantity: " + error.getMessage());
        }
    }

'''+s[a:]
a=s.index('        while (running) {');b=s.index('        } catch (NoSuchElementException error)',a);s=s[:a]+''.join('    '+line+'\n' if line else '\n' for line in s[a:b].splitlines())+s[b:];p.write_text(s,encoding='utf-8')
s=(P.parent/'d0778f38946f/run.ps1').read_text().replace('bankapp.RegressionTests','oms.RegressionTests').replace('bankapp.App','oms.App');(P/'run.ps1').write_text(s,encoding='utf-8');(P/'.gitignore').write_text('out/\ndata/oms.snapshot.txt\ndata/.oms-*.tmp\n',encoding='utf-8')
