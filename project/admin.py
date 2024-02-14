import streamlit as st
import db  # Import the database connection functions from db.py
from queries import update_data, delete_data  # Import data update and deletion functions from queries.py

def admin_dashboard():
    st.title("IPL Data Analysis Dashboard - Admin")

    st.sidebar.title("Admin Menu")

    # Admin actions
    admin_action = st.sidebar.radio("Select Admin Action", ["Update Data", "Delete Data"])

    if admin_action == "Update Data":
        update_data_button()
    elif admin_action == "Delete Data":
        delete_data_button()

def update_data_button():
    st.subheader("Update Data")

    # Create form elements to update data
    update_type = st.selectbox("Select Update Type", ["Update Team", "Update Match", "Update Player"])
    if update_type == "Update Team":
        # Create input fields for updating team data (e.g., name, wins, etc.)
        team_name = st.text_input("Team Name")
        team_wins = st.number_input("Wins")
        # Add more input fields for other attributes

        if st.button("Update Team"):
            connection = db.create_db_connection()
            if connection:
                # Call the data update function from queries.py to update team data
                success = update_data(connection, "team", team_name, team_wins)  # Pass the required data
                connection.close()
                if success:
                    st.success("Team data updated successfully!")
                else:
                    st.error("Failed to update team data. Please try again later.")
            else:
                st.error("Unable to connect to the database. Please try again later.")

    # Implement similar code for updating matches and players

def delete_data_button():
    st.subheader("Delete Data")

    # Create form elements to delete data (e.g., team, match, player)
    delete_type = st.selectbox("Select Delete Type", ["Delete Team", "Delete Match", "Delete Player"])
    if delete_type == "Delete Team":
        # Create input fields for deleting team data (e.g., team name)
        team_name = st.text_input("Team Name")

        if st.button("Delete Team"):
            connection = db.create_db_connection()
            if connection:
                # Call the data deletion function from queries.py to delete team data
                success = delete_data(connection, "team", team_name)  # Pass the required data
                connection.close()
                if success:
                    st.success("Team data deleted successfully!")
                else:
                    st.error("Failed to delete team data. Please try again later.")
            else:
                st.error("Unable to connect to the database. Please try again later.")

    # Implement similar code for deleting matches and players

def main():
    admin_dashboard()

if __name__ == "__main__":
    main()
