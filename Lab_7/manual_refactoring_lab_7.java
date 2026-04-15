import java.util.*;

// Main class
class BankingSystem {
public static void main(String[] args){
BankService bank=new Bank();
LoanService loanService=new LoanService(bank);
bank.createAccount("SAVINGS","Rahul",1000);
bank.deposit("Rahul",500);
bank.withdraw("Rahul",200);
loanService.applyLoan("Rahul",1000);
}
}

interface BankService{
void createAccount(String type,String name,double balance);
void deposit(String name,double amount);
void withdraw(String name,double amount);
}

class Bank implements BankService{
private AccountService accountService=new AccountService();
public void createAccount(String type,String name,double balance){
Account acc=AccountFactory.createAccount(type,name,balance);
accountService.addAccount(acc);
}
public void deposit(String name,double amount){
Account acc=accountService.getAccount(name);
acc.balance+=amount;
}
public void withdraw(String name,double amount){
Account acc=accountService.getAccount(name);
acc.withdraw(amount);
}
}

class AccountService{
private Map<String,Account> accounts=new HashMap<>();
public void addAccount(Account acc){accounts.put(acc.name,acc);}
public Account getAccount(String name){return accounts.get(name);}
}

class AccountFactory{
public static Account createAccount(String type,String name,double balance){
switch(type){
case "SAVINGS": return new SavingsAccount(name,balance);
case "CURRENT": return new CurrentAccount(name,balance);
case "BUSINESS": return new BusinessAccount(name,balance);
default: throw new IllegalArgumentException("Invalid type");
}
}
}

abstract class Account{
String name;
double balance;
Account(String name,double balance){this.name=name;this.balance=balance;}
abstract void withdraw(double amount);
}

class SavingsAccount extends Account{
SavingsAccount(String name,double balance){super(name,balance);}
void withdraw(double amount){
if(balance-amount<500){System.out.println("Min balance");return;}
balance-=amount;
}
}

class CurrentAccount extends Account{
CurrentAccount(String name,double balance){super(name,balance);}
void withdraw(double amount){
if(balance-amount<-1000){System.out.println("Overdraft");return;}
balance-=amount;
}
}

class BusinessAccount extends Account{
BusinessAccount(String name,double balance){super(name,balance);}
void withdraw(double amount){
if(balance-amount<-5000){System.out.println("Business overdraft");return;}
balance-=amount;
}
}

interface TransactionOperations{void deposit();void withdraw();}
interface LoanOperations{void applyLoan();}

class MobileApp implements TransactionOperations,LoanOperations{
public void deposit(){System.out.println("Mobile deposit");}
public void withdraw(){System.out.println("Mobile withdraw");}
public void applyLoan(){System.out.println("Mobile loan");}
}

class ATM implements TransactionOperations{
public void deposit(){System.out.println("ATM deposit");}
public void withdraw(){System.out.println("ATM withdraw");}
}

class LoanService{
private BankService bank;
public LoanService(BankService bank){this.bank=bank;}
public void applyLoan(String name,double amount){
bank.deposit(name,amount);
System.out.println("Loan applied "+name);
}
}

class NotificationService{
public void notifyUser(String name){
System.out.println("Email sent to "+name);
System.out.println("SMS sent to "+name);
System.out.println("Push sent to "+name);
}
}

class LoggingService{
public void log(String type,String name,double amount){
System.out.println("LOG "+type+" "+amount+" "+name);
}
}

class ReportService{
public void generate(Collection<Account> accounts){
System.out.println("Report:");
for(Account acc:accounts){
System.out.println(acc.name+" -> "+acc.balance);
}
}
}

class InterestService{
public void apply(Account acc){
if(acc instanceof SavingsAccount){
acc.balance+=acc.balance*0.05;
}else if(acc instanceof BusinessAccount){
acc.balance+=acc.balance*0.02;
}
}
}

class TaxService{
public void calculate(Account acc){
System.out.println("Tax calculated");
}
}