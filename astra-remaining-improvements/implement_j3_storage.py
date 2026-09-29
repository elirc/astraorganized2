from pathlib import Path
P=Path(__file__).resolve().parent/'stage/d0778f38946f'
(P/'src/bankapp/storage/FileStorage.java').write_text(r'''package bankapp.storage;

import bankapp.model.*;
import bankapp.service.BankService;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/** One versioned atomic snapshot; the old two-file format is read only for migration. */
public class FileStorage {
    private static final String HEADER = "# bank-snapshot-v1";
    private final Path directory;
    private final Path snapshotFile;
    public FileStorage(Path dataDirectory) {
        directory=dataDirectory.toAbsolutePath().normalize();
        snapshotFile=directory.resolve("bank.snapshot.txt");
    }

    public BankSnapshot loadSnapshot() throws IOException {
        var accounts=new ArrayList<BankAccount>();
        var transactions=new ArrayList<Transaction>();
        if(!Files.notExists(snapshotFile)) {
            List<String> lines=Files.readAllLines(snapshotFile);
            if(lines.isEmpty() || !HEADER.equals(lines.get(0))) throw new IOException("Unsupported or missing bank snapshot header.");
            for(int i=1;i<lines.size();i++) {
                String line=lines.get(i);
                if(line.isBlank()) continue;
                try {
                    if(line.startsWith("A|")) accounts.add(parseAccount(line.substring(2)));
                    else if(line.startsWith("T|")) transactions.add(parseTransaction(line.substring(2)));
                    else throw new IllegalArgumentException("Unknown record type.");
                } catch(RuntimeException error) { throw new IOException("Invalid bank snapshot record on line "+(i+1)+".",error); }
            }
        } else {
            Path accountsFile=directory.resolve("accounts.txt");
            Path transactionsFile=directory.resolve("transactions.txt");
            boolean noAccounts=Files.notExists(accountsFile), noTransactions=Files.notExists(transactionsFile);
            if(noAccounts != noTransactions) throw new IOException("Incomplete legacy data: both accounts.txt and transactions.txt are required.");
            if(!noAccounts) {
                readLegacy(accountsFile,accounts,transactions,true);
                readLegacy(transactionsFile,accounts,transactions,false);
            }
        }
        return validate(accounts,transactions);
    }

    private void readLegacy(Path file,List<BankAccount> accounts,List<Transaction> transactions,boolean accountFile) throws IOException {
        List<String> lines=Files.readAllLines(file);
        for(int i=0;i<lines.size();i++) {
            if(lines.get(i).isBlank()) continue;
            try {
                if(accountFile) accounts.add(parseAccount(lines.get(i)));
                else transactions.add(parseTransaction(lines.get(i)));
            } catch(RuntimeException error) { throw new IOException("Invalid legacy "+file.getFileName()+" record on line "+(i+1)+".",error); }
        }
    }

    private BankSnapshot validate(List<BankAccount> accounts,List<Transaction> transactions) throws IOException {
        try { return new BankService(accounts,transactions).snapshot(); }
        catch(RuntimeException error) { throw new IOException("Invalid bank snapshot: "+error.getMessage(),error); }
    }

    public void saveSnapshot(BankSnapshot snapshot) throws IOException {
        BankSnapshot validated=validate(snapshot.accounts(),snapshot.transactions());
        var lines=new ArrayList<String>();lines.add(HEADER);
        for(BankAccount account:validated.accounts()) lines.add("A|"+join(account.getId(),account.getAccountHolderName(),account.getBalance().toPlainString(),account.getCreatedAt().toString()));
        for(Transaction transaction:validated.transactions()) lines.add("T|"+join(transaction.getId(),transaction.getAccountId(),transaction.getType().name(),transaction.getAmount().toPlainString(),transaction.getTimestamp().toString(),transaction.getDescription(),transaction.getRelatedAccountId()));
        Files.createDirectories(directory);
        Path temporary=Files.createTempFile(directory,".bank-",".tmp");
        try {
            Files.write(temporary,lines);
            Files.move(temporary,snapshotFile,StandardCopyOption.ATOMIC_MOVE,StandardCopyOption.REPLACE_EXISTING);
        } finally { Files.deleteIfExists(temporary); }
    }

    private BankAccount parseAccount(String line) {
        List<String> fields=split(line,4);
        return new BankAccount(fields.get(0),fields.get(1),new BigDecimal(fields.get(2)),LocalDateTime.parse(fields.get(3)));
    }
    private Transaction parseTransaction(String line) {
        List<String> fields=split(line,7);
        return new Transaction(fields.get(0),fields.get(1),TransactionType.valueOf(fields.get(2)),new BigDecimal(fields.get(3)),LocalDateTime.parse(fields.get(4)),nullable(fields.get(5)),nullable(fields.get(6)));
    }
    private String nullable(String text) { return text.isEmpty()?null:text; }
    private String join(String... fields) {
        var escaped=new ArrayList<String>();
        for(String field:fields) escaped.add(escape(field==null?"":field));
        return String.join("|",escaped);
    }
    private String escape(String value) { return value.replace("\\","\\\\").replace("|","\\|").replace("\n","\\n").replace("\r","\\r"); }
    private List<String> split(String line,int expected) {
        var fields=new ArrayList<String>();var current=new StringBuilder();boolean escaping=false;
        for(int i=0;i<line.length();i++) {
            char character=line.charAt(i);
            if(escaping) {
                current.append(switch(character) {
                    case 'n' -> '\n';case 'r' -> '\r';case '|' -> '|';case '\\' -> '\\';
                    default -> throw new IllegalArgumentException("Unknown escape sequence.");
                });escaping=false;
            } else if(character=='\\') escaping=true;
            else if(character=='|') { fields.add(current.toString());current.setLength(0); }
            else current.append(character);
        }
        if(escaping) throw new IllegalArgumentException("Incomplete escape sequence.");
        fields.add(current.toString());
        if(fields.size()!=expected) throw new IllegalArgumentException("Unexpected field count.");
        return fields;
    }
}
''',encoding='utf-8')
p=P/'src/bankapp/App.java';s=p.read_text()
s=s.replace('import java.util.Scanner;', 'import java.util.Scanner;\nimport java.util.NoSuchElementException;\nimport bankapp.model.BankSnapshot;')
s=s.replace('    private final FileStorage fileStorage = new FileStorage(Path.of("data"));','    private final FileStorage fileStorage;')
s=s.replace('''        this.bankService = new BankService(fileStorage.loadAccounts(), fileStorage.loadTransactions());''','''        this(Path.of("data"));
    }

    public App(Path dataDirectory) throws IOException {
        this.fileStorage = new FileStorage(dataDirectory);
        BankSnapshot snapshot = fileStorage.loadSnapshot();
        this.bankService = new BankService(snapshot.accounts(), snapshot.transactions());''')
