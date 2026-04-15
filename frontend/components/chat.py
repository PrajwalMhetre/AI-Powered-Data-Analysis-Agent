import streamlit as st
import requests
import os

API_URL = os.environ.get("API_URL", "http://localhost:8000/api/v1")

def render_chat_interface():
    st.subheader("Dynamic Query System")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                payload = {"query": prompt}
                if st.session_state.get('active_source') == 'file':
                    payload['file_path'] = st.session_state['file_path']
                elif st.session_state.get('active_source') == 'db':
                    payload['db_uri'] = st.session_state['db_uri']
                else:
                    st.error("Please connect a data source first in the sidebar.")
                    return
                    
                try:
                    res = requests.post(f"{API_URL}/query", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        response_text = data.get("result", "No output.")
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    else:
                        st.error(str(res.json()))
                except Exception as e:
                    st.error(f"Error calling API: {str(e)}")
