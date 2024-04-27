# DataChat

Data Analysis with Natural Language Queries using GenAI & Streamlit

## Process

- User uploads dataset
- Get a user query
- Create chat-plan steps.
- For each:
    - Convert query into chat plan using LLMs, (query, dataset.shape/dataset.desc)
        - Instruction
            - What to do.
        - Input
            - What should be provided as input.
        - Output
            - What should be the output.
- Execute chat plan using LLMs.
- Show results

## Tools

- [Streamlit.io](https://blog.streamlit.io/)
- [LangChain](https://www.langchain.com/)
