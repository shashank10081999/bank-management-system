import streamlit as st
import  mysql.connector as connection
import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from constants import host , passwd , user , database 


class menu():
    def __init__(self ,host , user , passwd , database , customer_id=None):
        try:
            self.customer_id = customer_id    
            self.mydb = connection.connect(host  = host , user = user , passwd =passwd , database = database)
            self.cursor = self.mydb.cursor()
            self.mydb.autocommit = True
        
        except Exception as e:
            raise e
        
    def check_account_number(self):
         self.cursor.execute(f"select account_number from Accounts where customer_id = {self.customer_id}")
         data = self.cursor.fetchall()

         return data[0][0]
    
    def options(self , n):


        if n == 1:

            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.account_no = st.number_input("Please enter your account number")

            if not self.account_no:
                 st.stop()
            if self.account_no != self.check_account_number():
                 st.warning("Please check your account number")
                 st.stop()
                 

            self.cursor.execute(f"select * from Accounts where account_number = {int(self.account_no)}")

            data = self.cursor.fetchall()

            account_balance = data[0][3]

            if len(data) == 0:
                    print("Invalid Account Number")
                
            else:

                    options = st.selectbox("Please select the action" , ("with draw" , "add amount" , "account to account transfer"))


                    if options == "with draw" : 
                        with_draw_amount = int(st.number_input("Please enter the amount"))

                        if not with_draw_amount:
                             st.stop()

                        if with_draw_amount > account_balance:
                            st.write("your balance is low")
                        else:
                            st.write("Please collect your cash at the bank")

                            update_query = f"update Accounts set  balance= {account_balance - with_draw_amount}  where account_number={self.account_no}"

                            self.cursor.execute(update_query)

                            transactions_query = f"INSERT INTO Transactions\
                                (transaction_id , account_number , transaction_type , amount , transaction_date , description)\
                                VALUES ({random.randint(0,899999)} , {self.account_no} , 'international' , {with_draw_amount} , '%s' , 'nothing')\
                                " %(date_time)
                            self.cursor.execute(transactions_query)

                            withdarw_query = f"INSERT INTO withdraw \
                                               (withdraw_amount , withdraw_date , customer_id) values ({with_draw_amount} , '{datetime.now().strftime('%Y-%m-%d')}' , {self.customer_id})"
                            
                            self.cursor.execute(withdarw_query)

                            update = f"INSERT INTO updated_balance (account_number , updated_amount , updated_date) VALUES ({self.account_no}, {account_balance - with_draw_amount} , '{datetime.now().strftime('%Y-%m-%d')}')"

                            self.cursor.execute(update)

                            self.mydb.commit()

                    if options =="add amount":
                        amount2 = int(st.number_input("Pleae enter the amount you to add - "))

                        if not amount2:
                             st.stop()

                        add_update_query = f"update Accounts set   balance= {account_balance + amount2}  where account_number={self.account_no}"

                        self.cursor.execute(add_update_query)

                        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        transactions_query = f"INSERT INTO Transactions\
                                (transaction_id , account_number , transaction_type , amount , transaction_date , description)\
                                VALUES ({random.randint(0,899999)} , {self.account_no} , 'international' , {amount2} , '%s' , 'nothing')\
                                " % (date_time)
                        self.cursor.execute(transactions_query)

                        deposit_query = f"INSERT INTO deposit \
                                               (deposit_amount , despoit_date , customer_id) values ({amount2} , '{datetime.now().strftime('%Y-%m-%d')}' , {self.customer_id})"
                            
                        self.cursor.execute(deposit_query)

                        update = f"INSERT INTO updated_balance (account_number , updated_amount , updated_date) VALUES ({self.account_no}, {account_balance + amount2} , '{datetime.now().strftime('%Y-%m-%d')}')"

                        self.cursor.execute(update)

                        self.mydb.commit()

                        self.cursor.execute(f"select balance from Accounts where account_number={self.account_no}")

                        st.write(f"The Updated balance is {self.cursor.fetchall()[0][0]}")

                    if options == "account to account transfer": 

                        other_account_number = st.number_input("Please enter the number account number you want to send money to - " , value= 0)
                        amount3 = st.number_input("Please enter the amount you want to send - " , value=0)

                        if (not other_account_number) or (not amount3):
                             st.stop()

                        transactions_query = f"INSERT INTO Transactions\
                                (transaction_id , account_number , transaction_type , amount , transaction_date , description)\
                                VALUES ({random.randint(0,899999)} , {self.account_no} , 'international' , {amount3} , '%s' , 'Account to Account transfer') ,\
                                ({random.randint(0,899999)} , {other_account_number} , 'international' , {amount3} , '%s' , 'Account to Account transfer')" % (date_time ,date_time)
                        self.cursor.execute(transactions_query)

                        update_query1 = f"update Accounts set  balance= {account_balance - amount3}  where account_number={self.account_no}"

                        self.cursor.execute(update_query1)

                        self.cursor.execute(f"select * from Accounts where account_number = {other_account_number}")

                        other_account_amount = self.cursor.fetchall()[0][0]

                        update_query2 = f"update Accounts set  balance= {other_account_amount + amount3}  where account_number={other_account_number}"

                        self.cursor.execute(update_query2)

                        transfer_query = f"INSERT INTO NEFT_RTGS_Transfer \
                                               (transfer_type , transfer_date, transfer_amount , customer_id) values ('National' , '{datetime.now().strftime('%Y-%m-%d')}' , {amount3} , {self.customer_id})"
                            
                        self.cursor.execute(transfer_query)

                        update = f"INSERT INTO updated_balance (account_number , updated_amount , updated_date) VALUES ({self.account_no}, {account_balance + amount2} , '{datetime.now().strftime('%Y-%m-%d')}')"

                        self.cursor.execute(update)

                        

                        self.mydb.commit()

                        self.cursor.execute(f"select balance from Accounts where account_number={self.account_no}")

                        st.write(f"The Updated balance is {self.cursor.fetchall()[0][0]}")

 

        if n == 2:

                details_query = f"select * from customers where customer_id = {self.customer_id}"
                self.cursor.execute(details_query)
                data = self.cursor.fetchall()
                if len(data) == 0:
                    st.write("Account doesnot exist")
                else:

                    details = ["customer_id" , "customer_name" , "address" , "city" , "phone"]
                    for i , j in zip(details , data[0]):
                        st.write(i + " - " + str(j))


        if n ==3 :
                transactions = f"select * from Transactions where account_number in (select account_number from Accounts where customer_id = {self.customer_id})"

                self.cursor.execute(transactions)
                data= self.cursor.fetchall()


                if len(data) == 0 :
                    print("No Transactions")
                else:
                   transactions_details = ["transaction_id" , "account_number" , "transaction_type" , "amount" , "transaction_date" , "description"]
                       
                   df = pd.DataFrame(data , columns=transactions_details)

                   st.table(df)
                   
                         

        if n == 5:
                balance_query = f"SELECT balance FROM Accounts where customer_id = {self.customer_id}"
                self.cursor.execute(balance_query)
                data = self.cursor.fetchall()
                st.write(f"Balance - {data[0][0]}")

        if n == 6 :

                updated_name = st.text_input("Please enter the new name - ")
                updated_address = st.text_input("Please enter the updated address - ")
                updated_city = st.text_input("Please enter the updated city - ")
                updated_phone = st.text_input("Please enter the updated phone - ")

                if not updated_name or not updated_address or not updated_city or not updated_phone:
                     st.stop()

                self.cursor.execute(f"Update customers set customer_name = '%s' , address = '%s' , city = '%s',\
                                    phone = '%s' where customer_id = {self.customer_id}" % (updated_name , updated_address , updated_city , updated_phone))
                
                updated_details_query = f"select * from customers where customer_id = {self.customer_id}"
                self.cursor.execute(updated_details_query)
                data = self.cursor.fetchall()
                
                st.write("UPDATED DETAILS - ")
                details = ["customer_id" , "customer_name" , "address" , "city" , "phone"]
                for i , j in zip(details , data[0]):
                    st.write(i + " - " + str(j))


        if n == 7 :

                self.cursor.execute(f"select * from Loans where customer_id = {self.customer_id}")

                data = self.cursor.fetchall()

                if len(data) > 0:
                    df = pd.DataFrame(data , columns=["Loan id" , "Customer_id" , "amount" , "rate" , "start date" , "end date"])
                    
                    st.table(df)
                else:
                    st.write("You dont have any loans")

        if n==8 :

             appointment_date = st.date_input("Please enter the day for which you what to book the appointement")

             appointment_time = st.time_input("Please enter the time of appointment")

             if not appointment_date or not appointment_time:
                  st.stop()
                
             details_query = f"select * from customers where customer_id = {self.customer_id}"

             self.cursor.execute(details_query)
             data = self.cursor.fetchall()


             self.cursor.execute(f"INSERT INTO appointment (appointment_date , appointment_time , customer_id , customer_name) VALUES ('%s' , '%s' , {self.customer_id} , '{data[0][1]}')"%(appointment_date , appointment_time))

             st.write(f"Your appointment is book on {appointment_date}")
                  



    def options_employee(self , n):
         
        if n==1 :
            # cash credit 
            account_number = st.number_input("enter the account number")

            if not account_number:
                 st.stop()

            self.cursor.execute(f"select * from Accounts where account_number = {int(account_number)}")

            data = self.cursor.fetchall()

            account_balance = data[0][3]

            if len(data) ==  0:
                st.warning("Account is incorrect")
                st.stop()


            amount2 = int(st.number_input("Pleae enter the amount you to add - "))

            if not amount2:
                    st.stop()

            add_update_query = f"update Accounts set   balance= {account_balance + amount2}  where account_number={account_number}"

            self.cursor.execute(add_update_query)

            self.mydb.commit()

            st.write(f"Updated Balance - {account_balance + amount2}")
        
        if n ==2:
            branch_id = st.number_input("Enter the branch id")
            self.cursor.execute(f"select * from Accounts where branch_id={branch_id}")

            data = self.cursor.fetchall()

            df = pd.DataFrame(data , columns=["account_number" , "customer_id" , "account_type" , "balance" , "branch_id"])

            st.table(df)

        if n==3:
            # loan approval 
            customer_id = st.number_input("Please the customer number for who you approved the loan")
            amount = st.number_input("Please the loan amount")
            interset_rate = st.number_input("Enter the rate of interset")
            start_date = st.date_input("Please enter the strat date")
            end_date = st.date_input("Please enter the end date of the loan")


            if not customer_id or not amount or not interset_rate:
                 st.stop()

            if start_date != end_date:
                self.cursor.execute(f"INSERT INTO Loans (customer_id , amount , interest_rate ,start_date ,end_date)\
                                VALUES ({customer_id} , {amount} , {interset_rate} , '%s' , '%s')" % (start_date, end_date))
            
                st.write("Loan tabel is update")
            
                self.mydb.commit()

            
        if n==4 :
            st.write("Report")
            self.cursor.execute("select sum(amount) from Transactions where transaction_type =  'international'")

            internation = self.cursor.fetchall()[0][0]

            self.cursor.execute("select sum(amount) from Transactions where transaction_type =  'national'")

            nation = self.cursor.fetchall()[0][0]

            df = pd.DataFrame([(internation , "International") , (nation , "National")] , columns = ["total sum", "type"])

            fig, ax = plt.subplots()

            ax.bar(df["type"] , df["total sum"])
            plt.title("Total amount in international Transactions vs national Transactions")

            st.pyplot(fig)

        if n==5 :
             self.cursor.execute("select * from appointment")
             data = self.cursor.fetchall()

             df = pd.DataFrame(data , columns = ["Appointment_ID" , "Customer_ID" , "Customer_Name" , "Appointment_Date" , "Appointment_Time"])

             st.write('Appointments: '+"\n")

             for i in data :
                for j, k in zip(["Appointment_ID" , "Customer_ID" , "Customer_Name" , "Appointment_Date" , "Appointment_Time"] , i):
                     st.write(j + "-"+ str(k))
                st.write("*********************************")

        if n==6:
             
             customer_id = st.number_input("Please enter the customer id")

             if not customer_id:
                  st.stop()

             self.cursor.execute(f"select balance from Accounts where customer_id = {customer_id}")

             data = self.cursor.fetchall()      
             st.write("Balance - ", data[0][0])
             self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")
             self.cursor.execute("delete from Accounts where customer_id="+str(customer_id))
             self.cursor.execute('delete from Customers where customer_id='+str(customer_id))
             st.write('ACCOUNT DELETED SUCCESFULLY')

        if n==7 :
             st.write("Withdraws: - ")

             self.cursor.execute("select * from withdraw")

             withdraw_data = self.cursor.fetchall()

             withdraw_details = ["withdraw_id" , "withdraw_amount" , "withdraw_date" , "customer_id"]

             withdraw_df = pd.DataFrame(withdraw_data , columns=withdraw_details)

             st.table(withdraw_df)


             st.write("Deposit: - ")

             self.cursor.execute("select * from deposit")

             deposit_data = self.cursor.fetchall()

             deposit_details = ["deposit_id" , "deposit_amount" , "deposit_date" , "customer_id"]

             deposit_df = pd.DataFrame(deposit_data , columns=deposit_details)

             st.table(deposit_df)

             st.write("NEFT RTGS Transfer: - ")

             self.cursor.execute("select * from neft_rtgs_transfer")

             neft_rtgs_transfer_data = self.cursor.fetchall()

             neft_rtgs_transfer_data_details = ["transfer_id" , "transfer_type" , "transfer_date" , "customer_id" , "transfer_amount"]

             neft_rtgs_transfer_data_df = pd.DataFrame(neft_rtgs_transfer_data , columns=neft_rtgs_transfer_data_details)

             st.table(neft_rtgs_transfer_data_df)

        if n ==8 :
             st.write("Loan payment details")

             loan_payment_details = ["payment id", "payment_amount","payment_date","customer_id"]

             self.cursor.execute("select * from loan_payment")

             data = self.cursor.fetchall()

             df = pd.DataFrame(data, columns = loan_payment_details)

             st.table(df)






             





    


         





