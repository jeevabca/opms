import streamlit as st
import mysql.connector
#from tabulate import tabulate
from streamlit_option_menu import option_menu
from PIL import Image

# Open a database connection
con = mysql.connector.connect(host="localhost", user="root", password="Zyjeev@09", database="new_db")
res = con.cursor()

cus_option=""
emp_option=""

def get_customer():
    qry = "select customer_id from customer"
    res.execute(qry)
    result = res.fetchall()
    list_of_ids = []
    for i in result:
        list_of_ids.append(i[0])
    return list_of_ids

def get_order(customer_id):
   # customer_id = st.number_input("enter the customer_id",step=1, value=101)
    qry = "select order_id from orders where customer_id = %s"
    val = (customer_id,)
    res.execute(qry,val)
    result = res.fetchall()
    list_of_order = []
    for i in result:
        list_of_order.append(i[0])
    return list_of_order

def get_emp_password():
    qry = "select password_ from employee"
    res.execute(qry)
    result = res.fetchall()
    list_of_password = []
    for i in result:
        list_of_password.append(i[0])
    return list_of_password

def get_employee():
    qry = "select employee_id from employee"
    res.execute(qry)
    result = res.fetchall()
    list_of_ids = []
    for i in result:
        list_of_ids.append(i[0])
    return list_of_ids

def customer_signup():
        st.markdown("*Customer Signup*")
        user = st.selectbox("Enter the option",["None","Register","Login"])
        if user =="Register":
            global first_name
            first_name = st.text_input("*Enter your name:*",placeholder="Enter your name")
            city = st.text_input("*Enter the City*",placeholder="Enter your city")
            state = st.text_input("*Enter the State*",placeholder="Enter your state")
            def custo_id():
                global customer_id 
                customer_id=100
                qry="select customer_id from customer order by customer_id desc limit 1" 
                res.execute(qry) 
                st_result=res.fetchone() 
                if st_result==None: 
                    customer_id =customer_id+1
                    print("**Your Customer ID is:**",customer_id )
                    return customer_id
                else: 
                    customer_id =st_result[0]+1
                    st.write("**Your Customer ID is:**",customer_id )
                    return customer_id
    
            if st.button("Submit"):
                customer_id = custo_id()
                qry = "insert into customer values (%s,%s,%s,%s)"
                val = (customer_id,first_name,city,state)
                res.execute(qry,val)
                con.commit()
                st.success("*Registered succesfully*")
        elif user=="Login":
            customer_login()
        else:
            st.write("Do yo want to register or login")


    
# Define your Streamlit app
def customer_login():
    st.markdown("*Customer Login*")
    customer_id = st.number_input("Enter the customer_id",step=1, value=101)
    cust_list = get_customer()


    if customer_id in cust_list:
        st.success("Login successful!")
        st.markdown("*Select an option*")
        user = st.selectbox("", ["None","View Booking", "New Booking", "Cancel Booking"])

        if user == "View Booking":
            qry = "select * from orders where customer_id = %s"
            val = (customer_id,)
            res.execute(qry, val)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
            # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)    

        elif user == "New Booking":
            qry = "select productname, price from product"
            res.execute(qry)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
            # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)
                
            def order_id():
                global order_id 
                order_id=1000 
                qry="select order_id from orders order by order_id desc limit 1" 
                res.execute(qry) 
                st_result=res.fetchone() 
                if st_result==None: 
                    order_id =order_id+1
                    st.write("Your order id is:",order_id )
                    return order_id
                else: 
                    order_id =int(st_result[0])+1
                    st.write("Your order id is:",order_id )
                    return order_id

            productname = st.text_input("*Enter the product name*")
            quantity = st.number_input("*Enter the quantity*",step=1, value=0)
            new_order_id = order_id()  # Assuming you have an order_id function

            if st.button("Submit"):
            
                qry = "select price from product where productname = %s"
                res.execute(qry, (productname,))
                price_res = res.fetchone()
                price_res = price_res[0]
                total_amount = quantity * price_res
                    

                try:
                    qry = "insert into orders values (%s, %s, %s, %s, %s, %s)"
                    val = (new_order_id, customer_id, productname, price_res, quantity, total_amount)
                    res.execute(qry, val)
                    con.commit()
                    st.success("*Order placed successfully*")
                except Exception as e:
                    st.error("*Something went wrong*")

                else:
                    qry = "select quantity from product where productname = %s"
                    val = (productname,)
                    res.execute(qry, val)
                    st_result = res.fetchone()
                    stock = st_result[0]
                    if stock < quantity:
                        st.warning("Out of stock")
                    else:
                        cur_stock = stock - quantity
                        qry = "update product set quantity = %s where productname = %s"
                        val = (cur_stock, productname)
                        res.execute(qry, val)
                        con.commit()

        elif user == "Cancel Booking":
            customer_id = st.number_input("enter the customer_id", step=1, value=101)

            qry = "select * from orders where customer_id = %s"
            val = (customer_id,)
            res.execute(qry, val)
            result = res.fetchall()
            st.table(result)

            cust_ord_list = get_order(customer_id)
            order_id = st.number_input("Enter the OrderId",step=1, value=1001)
            
            if st.button("Submit"):

                if order_id in cust_ord_list:
                    qry = "select quantity from orders where order_id = %s"
                    val = (order_id,)
                    res.execute(qry, val)
                    cn_qnt = res.fetchone()
                    cn_qnt = cn_qnt[0]

                    qry = "select product_name from orders where order_id = %s"
                    val = (order_id,)
                    res.execute(qry, val)
                    cn_pro = res.fetchone()
                    cn_pro = cn_pro[0]

                    qry = "delete from orders where order_id = %s"
                    val = (order_id,)
                    res.execute(qry, val)
                    con.commit()

                    qry = "update product set quantity = %s where productname = %s"
                    val = (cn_qnt, cn_pro)
                    res.execute(qry, val)
                    con.commit()

                    st.success("*Order Cancelled*")
            else:
                st.write("Enter the details")

        else:
            st.write("Booking options")

            
    else:
        st.write("Enter the valid customer id")

