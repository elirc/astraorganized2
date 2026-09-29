from pathlib import Path
B=Path(__file__).resolve().parent
P=B/'stage/d9a27fa7f308'
def write(rel, text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
write('test/expensetracker/RegressionTests.java',r'''package expensetracker;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.List;
public class RegressionTests {
    private static int passed, failed;
    interface Check { void run() throws Exception; }
    static void test(String name, Check check) { try { check.run(); passed++; System.out.println("PASS " + name); }
        catch (Throwable e) { failed++; System.out.println("FAIL " + name + ": " + e); } }
    static void equal(Object expected, Object actual) { if (!expected.equals(actual)) throw new AssertionError("Expected " + expected + "; got " + actual); }
    static void rejects(Class<? extends Throwable> type, Check check) throws Exception { try { check.run(); } catch (Throwable e) { if (type.isInstance(e)) return; throw e; } throw new AssertionError("Expected " + type.getSimpleName()); }
    static Expense expense(long id, String note) { return new Expense(id,"Lunch",new BigDecimal("12.30"),"Food",LocalDate.of(2026,1,2),note); }
    static void withFile(CheckWithPath check) throws Exception {
        Path directory = Files.createTempDirectory("j5-regression-");
        try { check.run(directory.resolve("expenses.txt")); }
        finally { try (var files=Files.list(directory)) { for(Path file:files.toList()) Files.delete(file); } Files.delete(directory); }
    }
    interface CheckWithPath { void run(Path file) throws Exception; }
    public static void main(String[] args) throws Exception {
        test("empty optional note survives a save and load", () -> withFile(file -> {
            var storage=new ExpenseFileStorage(file);storage.save(List.of(expense(1,"")));
            equal(1,storage.load().size());equal("",storage.load().get(0).getNote());
        }));
        test("corrupt record rejects the entire file", () -> withFile(file -> {
            var storage=new ExpenseFileStorage(file);storage.save(List.of(expense(1,"ok")));
            Files.writeString(file,Files.readString(file)+"broken\n");
            rejects(IOException.class,storage::load);
        }));
        test("duplicate load does not replace current state", () -> {
            var manager=new ExpenseManager();manager.loadExpenses(List.of(expense(9,"original")));
            rejects(IllegalArgumentException.class,()->manager.loadExpenses(List.of(expense(1,"a"),expense(1,"b"))));
            equal(9L,manager.getAllExpenses().get(0).getId());
        });
        test("domain rejects sub-cent precision", () -> rejects(IllegalArgumentException.class,()->new Expense(1,"x",new BigDecimal("0.001"),"Food",LocalDate.now(),"")));
        System.out.println("RESULT passed="+passed+" failed="+failed);
        if(failed!=0) System.exit(1);
    }
}
''')
# Source improvements: domain invariants, complete CRUD, strict loading and atomic replacement.
p=P/'src/expensetracker/Expense.java';s=p.read_text()
s=s.replace('import java.util.Objects;', 'import java.util.Objects;\nimport java.util.Locale;\nimport java.math.RoundingMode;')
s=s.replace('this.amount = Objects.requireNonNull(amount, "Amount cannot be null.");', '''try {
            this.amount = Objects.requireNonNull(amount, "Amount cannot be null.").setScale(2, RoundingMode.UNNECESSARY);
        } catch (ArithmeticException ex) {
            throw new IllegalArgumentException("Amount must use at most 2 decimal places.", ex);
        }''')
s=s.replace('this.category = requireText(category, "Category");','this.category = normalizeCategory(category);')
s=s.replace('    private static String requireText', '''    static String normalizeCategory(String category) {
        String[] words = requireText(category, "Category").split("\\\\s+");
        StringBuilder result = new StringBuilder();
        for (String word : words) {
            if (result.length() > 0) result.append(' ');
            result.append(word.substring(0, 1).toUpperCase(Locale.ROOT));
            result.append(word.substring(1).toLowerCase(Locale.ROOT));
        }
        return result.toString();
    }

    private static String requireText''')
p.write_text(s)
p=P/'src/expensetracker/ExpenseManager.java';s=p.read_text()
s=s.replace('import java.util.Map;', 'import java.util.Map;\nimport java.util.HashSet;\nimport java.util.Objects;\nimport java.util.Optional;\nimport java.util.NoSuchElementException;')
s=s.replace('''        expenses.clear();
        expenses.addAll(loadedExpenses);
        nextId = calculateNextId();''','''        List<Expense> candidate = new ArrayList<>(Objects.requireNonNull(loadedExpenses));
        var ids = new HashSet<Long>();
        long highestId = 0;
        for (Expense expense : candidate) {
            Objects.requireNonNull(expense, "Saved expense cannot be null.");
            if (!ids.add(expense.getId())) throw new IllegalArgumentException("Duplicate expense id: " + expense.getId());
            highestId = Math.max(highestId, expense.getId());
        }
        // Validate the entire candidate before replacing the current state.
        expenses.clear();
        expenses.addAll(candidate);
        nextId = highestId == Long.MAX_VALUE ? 0 : highestId + 1;''')
s=s.replace('''        String cleanTitle = requireText(title, "Title");''','''        if (nextId == 0) throw new IllegalStateException("Expense id space is exhausted.");
        String cleanTitle = requireText(title, "Title");''',1)
s=s.replace('        nextId++;','        nextId = nextId == Long.MAX_VALUE ? 0 : nextId + 1;')
a=s.index('    private long calculateNextId()');b=s.index('    private BigDecimal parseAmount',a)
s=s[:a]+'''    public Optional<Expense> findExpense(long id) {
        return expenses.stream().filter(expense -> expense.getId() == id).findFirst();
    }

    public Expense updateExpense(long id, String title, String amount, String category, String date, String note) {
        for (int i = 0; i < expenses.size(); i++) {
            if (expenses.get(i).getId() == id) {
                // Build a valid replacement before touching the live collection.
                Expense replacement = new Expense(id, title, parseAmount(amount), category, parseDate(date), note);
                expenses.set(i, replacement);
                return replacement;
            }
        }
        throw new NoSuchElementException("Expense #" + id + " does not exist.");
    }

    public boolean deleteExpense(long id) {
        return expenses.removeIf(expense -> expense.getId() == id);
    }

'''+s[b:]
a=s.index('    private String normalizeCategory(')
s=s[:a]+'''    private String normalizeCategory(String category) {
        return Expense.normalizeCategory(category);
    }
}
'''
p.write_text(s)
p=P/'src/expensetracker/ExpenseFileStorage.java';s=p.read_text()
s=s.replace('import java.nio.file.Path;', 'import java.nio.file.Path;\nimport java.nio.file.StandardCopyOption;\nimport java.util.HashSet;\nimport java.util.Objects;')
s=s.replace('this.filePath = filePath;', 'this.filePath = Objects.requireNonNull(filePath).toAbsolutePath().normalize();')
s=s.replace('        List<Expense> expenses = new ArrayList<>();','        List<Expense> expenses = new ArrayList<>();\n        var ids = new HashSet<Long>();',1)
s=s.replace('''                    expenses.add(parseLine(trimmedLine));''','''                    Expense expense = parseLine(line);
                    if (!ids.add(expense.getId())) throw new IllegalArgumentException("Duplicate expense id: " + expense.getId());
                    expenses.add(expense);''')
s=s.replace('''                    System.out.println("Skipping invalid saved record on line " + lineNumber + ": " + ex.getMessage());''','''                    throw new IOException("Invalid saved record on line " + lineNumber + ": " + ex.getMessage(), ex);''')
a=s.index('    public void save(');b=s.index('    private String toLine(',a)
s=s[:a]+'''    public void save(List<Expense> expenses) throws IOException {
        // Snapshot and serialize first: invalid input cannot truncate existing data.
        List<Expense> snapshot = List.copyOf(expenses);
        var validator = new ExpenseManager();
        validator.loadExpenses(snapshot);
        List<String> lines = new ArrayList<>();
        lines.add("# id\\ttitle\\tamount\\tcategory\\tdate\\tnote");
        for (Expense expense : snapshot) lines.add(toLine(expense));

        Path parent = filePath.getParent();
        Files.createDirectories(parent);
        Path temporary = Files.createTempFile(parent, ".expenses-", ".tmp");
        try {
            Files.write(temporary, lines);
            // Fail visibly if the filesystem cannot provide atomic replacement.
            Files.move(temporary, filePath, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
        } finally {
            Files.deleteIfExists(temporary);
        }
    }

'''+s[b:]
s=s.replace('import java.io.BufferedWriter;\n','')
s=s.replace('default -> result.append(current);','default -> throw new IllegalArgumentException("Unknown escape sequence.");')
s=s.replace("            result.append('\\\\');",'            throw new IllegalArgumentException("Incomplete escape sequence.");')
s=s.replace('// This prevents escaped tab characters from being treated as separators.', '// Retain escape pairs for decoding while splitting physical tab separators.')
p.write_text(s)
p=P/'src/expensetracker/App.java';s=p.read_text()
s=s.replace('import java.util.Scanner;', 'import java.util.Scanner;\nimport java.util.NoSuchElementException;')
s=s.replace('Path filePath = Path.of("data", "expenses.txt");','Path filePath = args.length == 0 ? Path.of("data", "expenses.txt") : Path.of(args[0]);')
s=s.replace('        loadExpenses();','        if (!loadExpenses()) return;',1)
s=s.replace('''        } finally {
            saveExpenses();''','''        } catch (NoSuchElementException ex) {
            System.out.println("Input ended. Saving completed changes.");
        } finally {
            saveExpenses();''',1)
s=s.replace('    private void loadExpenses() {','    private boolean loadExpenses() {')
s=s.replace('''            System.out.println("Loaded " + expenseManager.getAllExpenses().size() + " expense(s).");''','''            System.out.println("Loaded " + expenseManager.getAllExpenses().size() + " expense(s).");
            return true;''')
s=s.replace('''            System.out.println("Could not load saved expenses. Starting with an empty list.");
            expenseManager.loadExpenses(List.of());''','''            System.out.println("Could not load saved expenses: " + ex.getMessage());
            System.out.println("Startup stopped. The saved file was not changed; repair a copy before retrying.");
            return false;''')
s=s.replace('''        System.out.println("7. Exit");''','''        System.out.println("7. Save and exit");
        System.out.println("8. Update expense");
        System.out.println("9. Delete expense");''')
s=s.replace('''            default:
                System.out.println("Invalid menu option. Please choose a number from 1 to 7.");''','''            case "8":
                updateExpenseFlow();
                return true;
            case "9":
                deleteExpenseFlow();
                return true;
            default:
                System.out.println("Invalid menu option. Please choose a number from 1 to 9.");''')
s=s.replace('''        } catch (IllegalArgumentException ex) {
            System.out.println("Could not add expense:''','''        } catch (IllegalArgumentException | IllegalStateException ex) {
            System.out.println("Could not add expense:''',1)
a=s.index('    private void filterByCategoryFlow()')
s=s[:a]+'''    private void updateExpenseFlow() {
        try {
            long id = Long.parseLong(prompt("Expense id"));
            if (expenseManager.findExpense(id).isEmpty()) {
                System.out.println("Expense #" + id + " does not exist.");
                return;
            }
            String title = prompt("New title");
            String amount = prompt("New amount");
            String category = prompt("New category");
            String date = prompt("New date (yyyy-MM-dd)");
            String note = prompt("New note (optional; blank clears it)");
            expenseManager.updateExpense(id, title, amount, category, date, note);
            System.out.println("Updated expense #" + id + ".");
        } catch (IllegalArgumentException ex) {
            System.out.println("Could not update expense: " + ex.getMessage());
        }
    }

    private void deleteExpenseFlow() {
        try {
            long id = Long.parseLong(prompt("Expense id"));
            if (expenseManager.findExpense(id).isEmpty()) {
                System.out.println("Expense #" + id + " does not exist.");
                return;
            }
            if (!prompt("Delete expense #" + id + "? Type yes to confirm").equalsIgnoreCase("yes")) {
                System.out.println("Deletion cancelled.");
                return;
            }
            expenseManager.deleteExpense(id);
            System.out.println("Deleted expense #" + id + ".");
        } catch (IllegalArgumentException ex) {
            System.out.println("Could not delete expense: " + ex.getMessage());
        }
    }

'''+s[a:]
p.write_text(s)