s=s.replace('            new App().run();','            new App(args.length == 0 ? Path.of("data") : Path.of(args[0])).run();')
s=s.replace('''        while (running) {''','''        try {
        while (running) {''',1)
s=s.replace('''                    default -> System.out.println("Please choose a valid menu option.");''','''                    case "8" -> renameAccount();
                    case "9" -> deleteUnusedAccount();
                    default -> System.out.println("Please choose a valid menu option.");''')
s=s.replace('''        }
    }

    private void printMenu()''','''        }
        } catch (NoSuchElementException exception) {
            saveData();
            System.out.println("Input ended. Completed operations are saved.");
        } finally {
            scanner.close();
        }
    }

    private void printMenu()''',1)
s=s.replace('''        System.out.println("7 Exit");''','''        System.out.println("7 Exit");
        System.out.println("8 Rename account holder");
        System.out.println("9 Delete unused account");''')
s=s.replace('''        fileStorage.saveAccounts(bankService.getAccountsForSaving());
        fileStorage.saveTransactions(bankService.getAllTransactions());''','''        fileStorage.saveSnapshot(bankService.snapshot());''')
a=s.index('    private BigDecimal readAmount')
s=s[:a]+'''    private void renameAccount() throws IOException {
        System.out.print("Account ID: ");
        String accountId = scanner.nextLine().trim();
        System.out.print("New holder name: ");
        String holderName = scanner.nextLine();
        bankService.renameAccount(accountId, holderName);
        saveData();
        System.out.println("Account holder updated.");
    }

    private void deleteUnusedAccount() throws IOException {
        System.out.print("Account ID: ");
        String accountId = scanner.nextLine().trim();
        if(bankService.getAccountById(accountId)==null) {
            System.out.println("Account not found.");
            return;
        }
        System.out.print("Delete unused account? Type yes to confirm: ");
        if(!scanner.nextLine().trim().equalsIgnoreCase("yes")) {
            System.out.println("Deletion cancelled.");
            return;
        }
        bankService.deleteUnusedAccount(accountId);
        saveData();
        System.out.println("Unused account deleted.");
    }

'''+s[a:]
p.write_text(s,encoding='utf-8')
# Reuse the established runner pattern with recursive Java package discovery.
s=(P.parent/'d9a27fa7f308/run.ps1').read_text().replace('src/expensetracker','src').replace('test/expensetracker','test').replace("-Filter '*.java'","-Recurse -Filter '*.java'").replace('expensetracker.RegressionTests','bankapp.RegressionTests').replace('expensetracker.App','bankapp.App').replace('data/expenses.txt','data')
(P/'run.ps1').write_text(s,encoding='utf-8')
(P/'.gitignore').write_text('out/\ndata/bank.snapshot.txt\ndata/.bank-*.tmp\n',encoding='utf-8')
