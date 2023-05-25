from constants import host , user , passwd , database
from tables import Database_creation
from values import Insert_values
import numpy as np
import  mysql.connector as sql
from menu import menu
import datetime as dt


#cur.execute('create table user_table(username varchar(25) primary key,passwrd varchar(25) not null )')
print()
print('====================================WELCOME TO BANK WEBSITE============================================================')
print()

mydb = Database_creation(database , host , user , passwd)
mydb.initiate_database()

#values = Insert_values(database , host , user , passwd)
#values.initiate_inserting_values()

conn=sql.connect(host=host,user=user,passwd=passwd,database=database)
cur = conn.cursor()

print()
print('1.REGISTER')
print()
print('2.LOGIN')
print()

n  =int(input("Please enter your number "))
print()

def login_function(customer_id , pin_password):

    menu_object = menu(host=host,user=user,passwd=passwd,database=database , customer_id= customer_id)

    cur.execute(f"SELECT password_pin FROM User_password where customer_id = {customer_id}")
    if pin_password == cur.fetchall()[0][0]:
        menu_object.options()
    else:
        print("Incorrect password")


if n==2:
    customer_id = int(input("Please neter the customer id "))
    pin_password = int(input("Please enter your pin "))
    login_function(customer_id , pin_password)

elif n ==1:
    customer_name = input("Please enter your name ")
    print()
    customer_address = input("Please enter your address ")
    print()
    customer_city = input("Please enter your city ")
    print()
    customer_phone = input("Please enter your phone number ")
    print()
    customer_pin = int(input("Please set passcode "))
    print()

    #print("INSERT INTO customers(customer_id , customer_name , address , city , phone) VALUES (0 , '%s' , '%s' , '%s' , '%s')" % (customer_name, customer_address , customer_city , customer_phone))

    featch_query = "select * from Customers where phone = '%s'" %(customer_phone)

    cur.execute(featch_query)

    data = cur.fetchall()

    if len(data) != 0:
        raise Exception("We already have a account with same phone")
     
    
    cur.execute("INSERT INTO customers(customer_id , customer_name , address , city , phone) VALUES (0 , '%s' , '%s' , '%s' , '%s')" % (customer_name, customer_address , customer_city , customer_phone))
    
    conn.commit()

    featch_query = "select * from Customers where customer_name = '%s' and phone = '%s'" %(customer_name , customer_phone)

    cur.execute(featch_query)


    data = cur.fetchall()

    customer_id = data[0][0]

    pin_query = f"INSERT INTO User_password (customer_id , password_pin)\
                                VALUES ({customer_id} , {customer_pin})"
    
    cur.execute(pin_query)
    conn.commit()

    print()
    print("You have successfully Registered in website")
    login_function(customer_id , customer_pin)


