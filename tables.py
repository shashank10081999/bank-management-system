import mysql.connector as connection
from constants import host , user , passwd , database

class Database_creation():

    def __init__(self , database  , host , user , passwd):

        try:
            self.database = database
            self.mydb = connection.connect(host  = host , user = user , passwd =passwd)
            self.cursor = self.mydb.cursor()
        except Exception as e :
            print("Issue with database connection , Please check the user name , password and host")
            raise e

    def is_database_created(self , database):
        
        is_database = False
        query = f"SHOW DATABASES LIKE '{database}'"
        self.cursor.execute(query)
        if len(self.cursor.fetchall()) > 0:
            is_database = True
        return is_database

    def create_database(self , database):

        if self.is_database_created(database):

            #print(f"{database} is already present")
            pass
        
        else:

            query = f"CREATE DATABASE {database}"

            self.cursor.execute(query)

            if self.is_database_created(database):
                print("Sucessfully create the database")
            else:
                print("database is not create please check")

    def  is_table_created(self, database, table_name):
        is_table = False 

        query = f"USE {database}"

        self.cursor.execute(query)

        query_table = f"SHOW TABLES LIKE '{table_name}'"
        self.cursor.execute(query_table)
        if len(self.cursor.fetchall()) > 0:
            is_table = True
        
        return is_table
    
    def create_tables(self , database):

        try:
            
            if self.is_table_created(database , "customers"):
                pass
                #print("Customers table is already present in the database")
            
            else:

                customer_query = "CREATE TABLE customers ( customer_id INT PRIMARY KEY AUTO_INCREMENT,\
                         customer_name VARCHAR(100) ,\
                         address VARCHAR(255) ,\
                         city VARCHAR(255) ,\
                         phone VARCHAR(20))"

                self.cursor.execute(customer_query)
            
                
            if self.is_table_created(database , "Branches"):
                pass
                #print("Branches table is already present in the database")
            
            else:
                
                branches_query = "CREATE TABLE Branches (\
                    branch_id INT PRIMARY KEY,\
                    name VARCHAR(255) NOT NULL,\
                    address VARCHAR(255) NOT NULL,\
                    phone VARCHAR(20),\
                    manager_name VARCHAR(255) NOT NULL,\
                    manager_phone VARCHAR(20),\
                    manager_email VARCHAR(255))"
                
                self.cursor.execute(branches_query)

            
            if self.is_table_created(database , "Accounts"):
                pass
                #print("Accounts table sis already present in the database")

            else:

                accounts_query = "CREATE TABLE Accounts ( account_number INT PRIMARY KEY , \
                    customer_id INT NOT NULL , \
                    account_type VARCHAR(20) NOT NULL , \
                    balance DECIMAL(10,2) NOT NULL , \
                    branch_id INT , \
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),\
                    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id))"
                
                self.cursor.execute(accounts_query)
            
            if self.is_table_created(database , "Transactions"):
                pass
                #print("Transactions table is already present in the database")
            
            else:
                transactions_query = "CREATE TABLE Transactions ( \
                    transaction_id INT PRIMARY KEY ,\
                    account_number INT NOT NULL,\
                    transaction_type VARCHAR(20) NOT NULL,\
                    amount DECIMAL(10,2) NOT NULL,\
                    transaction_date DATETIME NOT NULL,\
                    description VARCHAR(255) ,\
                    FOREIGN KEY (account_number) REFERENCES Accounts(account_number) )"
                
                self.cursor.execute(transactions_query)


            if self.is_table_created(database , "Employees"):
                pass
                #print("Employees table is present in the database")
            
            else:
                
                employees_query = "CREATE TABLE Employees ( \
                    employee_id INT PRIMARY KEY,\
                    branch_id INT,\
                    name VARCHAR(255) NOT NULL,\
                    job_title VARCHAR(255) NOT NULL,\
                    department VARCHAR(255) NOT NULL,\
                    phone VARCHAR(20),\
                    email VARCHAR(255),\
                    hire_date DATE NOT NULL,\
                    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id))"
                
                self.cursor.execute(employees_query)
                
            if self.is_table_created(database , "Loans"):
                pass
                #print("Loan table is already present in the database")
            
            else:
                
                loan_query = "CREATE TABLE Loans ( \
                    loan_id INT PRIMARY KEY,\
                    customer_id INT NOT NULL,\
                    amount DECIMAL(10, 2) NOT NULL,\
                    interest_rate DECIMAL(5, 2) NOT NULL,\
                    start_date DATE NOT NULL,\
                    end_date DATE NOT NULL,\
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                
                self.cursor.execute(loan_query)

            if self.is_table_created(database , "User_password"):
                pass
                #print("The User password table is already present in the database")

            else:
                user_password_query = "CREATE TABLE User_password (\
                    customer_id INT PRIMARY KEY,\
                    password_pin VARCHAR(20) NOT NULL,\
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                
                self.cursor.execute(user_password_query)

            if self.is_table_created(database , "employee_password"):
                pass
                #print("The User password table is already present in the database")

            else:
                user_password_query = "CREATE TABLE employee_password ( \
                    employee_id INT PRIMARY KEY,\
                    password_pin VARCHAR(20) NOT NULL , \
                    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id))"
                
                self.cursor.execute(user_password_query)

            if self.is_table_created(database , "appointment"):
                pass

            else:
                appointment_query = "CREATE TABLE appointment (\
                                    id INT NOT NULL AUTO_INCREMENT ,\
                                    customer_id INT NOT NULL,\
                                    customer_name VARCHAR(50) NOT NULL,\
                                    appointment_date DATE NOT NULL,\
                                    appointment_time TIME NOT NULL,\
                                    PRIMARY KEY (id),\
                                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)\
                                    )"
                self.cursor.execute(appointment_query)

            if self.is_table_created(database , "withdraw"):
                pass

            else:
                withdraw_query = "CREATE TABLE withdraw (\
                                withdraw_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                withdraw_amount INT NOT NULL,\
                                withdraw_date DATE NOT NULL,\
                                customer_id INT NOT NULL,\
                                FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                self.cursor.execute(withdraw_query)

            if self.is_table_created(database , "deposit"):
                pass
            else:
                deposit_query = "CREATE TABLE deposit (\
                                deposit_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                deposit_amount INT NOT NULL,\
                                despoit_date DATE NOT NULL,\
                                customer_id INT NOT NULL,\
                                FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                self.cursor.execute(deposit_query)
            
            if self.is_table_created(database , "NEFT_RTGS_Transfer"):
                pass
            
            else:
                transfer_query = "CREATE TABLE NEFT_RTGS_Transfer (\
                                transfer_if INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                transfer_amount INT NOT NULL,\
                                transfer_type VARCHAR(20),\
                                transfer_date DATE NOT NULL,\
                                customer_id INT NOT NULL,\
                                FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                self.cursor.execute(transfer_query)
                
            if self.is_table_created(database , "updated_balance"):
                pass
            else:
                update_balance_query = "CREATE TABLE updated_balance(\
                                        account_number INT NOT NULL PRIMARY KEY,\
                                        updated_amount INT,\
                                        updated_date DATE ,\
                                        FOREIGN KEY (account_number) REFERENCES Accounts(account_number))"
                self.cursor.execute(update_balance_query)

            if self.is_table_created(database , "loan_payment"):
                pass
            else:
                loan_payment_query = "CREATE TABLE loan_payment(\
                                       payment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                       payment_amount INT NOT NULL,\
                                       payment_date DATE,\
                                       customer_id INT,\
                                       FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"
                self.cursor.execute(loan_payment_query)


            
        except Exception as e:
            raise e 
        
    def initiate_database(self):
        self.create_database(self.database)
        self.create_tables(self.database)

        print("=================================The Bank Database is up and ready====================================================")

                






