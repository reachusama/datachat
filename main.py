import streamlit as st
import pandas as pd
from src.query import process_query

st.set_page_config(layout="wide")


def main():
    st.title("Data Chat")

    # Sidebar for file upload and query input
    st.sidebar.title("Controls")

    # User query
    query = st.sidebar.text_area("Enter your query here:")
    query_warning_placeholder = st.sidebar.empty()

    # Submit btn
    submit_button = st.sidebar.button("Process Query")
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Uploaded file
    uploaded_file = st.sidebar.file_uploader("Upload a File")

    # Load the file
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        st.sidebar.success("File Uploaded Successfully!")
    else:
        data = pd.DataFrame()  # Empty DataFrame if no file is uploaded
        st.sidebar.warning("Please upload a file.")

    # Initialize a session state to store responses
    if 'responses' not in st.session_state:
        st.session_state.responses = []

    # Placeholder for responses
    response_container = st.empty()

    # Process and store the response
    if submit_button:
        if not query.strip():
            query_warning_placeholder.warning("Please enter a query.")
        else:
            response = process_query(query, data)
            st.session_state.responses.append(response)
            query_warning_placeholder.empty()

    # Displaying all responses in an expander
    with response_container.container():
        if st.session_state.responses:
            for idx, response in enumerate(st.session_state.responses, 1):
                with st.expander(f"Response #{idx}", expanded=True):
                    st.write(response)


if __name__ == "__main__":
    main()
