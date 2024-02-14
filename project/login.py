import streamlit as st
import psycopg2

# Database connection parameters
dbname = "your_database_name"
user = "your_database_user"
db_password = "your_database_password"
host = "your_database_host"

# Define user_login and admin_login functions
def user_login(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        valid = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return valid
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def admin_login(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        valid = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return valid
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Define the registration function
def register_user(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Define your pages as functions
def home_page(user_role):
    st.title("Home Page")
    st.write(f"Welcome to the {user_role} dashboard!")

def admin_dashboard():
    st.title("Admin Dashboard")
    st.write("Welcome to the admin dashboard!")

def user_dashboard():
    st.title("User Dashboard")
    st.write("Welcome to the user dashboard!")

def login_page():
    st.title("Login Page")

    # Cricket animation
    st.markdown(
        """
        <div style="text-align:center">
        <img src="https://media.giphy.com/media/3orieTBvHtsMSEjmUQ/giphy.gif" alt="Cricket" width="300">
        </div>
        """
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["User", "Admin"])

    if st.button("Log In"):
        if role == "Admin":
            if admin_login(username, password):
                st.session_state.logged_in = True
                st.session_state.user_role = "Admin"
                st.success("Admin login successful! Redirecting to Admin Dashboard...")
            else:
                st.error("Invalid admin credentials. Please try again.")
        elif role == "User":
            if user_login(username, password):
                st.session_state.logged_in = True
                st.session_state.user_role = "User"
                st.success("User login successful! Redirecting to User Dashboard...")
            else:
                st.error("Invalid user credentials. Please try again.")
    
    # User Registration
    st.write("New User? Register Here:")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if role == "User":
            if register_user(new_username, new_password):
                st.success("User registration successful! You can now log in.")
                st.session_state.logged_in = True
                st.session_state.user_role = "User"
            else:
                st.error("Failed to register user. Please try again.")

# Initialize the session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

# Render the appropriate page based on the user's role
if st.session_state.logged_in:
    if st.session_state.user_role == "Admin":
        admin_dashboard()
    else:
        user_dashboard()
else:
    login_page()
