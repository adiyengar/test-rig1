"""Main entry point - auto-redirects to Index Management Tool."""
import streamlit as st

st.set_page_config(
    page_title="Index Management Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-redirect to Index Management Tool
st.switch_page("pages/1_Index_Management_Tool.py")
