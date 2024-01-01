from dotenv import load_dotenv
from io import StringIO
import streamlit as st
import pandas as pd
import os

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import E2BDataAnalysisTool
from langchain.callbacks import StreamlitCallbackHandler


# Function to save generated artifacts
def process_artifact(artifact):
    print("New matplotlib chart generated:", artifact.name)
    file = artifact.download()
    basename = os.path.basename(artifact.name)
    with open(f"./resources/outputs/{basename}", "wb") as f:
        f.write(file)


@st.cache_resource
def init_upload_sandbox(_data, _file):
    e2b_data_analysis_tool = E2BDataAnalysisTool(
        on_stdout=lambda stdout: print(stdout),
        on_stderr=lambda stderr: print(stderr),
        on_artifact=process_artifact,
    )

    csv_data = _data.to_csv(index=False)
    csv_file = StringIO(csv_data)
    csv_file.name = "user_data.csv"
    remote_path = e2b_data_analysis_tool.upload_file(
        file=csv_file,
        description=f"Data columns consist of {', '.join(list(_data.columns))}.",
    )

    print(remote_path)
    return e2b_data_analysis_tool


# Function to initialize the agent
@st.cache_resource
def init_agent():
    tools = [st.session_state.e2b_data_analysis_tool.as_tool()]
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    agent = initialize_agent(
        tools,
        llm,
        name="Data Analyst",
        instructions="Your role is to act as a data analyst for non-technical people...",
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent


# Function to initialize session state variables
def initialize_session_state():
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0


# Function to handle query submission
def handle_query_submission(submit_button, query, query_warning_placeholder):
    if submit_button:
        if not query.strip():
            query_warning_placeholder.warning("Please enter a query.")
        else:
            st_callback = StreamlitCallbackHandler(st.container())
            response = st.session_state.agent.run(query, callbacks=[st_callback])
            st.session_state.responses.append(response)
            query_warning_placeholder.empty()


# Function to handle session reset
def handle_session_reset(clear_session_button):
    if clear_session_button:
        print("Session reset initiated")
        st.session_state.e2b_data_analysis_tool.close()
        st.session_state["file_uploader_key"] += 1
        st.session_state.responses = []
        st.rerun()


# Function to display responses
def display_responses(response_container):
    with response_container.container():
        if st.session_state.responses:
            for idx, response in enumerate(st.session_state.responses, 1):
                with st.expander(f"Response #{idx}", expanded=True):
                    st.write(response)


# Main function
def main():
    st.title("Data Chat")

    # Sidebar for controls
    st.sidebar.title("Controls")
    initialize_session_state()

    query = st.sidebar.text_area("Enter your query here:")
    query_warning_placeholder = st.sidebar.empty()
    submit_button = st.sidebar.button("Process Query")
    clear_session_button = st.sidebar.button("Clear Session")

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload a File", key=st.session_state["file_uploader_key"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        # Initialize tools and agent

        st.session_state.e2b_data_analysis_tool = init_upload_sandbox(data, uploaded_file)
        st.session_state.agent = init_agent()
        st.sidebar.success("File Uploaded Successfully!")
    else:
        st.sidebar.warning("Please upload a file.")

    # Response container
    response_container = st.empty()

    # Process query
    handle_query_submission(submit_button, query, query_warning_placeholder)

    # Clear session
    handle_session_reset(clear_session_button)

    # Display responses
    display_responses(response_container)


if __name__ == "__main__":
    load_dotenv()
    st.set_page_config(layout="wide")
    main()
