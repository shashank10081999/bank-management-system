import mysql.connector as connection
import random
import datetime
from constants import host , user , passwd , database
import re

mydb = connection.connect(host  = host , user = user , passwd =passwd)


cur = mydb.cursor()

cur.execute("use bank_management_system")
#cur.execute("select employee_id from Employees")
#data = cur.fetchall()

#cur.execute("create table employee_password (employee_id int PRIMARY KEY, password varchar(20) , FOREIGN KEY (employee_id) REFERENCES Employees(employee_id))")

#for i in data:
#    user_password_query = f"insert into employee_password (employee_id , password) values ({i[0]} , 'abc123')"
#    cur.execute(user_password_query)
#    mydb.commit()

cur.execute("select * from User_password ")

""" for i in cur.fetchall():
    query = f"INSERT INTO loan_payment ( payment_amount , payment_date , customer_id) VALUES ( {random.randint(100,1000)} , '{datetime.now().strftime('%Y-%m-%d')}' , {i[0]})"

    cur.execute(query)

    mydb.commit()

cur.execute("select customer_id from customers")

for i in cur.fetchall():

    withdraw = f"INSERT INTO withdraw (withdraw_amount , withdraw_date , customer_id) values ({random.randint(100,200)} , '{datetime.now().strftime('%Y-%m-%d')}' , {i[0]})"
    deposit = f"INSERT INTO deposit (deposit_amount , despoit_date , customer_id) values ({random.randint(500,700)} , '{datetime.now().strftime('%Y-%m-%d')}' , {i[0]})"
    transfer = f"INSERT INTO NEFT_RTGS_Transfer (transfer_type , transfer_date, transfer_amount , customer_id) values ('National' , '{datetime.now().strftime('%Y-%m-%d')}' , {random.randint(100,250)} , {i[0]})"

    cur.execute(withdraw)
    cur.execute(deposit)
    cur.execute(transfer)

    mydb.commit() """

def newList():
    """ l = list(l)
    new_list = []
    l[2] = re.findall(r"\d+\.\d+", str(l[2]))[0]
    l[3] = re.findall(r"\d+\.\d+", str(l[3]))[0]

    l[4] = l[4].strftime("%Y-%m-%d")
    l[5] = l[5].strftime("%Y-%m-%d") """

    new_list = []

    new_list.append(random.choice([24,25,26,27]))
    new_list.append(random.choice(["JPMorgan Chase" ,  "Bank of America" , "3. Citigroup " ,  "Wells Fargo" , "U.S. Bancorp" ,  "PNC Financial Services"]))
    new_list.append("North elm denton")
    new_list.append("123456789")
    new_list.append(random.choice(["Shashank" , "Sanju" , "Monika" , "rmsh"]))
    new_list.append("123456")
    new_list.append("xyz@gmail.com")


    



    return tuple(new_list)


#for i in cur.fetchall():
#    print(newList(i) , "," , end = "\t")

for i in range(1,30):
    print(newList() , end="/t")

