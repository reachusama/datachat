# DataChat

An open-source software for data analysis using natural language queries.

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
- Create code to execute query
- Execute the query
- Show results

## LLMs Deployment

- [LC x HF Text Generation](https://python.langchain.com/docs/integrations/llms/huggingface_textgen_inference)
- [Hugging Face Text Generation](https://github.com/huggingface/text-generation-inference)

```angular2html

model=tiiuae/falcon-7b-instruct
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run

docker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.3 --model-id $model
```