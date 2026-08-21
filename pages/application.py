import streamlit as st
from db.queries import get_all_applications, update_application, add_application, delete_application
from db.database import STATUS_ORDER
st.title("Applications")

@st.cache_data
def load_data():
    return get_all_applications()

df = load_data()

# --- sidebar filters ---
st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect("Status", options=STATUS_ORDER, default='Applied')
company_search = st.sidebar.text_input("Search company")

filtered = df.copy()
if status_filter:
    filtered = filtered[df['status'].isin(status_filter)]
if company_search:
    filtered = filtered[filtered["company"].str.contains(company_search, case=False, na=False)]

