import streamlit as st
from streamlit_option_menu import option_menu
from constants import host , user , passwd , database
from tables import Database_creation
from values import Insert_values
import numpy as np
import  mysql.connector as sql
from menu import menu
import datetime as dt
import streamlit_authenticator as stauth

st.title("Bank management system")

mydb = Database_creation(database , host , user , passwd)
mydb.initiate_database()

#values = Insert_values(database , host , user , passwd)
#values.initiate_inserting_values()

conn=sql.connect(host=host,user=user,passwd=passwd,database=database)
cur = conn.cursor()


options = st.selectbox("Customers or Employee" , ("Select a option" , "customer" , "employee") , label_visibility = "hidden")

if not options:
    st.stop()

if options == "customer":

    customer_id = st.number_input("Please enter the customer_id")
    password = st.text_input("Please enter the password" , type="password")

    #button_status = st.button("Login")

    if not customer_id or not password:
        st.stop()

    cur.execute(f"SELECT password_pin FROM User_password where customer_id = {customer_id}")
    state = (password == cur.fetchall()[0][0])

    #login_state = st.button("Login")


    if not state:
        st.warning("Password is incorrect")
        st.stop()
    
    else:

        menu_object = menu(host=host,user=user,passwd=passwd,database=database , customer_id= customer_id)


        with st.sidebar:
            selected = option_menu(
                menu_title = "Main Menu",
                options = ['Transaction', 'Customer details', 'Transaction details', 'Check your account balance', 'Update account details', 'Loan details', 'Appointment'] , default_index=1)

        if selected == "Customer details":
            menu_object.options(2)

        elif selected == "Transaction":
            menu_object.options(1)

        elif selected == "Transaction details":
            menu_object.options(3)

        elif selected == "Check your account balance":
            menu_object.options(5)

        #elif selected == "DELETE ACCOUNT":
        #    menu_object.options(4)
        
        elif selected == "Update account details":
            menu_object.options(6)

        elif selected == "Loan details":
            menu_object.options(7)
        
        elif selected == "Appointment":
            menu_object.options(8)


elif options == "employee":
    employee_id = st.number_input("Please enter your employee id")
    password = st.text_input("Please enter the password" , type="password")

    if not employee_id or not password:
        st.stop()

    cur.execute(f"SELECT password FROM employee_password where employee_id = {employee_id}")
    state = (password == cur.fetchall()[0][0])

    #login_state = st.button("Login")


    if not state:
        st.warning("Password is incorrect")
        st.stop()
    else:
        menu_object = menu(host=host,user=user,passwd=passwd,database=database)

        with st.sidebar:
            selected = option_menu(
                menu_title = "Main Menu",
                options = ["Cash" , "Transactions" , "Customers in a Branch" , "Loan approval" , "Loan payment" , "Report" , "Appointment" , "Delete Account"])
            
        if selected == "Cash":
            menu_object.options_employee(1)
        elif selected == "Customers in a Branch":
            menu_object.options_employee(2)
        elif selected == "Loan approval":
            menu_object.options_employee(3)
        elif selected == "Report":
            menu_object.options_employee(4)
        elif selected == "Appointment":
            menu_object.options_employee(5)
        elif selected == "Delete Account":
            menu_object.options_employee(6)
        elif selected == "Transactions":
            menu_object.options_employee(7)
        elif selected == "Loan payment":
            menu_object.options_employee(8)
