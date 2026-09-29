from pathlib import Path
B=Path(__file__).resolve().parent;P=B/'stage/d0778f38946f'
def write(rel,text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
write('test/bankapp/RegressionTests.java',r'''package bankapp;
import bankapp.model.*;
import bankapp.service.BankService;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
public class RegressionTests {
    static int passed,failed;
    interface Check { void run() throws Exception; }
    static void test(String name,Check check) { try { check.run();passed++;System.out.println("PASS "+name); } catch(Throwable error) { failed++;System.out.println("FAIL "+name+": "+error); } }
    static void equal(Object expected,Object actual) { if(!expected.equals(actual)) throw new AssertionError("Expected "+expected+"; got "+actual); }
    static void rejects(Class<? extends Throwable> type,Check check) throws Exception { try { check.run(); } catch(Throwable error) { if(type.isInstance(error)) return;throw error; } throw new AssertionError("Expected "+type.getSimpleName()); }
    static BigDecimal money(String value) { return new BigDecimal(value); }
    static BankAccount account(String id,String balance) { return new BankAccount(id,"Learner",money(balance),LocalDateTime.of(2026,1,2,3,4)); }
    static BankService service() { return new BankService(List.of(account("A","10.00"),account("B","0.00")),List.of()); }
    public static void main(String[] args) throws Exception {
        test("returned account cannot change service balance",()->{var s=service();s.getAccountById("A").increaseBalance(money("5"));equal(money("10.00"),s.getAccountById("A").getBalance());});
        test("constructor does not retain caller-owned mutable account",()->{var a=account("A","10.00");var s=new BankService(List.of(a),List.of());a.decreaseBalance(money("1"));equal(money("10.00"),s.getAccountById("A").getBalance());});
        test("duplicate account ids rejected",()->rejects(IllegalArgumentException.class,()->new BankService(List.of(account("A","1"),account("A","2")),List.of())));
        test("orphan transaction rejected",()->rejects(IllegalArgumentException.class,()->new BankService(List.of(),List.of(new Transaction("T","missing",TransactionType.DEPOSIT,money("1"),LocalDateTime.now(),null,null)))));
        test("sub-cent deposit rejected without balance or history mutation",()->{var s=service();rejects(IllegalArgumentException.class,()->s.deposit("A",money("1.001"),""));equal(money("10.00"),s.getAccountById("A").getBalance());equal(0,s.getAllTransactions().size());});
        test("negative model balance rejected",()->rejects(IllegalArgumentException.class,()->account("A","-1")));
        System.out.println("RESULT passed="+passed+" failed="+failed);
        if(failed!=0) System.exit(1);
    }
}
''')
write('src/bankapp/model/Money.java',r'''package bankapp.model;
import java.math.BigDecimal;
import java.math.RoundingMode;
public final class Money {
    private Money() { }
    public static BigDecimal nonNegative(BigDecimal amount) {
        if(amount==null) throw new IllegalArgumentException("Amount is required.");
        BigDecimal normalized;
        try { normalized=amount.setScale(2,RoundingMode.UNNECESSARY); }
        catch(ArithmeticException error) { throw new IllegalArgumentException("Amount must use at most 2 decimal places.",error); }
        if(normalized.signum()<0) throw new IllegalArgumentException("Amount cannot be negative.");
        return normalized;
    }
    public static BigDecimal positive(BigDecimal amount) {
        BigDecimal normalized=nonNegative(amount);
        if(normalized.signum()==0) throw new IllegalArgumentException("Amount must be greater than zero.");
        return normalized;
    }
    public static String text(String value,String field) {
        if(value==null || value.trim().isEmpty()) throw new IllegalArgumentException(field+" is required.");
        return value.trim();
    }
}
''')
p=P/'src/bankapp/model/BankAccount.java';s=p.read_text()
s=s.replace('Objects.requireNonNull(id, "id must not be null")','Money.text(id, "Account id")').replace('Objects.requireNonNull(accountHolderName, "accountHolderName must not be null")','Money.text(accountHolderName, "Account holder name")').replace('Objects.requireNonNull(balance, "balance must not be null")','Money.nonNegative(balance)')
s=s.replace('balance = balance.add(amount);','balance = balance.add(Money.positive(amount));').replace('balance = balance.subtract(amount);','''BigDecimal cleanAmount = Money.positive(amount);
        if(balance.compareTo(cleanAmount)<0) throw new IllegalStateException("Insufficient balance.");
        balance = balance.subtract(cleanAmount);''')
s=s.replace('    public String getId() {','''    public BankAccount copy() {
        return new BankAccount(id, accountHolderName, balance, createdAt);
    }

    public String getId() {''')
p.write_text(s)
p=P/'src/bankapp/model/Transaction.java';s=p.read_text().replace('Objects.requireNonNull(id, "id must not be null")','Money.text(id, "Transaction id")').replace('Objects.requireNonNull(accountId, "accountId must not be null")','Money.text(accountId, "Account id")').replace('Objects.requireNonNull(amount, "amount must not be null")','Money.positive(amount)')
s=s.replace('        this.relatedAccountId = relatedAccountId;','''        boolean transfer = type == TransactionType.TRANSFER_IN || type == TransactionType.TRANSFER_OUT;
        if(transfer) {
            this.relatedAccountId = Money.text(relatedAccountId, "Related account id");
            if(this.accountId.equals(this.relatedAccountId)) throw new IllegalArgumentException("Transfer accounts must differ.");
        } else {
            if(relatedAccountId != null) throw new IllegalArgumentException("Only transfers have related accounts.");
            this.relatedAccountId = null;
        }''')
p.write_text(s)
write('src/bankapp/model/BankSnapshot.java',r'''package bankapp.model;
import java.util.List;
/** Detached accounts and immutable transactions captured from one service state. */
public record BankSnapshot(List<BankAccount> accounts, List<Transaction> transactions) {
    public BankSnapshot {
        accounts=accounts.stream().map(BankAccount::copy).toList();
        transactions=List.copyOf(transactions);
    }
    @Override public List<BankAccount> accounts() {
        return accounts.stream().map(BankAccount::copy).toList();
    }
}
''')
p=P/'src/bankapp/service/BankService.java';s=p.read_text()
s=s.replace('import bankapp.model.TransactionType;','import bankapp.model.TransactionType;\nimport bankapp.model.Money;\nimport bankapp.model.BankSnapshot;\nimport java.util.HashSet;\nimport java.util.Objects;')
s=s.replace('import java.math.RoundingMode;\n','')
s=s.replace('''            accountsById.put(account.getId(), account);''','''            Objects.requireNonNull(account, "Account cannot be null.");
            if(accountsById.putIfAbsent(account.getId(), account.copy()) != null)
                throw new IllegalArgumentException("Duplicate account id: " + account.getId());''',1)
s=s.replace('        transactions.addAll(existingTransactions);','''        var transactionIds = new HashSet<String>();
        for(Transaction transaction : existingTransactions) {
            Objects.requireNonNull(transaction, "Transaction cannot be null.");
            if(!transactionIds.add(transaction.getId())) throw new IllegalArgumentException("Duplicate transaction id: " + transaction.getId());
            if(!accountsById.containsKey(transaction.getAccountId())) throw new IllegalArgumentException("Transaction references a missing account.");
            if(transaction.getRelatedAccountId()!=null && !accountsById.containsKey(transaction.getRelatedAccountId()))
                throw new IllegalArgumentException("Transfer references a missing related account.");
            transactions.add(transaction);
        }''')
# Synchronize operations and snapshot capture for one service instance.
import re
s=re.sub(r'    public (?!BankService\()(?=(?:BankAccount|List<|Transaction|Collection<))','    public synchronized ',s)
s=s.replace('        return account;','        return account.copy();',1)
s=s.replace('List<BankAccount> accounts = new ArrayList<>(accountsById.values());','List<BankAccount> accounts = new ArrayList<>(accountsById.values().stream().map(BankAccount::copy).toList());')
s=s.replace('accounts.sort(Comparator.comparing(BankAccount::getCreatedAt));','accounts.sort(Comparator.comparing(BankAccount::getCreatedAt).thenComparing(BankAccount::getId));')
s=s.replace('        return accountsById.get(accountId);','        BankAccount account = accountsById.get(accountId);\n        return account == null ? null : account.copy();')
s=s.replace('        account.increaseBalance(cleanAmount);\n','').replace('''        transactions.add(transaction);
        return transaction;''','''        account.increaseBalance(cleanAmount);
        transactions.add(transaction);
        return transaction;''',1)
s=s.replace('        account.decreaseBalance(cleanAmount);\n','')
# only withdrawal method's append now gets debit after constructing its transaction
idx=s.index('    public synchronized Transaction withdraw');end=s.index('    public synchronized List<Transaction> transfer',idx)
part=s[idx:end].replace('        transactions.add(transaction);','        account.decreaseBalance(cleanAmount);\n        transactions.add(transaction);');s=s[:idx]+part+s[end:]
s=s.replace('''        sourceAccount.decreaseBalance(cleanAmount);
        destinationAccount.increaseBalance(cleanAmount);

''','')
s=s.replace('        transactions.add(transferOut);','        sourceAccount.decreaseBalance(cleanAmount);\n        destinationAccount.increaseBalance(cleanAmount);\n        transactions.add(transferOut);')
s=s.replace('        return new ArrayList<>(accountsById.values());','        return new ArrayList<>(accountsById.values().stream().map(BankAccount::copy).toList());')
a=s.index('    private BigDecimal validateAmount');b=s.index('    private Transaction createTransaction',a)
s=s[:a]+'''    private BigDecimal validateAmount(BigDecimal amount, String actionName) {
        try { return Money.positive(amount); }
        catch(IllegalArgumentException error) { throw new IllegalArgumentException(actionName + ": " + error.getMessage(), error); }
    }

'''+s[b:]
a=s.index('    private BankAccount requireAccount')
s=s[:a]+'''    public synchronized BankSnapshot snapshot() {
        return new BankSnapshot(getAllAccounts(), getAllTransactions());
    }

    public synchronized BankAccount renameAccount(String accountId, String holderName) {
        BankAccount current = requireAccount(accountId);
        BankAccount replacement = new BankAccount(current.getId(), holderName, current.getBalance(), current.getCreatedAt());
        accountsById.put(accountId, replacement);
        return replacement.copy();
    }

    public synchronized boolean deleteUnusedAccount(String accountId) {
        BankAccount account = accountsById.get(accountId);
        if(account==null) return false;
        if(account.getBalance().signum()!=0 || transactions.stream().anyMatch(t -> accountId.equals(t.getAccountId()) || accountId.equals(t.getRelatedAccountId())))
            throw new IllegalStateException("Only a zero-balance account with no transaction history can be deleted.");
        accountsById.remove(accountId);
        return true;
    }

'''+s[a:]
p.write_text(s)