def emp_id():
    global employee_id
    employee_id=100
    qry="select employee_id from employee order by employee_id desc limit 1"
    res.execute(qry)
    st_result=res.fetchone()
    if st_result==None:
        employee_id=employee_id+1
        st.write("Your Employee ID is:",employee_id)
        return employee_id
    else:
        employee_id = st_result[0] + 1
        st.write("Your Employee ID is:", employee_id)
        return employee_id
def employee_signup():
    st.title("*Product Management Menu*")
    st.markdown("*Employee Signup*")
    emp_e = st.selectbox("Select the options", ["None","Register", "Login"], key="emp_e")  # Unique key for each iteration
    if emp_e == "Register":
        name, password = st.columns(2)
        first_name = name.text_input("Enter your name")
        password_input = password.text_input("Enter the password", type="password")
        if st.button("Register"):
            employee_id = emp_id()
            qry = "INSERT INTO employee (employee_id, firstname, password_) VALUES (%s, %s, %s)"
            val = (employee_id, first_name, password_input)
            res.execute(qry, val)
            con.commit()
            st.success("*Registered successfully*")
    elif emp_e == "Login":
        employee_login()
    else:
        st.write("Do you want to Register or Login")

def employee_login():
    st.markdown("*Employee Login*")

    id_,password = st.columns(2)
    employee_id = id_.number_input("Enter the Employee ID",step=1, value=101)
    password_ = password.text_input("Enter the password", type="password")
    
    qry = "SELECT employee_id FROM employee where employee_id=%s and password_=%s"
    val=(employee_id,password_)
    res.execute(qry,val)
    result = res.fetchone()
    if result == None:
        st.write("Enter the Required Details")
    else:
        st.success("Login Successfully")

        emp_option=st.selectbox("Product Management",["Add Product","Add Quantity","Delete Quantity","Delete Product","View Product"]) 
                
        if emp_option == "Add Product":
            productname=st.text_input("Enter the product name:") 
            price=st.number_input("Enter the price:",step=1, value=0)
            quantity=st.number_input("Enter the quantity:",step=1, value=0)
            if st.button("Add Product"):
                def pro_id():
                    global product_id 
                    product_id=100 
                    qry="select product_id from product order by product_id desc limit 1" 
                    res.execute(qry) 
                    st_result=res.fetchone() 
                    if st_result==None: 
                        product_id=product_id +1
                        st.write(productname,"Product ID is:",product_id)
                        return product_id
                    else: 
                        product_id=int(st_result[0])+1
                        st.write(productname,"Product ID is:",product_id)
                        return product_id
                product_id=pro_id()
                    
                qry="insert into product values (%s,%s,%s,%s)" 
                val=(product_id,productname,price,quantity) 
                res.execute(qry,val) 
                con.commit() 
                st.success("Product added successfully")     

        elif emp_option == "Add Quantity":
            qry = "select * from product"
            res.execute(qry)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
                # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)

            productname=st.text_input("Enter the product name:") 
            cn_quantity=st.number_input("Enter the quantity:",step=1, value=0)

            if st.button("Add Quantity"):
                qry="select quantity from product where productname=%s" 
                val=(productname,) 
                res.execute(qry,val) 
                st_result=res.fetchone() 
                quantity=st_result[0]+cn_quantity 
                qry="update product set quantity=%s where productname=%s" 
                val=(quantity,productname) 
                res.execute(qry,val) 
                con.commit() 
                st.success("Quantity updated successfully") 

        elif emp_option == "Delete Quantity":
            qry = "select * from product"
            res.execute(qry)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
                # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)

            productname=st.text_input("Enter the product name:") 
            cn_quantity=st.number_input("Enter the quantity:",step=1, value=0)

            if st.button("Delete Quantity"):
                qry="select quantity from product where productname=%s" 
                val=(productname,) 
                res.execute(qry,val) 
                st_result=res.fetchone() 
                quantity=st_result[0]-cn_quantity 
                qry="update product set quantity=%s where productname=%s" 
                val=(quantity, productname) 
                res.execute(qry,val) 
                con.commit() 
                st.write("quantity deleted successfully") 
            
        elif emp_option == "Delete Product":
            qry = "select * from product"
            res.execute(qry)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
                # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)   

            productname=st.text_input("Enter the product name:") 
            
            choice=st.radio("are you sure you want to delete this product yes/no:",["yes","no"]) 
            if choice=="yes":
                qry="delete from product where productname=%s" 
                val=(productname,) 
                res.execute(qry,val) 
                con.commit() 
                st.write(productname,"Deleted successfully")
            else:
                st.write("Deletion cancelled successfully")
                
        elif emp_option == "View Product":
            qry = "select * from product"
            res.execute(qry)
            result = res.fetchall()
            table_headings = [desc[0] for desc in res.description]
                # Create a list that includes the headings as the first row
            table_data = [table_headings] + result
            st.table(table_data)
        else:
            st.write("Select the options")

