import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import E2BDataAnalysisTool

load_dotenv()
st.set_page_config(layout="wide")


def save_artifact(artifact):
    print("New matplotlib chart generated:", artifact.name)
    file = artifact.download()
    basename = os.path.basename(artifact.name)

    with open(f"./resources/outputs/{basename}", "wb") as f:
        f.write(file)


st.session_state.e2b_data_analysis_tool = E2BDataAnalysisTool(
    # on_stdout=lambda stdout: print("stdout:", stdout),
    # on_stderr=lambda stderr: print("stderr:", stderr),
    on_stdout=lambda stdout: st.session_state.responses.append(stdout),
    on_stderr=lambda stderr: st.session_state.responses.append(stderr),
    on_artifact=save_artifact,
)

tools = [st.session_state.e2b_data_analysis_tool.as_tool()]
llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = initialize_agent(
    tools,
    llm,
    name="Data Analyst",
    instructions="Your role is to act as a data analyst for non-technical people. You will assist users in understanding and interpreting data, focusing on simplicity and clarity. Avoid using overly technical jargon or complex statistical concepts unless specifically asked.",
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True,
)


def process_query(q):
    result = agent.run(
        q
        # "What is the median housing age for houses that have the top population? Create a visualisation using graph."
    )
    return result


def upload_file():
    pass


def main():
    st.title("Data Chat")

    # Sidebar for file upload and query input
    st.sidebar.title("Controls")
    # Initialize a session state to store responses
    if 'responses' not in st.session_state:
        st.session_state.responses = []

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "file_uploaded" not in st.session_state:
        st.session_state["file_uploaded"] = False

    # User query
    query = st.sidebar.text_area("Enter your query here:")
    query_warning_placeholder = st.sidebar.empty()

    # Submit btn
    submit_button = st.sidebar.button("Process Query")
    clear_session_button = st.sidebar.button("Clear Session")
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Uploaded file
    uploaded_file = st.sidebar.file_uploader("Upload a File",
                                             key=st.session_state["file_uploader_key"])

    # Load the file
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        if not st.session_state["file_uploaded"]:
            remote_path = st.session_state.e2b_data_analysis_tool.upload_file(
                file=uploaded_file,
                description=f"Data columns consist of {', '.join(list(data.columns))}",
            )

            print("UPLOADED FILE: ", remote_path)

        st.session_state["file_uploaded"] = True
        st.sidebar.success("File Uploaded Successfully!")
    else:
        data = pd.DataFrame()  # Empty DataFrame if no file is uploaded
        st.sidebar.warning("Please upload a file.")

    # Placeholder for responses
    response_container = st.empty()

    # Process and store the response
    if submit_button:
        if not query.strip():
            query_warning_placeholder.warning("Please enter a query.")
        else:
            response = process_query(query)
            st.session_state.responses.append(response)
            query_warning_placeholder.empty()

    if clear_session_button:
        print("I am here")
        st.session_state.e2b_data_analysis_tool.close()
        st.session_state["file_uploaded"] = False
        st.session_state["file_uploader_key"] += 1
        st.rerun()

    # Displaying all responses in an expander
    with response_container.container():
        if st.session_state.responses:
            for idx, response in enumerate(st.session_state.responses, 1):
                with st.expander(f"Response #{idx}", expanded=True):
                    st.write(response)


if __name__ == "__main__":
    main()
