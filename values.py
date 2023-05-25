import mysql.connector as connection
from constants import host , user , passwd , database
import random
import datetime
import numpy as np

class Insert_values():
    
    def __init__(self , database , host , user , passwd):
        try:
            self.database = database
            self.mydb = connection.connect(host = host , user = user , passwd = passwd)
            self.cursor = self.mydb.cursor()
            print("connected to the database successfully")
        except Exception as e:
            raise e
        
    def customer_values(self):
        r = []
        name = ["Shashank" , "Vinay" , "Harish" , "Sanjana" , "Venkat" , "Harani" , "Bhargav" , "Lohith" , "Manish" , "Varam" , "Vandana" , "Lavanya" , "Monika" ,"Kishore" , "Naveen" , "Anil"]
        ph_no = []
        s = ""
        ph_no.append(random.randint(6, 9))
  
        for i in range(1, 10):
            ph_no.append(random.randint(0, 9))

        for j in ph_no:
            s = s + str(j)
        
        return random.choice(name) , s
    
    def insert_values(self):
        try :
            self.cursor.execute(f"USE {self.database}")

            # self.cursor.execute("INSERT INTO Branches (branch_id , name , address ,phone ,manager_name ,manager_phone ,manager_email)\
            #                     VALUES (24 , 'MVP' , 'MVP' , '2222222' , 'shashank' , '3333333' , 'shashank@gmail.com'),\
            #                     (25 , 'Denton' , 'Denton' , '2222223' , 'lokhi' , '3333333' , 'lokhi@gmail.com'),\
            #                     (26 , 'Boston' , 'Boston' , '2222224' , 'vaishu' , '3333333' , 'vaishu@gmail.com'),\
            #                     (27 , 'Dallas' , 'Dallas' , '2222225' , 'bhargav' , '3333333' , 'bhargav@gmail.com'),\
            #                     (28 , 'Frisco' , 'Frisco' , '2222226' , 'varsha' , '3333333' , 'varsha@gmail.com')")

            for i in range(1,201):
                name , phone_no = self.customer_values()
                self.cursor.execute(f"INSERT INTO customers (customer_id , customer_name , address , city , phone)\
                                VALUES ({i} , '%s' , 'North elm stree' , 'Denton' , '%s')" % (name, phone_no))

                account_type = random.choice(["saving", "current"])
                self.cursor.execute(f"INSERT INTO Accounts\
                                (account_number , customer_id , account_type , balance , branch_id )\
                                VALUES ({10000000+i} , {i} , '{account_type}' , {random.randint(100,500)} , {random.choice([24 , 25 , 26 , 27 , 28])})")
                
                self.cursor.execute(f"INSERT INTO User_password (customer_id , password_pin)\
                                VALUES ({i} , 'abc123')")
                
                if i % 5 == 0:
                    rate = random.randint(0,12)
                    amount = random.randint(10000,50000)
                    start_date = datetime.date(random.randint(1999 , 2023) , random.randint(1,12) , random.randint(1,28))
                    end_date = datetime.date(random.randint(1999 , 2023) , random.randint(1,12) , random.randint(1,28))

                    self.cursor.execute(f"INSERT INTO Loans (loan_id , customer_id , amount , interest_rate ,start_date ,end_date)\
                                VALUES ({1000 +i} , {i} , {amount} , {rate} , '%s' , '%s')" % (start_date, end_date))

                for j in range(5):
                    transaction_type = random.choice(["internation", "national"])

                    self.cursor.execute(f"INSERT INTO Transactions\
                                (transaction_id , account_number , transaction_type , amount , transaction_date , description)\
                                VALUES ({random.randint(1,20000000)} , {10000000+i} , '%s' , 100 , '2015-04-03 14:00:45' , 'nothing')\
                                " % (transaction_type))
            
            for i in range(50):
                name , phone_no = self.customer_values()
                branche_id = [24,25,26,27,28]
                job_title = random.choice(["Bank clerk" , "Assistant Manager" , "Banking associate" , "Senior banker"])
                hire_date = str(datetime.date(random.randint(1999 , 2023) , random.randint(1,12) , random.randint(1,28)))
                self.cursor.execute(f"INSERT INTO Employees\
                                (employee_id , branch_id , name ,job_title ,department ,phone ,email ,hire_date)\
                                VALUES ({i} , {random.choice(branche_id)},  '%s' , '%s' , 'loan' , '%s' , '%s' , '%s')" % (name , job_title , phone_no , name+'@gamel.com' , hire_date))
                
                self.cursor.execute(f"INSERT INTO employee_password(employee_id, password_pin) VALUES ({i} , 'abc123')")
            
            self.mydb.commit()  



        except Exception as e:
            raise e
    
    def initiate_inserting_values(self):
        self.insert_values()

        print("values are inserted into the tables")



