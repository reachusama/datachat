from io import StringIO

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import E2BDataAnalysisTool

from utils import process_artifact, process_response


@st.cache_resource
def init_upload_sandbox(_data):
    e2b_data_analysis_tool = E2BDataAnalysisTool(
        on_stdout=lambda stdout: print(f"stdout: {stdout}"),
        on_stderr=lambda stderr: print(f"stderr: {stderr}"),
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


def initialize_session_state():
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0


def handle_query_submission(submit_button, query, query_warning_placeholder):
    if submit_button:
        if not query.strip():
            query_warning_placeholder.warning("Please enter a query.")
        else:
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(query)
                response = process_response(response)
                st.session_state.responses.append(response)
                query_warning_placeholder.empty()


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
                    for res in response:
                        if res["type"] == "text":
                            st.write(res["output"])
                        else:
                            st.image(res["output"])


# Main function
def main():
    st.title("Natural Data Analysis")

    # Sidebar for controls
    st.sidebar.title("Controls")
    initialize_session_state()

    query = st.sidebar.text_area("Enter your query here:")
    query_warning_placeholder = st.sidebar.empty()
    submit_button = st.sidebar.button("Process Query")
    clear_session_button = st.sidebar.button("Clear Session")

    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "Upload a File", key=st.session_state["file_uploader_key"]
    )

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)

        st.session_state.e2b_data_analysis_tool = init_upload_sandbox(data)
        st.session_state.agent = init_agent()
        st.sidebar.success("File Uploaded Successfully!")
    else:
        st.sidebar.warning("Please upload a file.")

    response_container = st.empty()
    handle_query_submission(submit_button, query, query_warning_placeholder)
    handle_session_reset(clear_session_button)
    display_responses(response_container)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    load_dotenv()
    main()
