# DataChat

Data Analysis with Natural Language Queries using GenAI & Streamlit

## Code Large Language Models

- [Salesforce CodeT5](https://github.com/salesforce/CodeT5/)
- [Why Salesforce](https://arxiv.org/pdf/2305.07922.pdf)
- Instruct Code T5+, Embeddings Code T5 +

### Results

![Alt Text](./resources/llms/results.png)

## Tools

- [Streamlit.io](https://blog.streamlit.io/)
- [LangChain](https://www.langchain.com/)

## Planning

- User uploads dataset
- Get a user query
- Convert query into chat plan using LLMs.
    - Instruction
        - What to do.
    - Input
        - What should be provided as input.
    - Output
        - What should be the output.
- Use chat plan using LLMs.
- Execute the query
- Show results

## LLMs Deployment

- [LC x HF Text Generation](https://python.langchain.com/docs/integrations/llms/huggingface_textgen_inference)
- [Hugging Face CodeT5p-16B](https://huggingface.co/Salesforce/instructcodet5p-16b)


- https://huggingface.co/docs/text-generation-inference/installation
- https://huggingface.co/blog/inference-endpoints-llm

## Next steps

- Deploy a custom LLM on Huggingface
- https://ui.endpoints.huggingface.co/reachusama/endpoints
- Use deployed model to build the repository