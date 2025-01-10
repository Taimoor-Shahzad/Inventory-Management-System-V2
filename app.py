import streamlit as st
from lms_core import ProductManager, Product, Role, ProductNotFoundError, InsufficientStockError
from authentication import AuthenticationManager, AuthenticationError, AuthorizationError
import pandas as pd

# Initialize Managers
auth_manager = AuthenticationManager()
product_manager = ProductManager()

# Helper Function for Product Table
def display_products():
    products = product_manager.get_products()
    df = pd.DataFrame([
        {
            "Product ID": p.product_id,
            "Name": p.name,
            "Category": p.category,
            "Price": p.price,
            "Stock": p.stock_quantity,
        }
        for p in products
    ])
    st.dataframe(df)

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    menu = ["Add Product", "Remove Product", "View Products", "Adjust Stock"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    if choice == "Add Product":
        st.header("Add a New Product")
        product_id = st.number_input("Product ID", min_value=1, step=1)
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)

        if st.button("Add Product"):
            try:
                product = Product(product_id, name, category, price, stock)
                product_manager.add_product(product)
                st.success("Product added successfully!")
            except ValueError as e:
                st.error(str(e))

    elif choice == "Remove Product":
        st.header("Remove a Product")
        product_ids = [p.product_id for p in product_manager.get_products()]
        selected_id = st.selectbox("Select Product ID", product_ids)

        if st.button("Remove Product"):
            try:
                product_manager.remove_product(selected_id)
                st.success("Product removed successfully!")
            except ProductNotFoundError:
                st.error("Product not found.")

    elif choice == "View Products":
        st.header("All Products")
        display_products()

    elif choice == "Adjust Stock":
        st.header("Adjust Stock Levels")
        product_ids = [p.product_id for p in product_manager.get_products()]
        selected_id = st.selectbox("Select Product ID", product_ids)
        adjustment = st.number_input("Stock Adjustment (use negative for reduction)", step=1)

        if st.button("Adjust Stock"):
            try:
                product_manager.adjust_stock(selected_id, adjustment)
                st.success("Stock adjusted successfully!")
            except ProductNotFoundError:
                st.error("Product not found.")
            except InsufficientStockError as e:
                st.error(str(e))

# User Dashboard
def user_dashboard():
    st.title("User Dashboard")
    st.header("View Products")
    search = st.text_input("Search by Product Name or Category")

    products = product_manager.get_products()
    df = pd.DataFrame([
        {
            "Product ID": p.product_id,
            "Name": p.name,
            "Category": p.category,
            "Price": p.price,
            "Stock": p.stock_quantity,
        }
        for p in products
    ])

    if search:
        filtered_df = df[
            (df["Name"].str.contains(search, case=False)) |
            (df["Category"].str.contains(search, case=False))
        ]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)

# Registration Page
def register_page():
    st.title("Register New User")
    username = st.text_input("Username", key="reg_username", value="")
    password = st.text_input("Password", type="password", key="reg_password", value="")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password", value="")
    role = st.selectbox("Role", [Role.USER, Role.ADMIN])  # Optional for Admin Role

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                current_user_role = st.session_state.get("role", None)
                auth_manager.register_user(username, password, role, current_user_role)
                st.success("User registered successfully!")
            except Exception as e:
                st.error(str(e))

# Login Page
def login_page():
    st.title("Login")
    username = st.text_input("Username", key="login_username", value="")
    password = st.text_input("Password", type="password", key="login_password", value="")

    if st.button("Login"):
        try:
            user = auth_manager.authenticate_user(username, password)
            st.session_state.logged_in = True
            st.session_state.role = user.role
            st.success(f"Logged in as {user.role}")
        except Exception as e:
            st.error(str(e))

# Main Interface
def main():
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None

    st.sidebar.title("Inventory Management System")

    # Sidebar logic based on login state
    if not st.session_state.logged_in:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            login_page()
        elif choice == "Register":
            register_page()
    else:
        if st.session_state.role == Role.ADMIN:
            admin_dashboard()  # Admin functionality
        elif st.session_state.role == Role.USER:
            user_dashboard()  # User functionality

        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None

if __name__ == "__main__":
    main()
