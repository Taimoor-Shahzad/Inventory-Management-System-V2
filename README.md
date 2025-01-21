# Inventory Management System (IMS) - Version 2

## Overview
The Inventory Management System (IMS) - Version 2 is an enhanced version of the original IMS. It features a modernized Streamlit interface, improved functionality, and better organization to streamline inventory management for small businesses. Key improvements include a redesigned sidebar, separate user and admin workflows, and enhanced user experience. The system is user-friendly and provides robust role-based access for administrators and regular users.

## Features

### *Role-Based Access Control*
#### Admin Role:
- Add new products to the inventory.
- Remove existing products.
- View all products with detailed information.
- Adjust stock levels dynamically.
- Access advanced features like viewing inventory analytics (planned future feature).

### *Product Management*
- Create, read, update, and delete products.
- Real-time stock adjustment.
- Persistent data storage in JSON files (inventory.json and users.json).

### *Streamlit Interface*
- Fully responsive and interactive web interface.
- Redesigned sidebar that dynamically updates based on user roles.
- Admin-specific dropdowns for inventory operations.
- Clean and minimalist design optimized for usability.

### *Error Handling*
- User-friendly error messages for invalid actions.
- Custom exceptions for authentication and inventory operations.

### *Data Persistence*
- User and product data are stored securely in JSON files (users.json, inventory.json).

### *Improved Logout Functionality*
- Simplified and intuitive logout button placement for all users.

## Setup and Installation

### *Installation Steps*
1. Clone the repository or download the project files.
2. Navigate to the project directory:
   bash
   cd "<Your_dir>"
   
3. Install required dependencies:
   bash
   pip install -r requirements.txt
   
4. Ensure the Data folder contains the following files:
   - inventory.json: Initialize with [] (empty list).
   - users.json: Initialize with {} (empty dictionary).

## How to Run

### *Running the Application*
1. Navigate to the project directory:
   bash
   cd "Inventory Management System"
   
2. Start the Streamlit application:
   bash
   streamlit run app.py
   
3. Open the URL provided by Streamlit (usually http://localhost:8501) in your web browser.

### *Default Credentials*
#### Admin Login:
- Username: admin
- Password: adminpass

## Using the Application

### *1. Login*
- Enter your username and password on the login screen.
- Based on your role, the respective dashboard (Admin/User) will load.

### *2. Admin Functionalities*
- *Add Product*: Enter product details (ID, name, category, price, stock) and click "Add Product".
- *Remove Product*: Select a product from the dropdown and click "Remove Product".
- *View Products*: Displays all products in a tabular format.
- *Adjust Stock*: Select a product, specify the adjustment (positive or negative), and click "Adjust Stock".

### *3. User Functionalities*
- *View Products*: Displays all available products.
- *Search Products*: Use the search bar to find products by name or category.

### *4. Logout*
- Use the "Logout" button in the sidebar to log out of the system.

## Technical Details

### **Backend (lms_core.py)**
- AuthenticationManager: Handles user authentication and registration.
- ProductManager: Manages inventory operations (add, remove, adjust stock).
- *Persistent Storage*: Data is stored in inventory.json and users.json.

### **Frontend (app.py)**
- Built with the Streamlit framework.
- Dynamic role-based views to load the appropriate dashboard for admin or user.

### *Error Handling*
- Custom exceptions like AuthenticationError, ProductNotFoundError, and InsufficientStockError ensure smooth operation and clear error messages.
