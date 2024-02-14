# app.py

import streamlit as st
from login import login_page
from user import user_dashboard
from admin import admin_dashboard

# ... (session state and redirection logic)

if st.session_state.logged_in:
    if st.session_state.user_role == "Admin":
        admin_dashboard()
    else:
        user_dashboard()
else:
    login_page()