st.sidebar.title("Electronic gadget online_store")

with st.sidebar:
    selected = option_menu("Main Menu", ["Home page","Employee","Customer"])
    if selected == "Customer":
        st.sidebar.title("Customer")
        cus_option = option_menu("", ["Signup", "Login"])
    elif selected == "Employee":
        st.sidebar.title("Employee")
        emp_option = option_menu("", ["Signup", "Login"])
    
if selected=="Home page":
    st.title("Welcome to My Online Store")
    st.header("Discover a World of Products")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("*At our online store, we bring you a world of cutting-edge technology and innovative electronic gadgets that make life more convenient, enjoyable, and connected. Explore our extensive selection of gadgets designed to enhance your daily routines, entertain you, and keep you on the forefront of technological advancements.*")
    # Display the image in the first column
    with col2:
        st.image('images/electronic gadget.jpg', caption='Image Caption', use_column_width=True)

    st.header("Customer Reviews")
    st.subheader("What our customers are saying")
    st.write("⭐⭐⭐⭐⭐ - 'I love this store! Great products and fast shipping.'")
    st.write("⭐⭐⭐⭐ - 'Good quality products at affordable prices.'")
    st.write("⭐⭐⭐⭐⭐ - 'Excellent customer service and a wide selection of items.'")

    st.markdown("---")
    st.write("© 2023 My Online Store. All rights reserved.")

if cus_option=="Signup":
    col1, col2 = st.columns((6,1))

    with col1:
       st.title("*Electronic Gadget Online Store*")
    # Display the image in the first column
    with col2:
        st.image('images/electronic gadget.jpg', width=100)

    customer_signup()
elif cus_option=="Login":
    col1, col2 = st.columns((6,1))

    with col1:
       st.title("*Electronic Gadget Online Store*")
    # Display the image in the first column
    with col2:
        st.image('images/electronic gadget.jpg', width=100)
    customer_login()

if emp_option == "Signup":
    col1, col2 = st.columns((6,1))

    with col1:
       st.title("*Electronic Gadget Online Store*")
    # Display the image in the first column
    with col2:
        st.image('images/electronic gadget.jpg', width=100)
    employee_signup()
elif emp_option == "Login":
    col1, col2 = st.columns((6,1))

    with col1:
       st.title("*Electronic Gadget Online Store*")
    # Display the image in the first column
    with col2:
        st.image('images/electronic gadget.jpg', width=100)
    st.title("*Product Management Menu*")
    employee_login()