import streamlit as st
from components.upload import render_upload_section
from components.chat import render_chat_interface

# Set Page Config
st.set_page_config(page_title="AI Data Analyst", layout="wide", page_icon="📊")

# Custom CSS for Premium Design
st.markdown("""
<style>
    .reportview-container {
        background: #121212;
    }
    .sidebar .sidebar-content {
        background: #1a1a1a;
    }
    h1, h2, h3 {
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    /* Buttons */
    .stButton>button {
        background-color: #2e6bfa;
        color: white;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1a51d4;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Industrial AI Data Analyst")

# Initialize session states
if 'active_source' not in st.session_state:
    st.session_state['active_source'] = None
if 'summary_data' not in st.session_state:
    st.session_state['summary_data'] = None

# Sidebar Upload & Connection
render_upload_section()

# Main Workspace Tabs
tab_summary, tab_query = st.tabs(["Executive Summary", "Dynamic Query Chat"])

with tab_summary:
    if st.session_state['summary_data']:
        st.subheader("Autonomous Insights")
        st.write(st.session_state['summary_data']['summary'])
        
        # Add basic visual (Stubbed, Plotly can go here based on data)
        # Using Streamlit metrics as an aesthetic placeholder
        col1, col2, col3 = st.columns(3)
        col1.metric("Status", "Analyzed")
        col2.metric("Data Quality", "High")
        col3.metric("Insights", "Ready")
        
        # PDF Export Button logic
        # In a real app we'd fetch the file bytes from backend
        st.success("PDF generated successfully by the agent backend.")
        st.markdown(f"**Export path on server:** `{st.session_state['summary_data']['pdf_path']}`")
    else:
        st.info("Upload a file or connect to a database to generate insights.")

with tab_query:
    render_chat_interface()
