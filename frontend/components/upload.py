import streamlit as st
import requests
import json
import os

API_URL = os.environ.get("API_URL", "http://localhost:8000/api/v1")

def db_connector_tab():
    st.subheader("Connect to Database")
    st.info("Supported: PostgreSQL, MongoDB, Snowflake")
    
    db_type = st.selectbox("Database Type", ["PostgreSQL", "Snowflake", "MongoDB (BI Connector)"])
    db_uri = st.text_input("Connection URI", type="password", placeholder="postgresql://user:pass@host:5432/db")
    
    if st.button("Connect"):
        if db_uri:
            st.session_state['db_uri'] = db_uri
            st.session_state['active_source'] = "db"
            st.session_state['file_path'] = None
            st.success(f"Connected to {db_type}!")
        else:
            st.error("Please enter a valid URI.")

def file_upload_tab():
    st.subheader("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        if st.button("Upload & Process"):
            with st.spinner("Sanitizing and pushing to secure server..."):
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                try:
                    res = requests.post(f"{API_URL}/upload", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state['file_path'] = data['file_path']
                        st.session_state['active_source'] = "file"
                        st.session_state['db_uri'] = None
                        st.success("File uploaded successfully!")
                        
                        # Generate Summary automatically on upload
                        st.info("Generating Executive Summary...")
                        sum_res = requests.post(f"{API_URL}/summary", json={"file_path": data['file_path']})
                        if sum_res.status_code == 200:
                            st.session_state['summary_data'] = sum_res.json()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")

def render_upload_section():
    st.sidebar.header("Data Source Setup")
    tab1, tab2 = st.sidebar.tabs(["File Upload", "Database"])
    with tab1:
        file_upload_tab()
    with tab2:
        db_connector_tab()
