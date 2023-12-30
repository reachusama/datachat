from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate

llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:8010/",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)
template = """Instruction: {instruction}
Input: {input}
Output:"""
prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def main():
    instruction = """
    Write a code to add two numbers without using the \"+\" operator.
    """
    input = """
    num1 = 2
    num2 = 7
    """

    params = {
        "instruction": instruction.strip("\n"),
        "input": input.strip("\n")
    }
    result = chain.run(params)
    print(result)


if __name__ == "__main__":
    main()


def process_query(query, data):
    # Implement your query processing logic here
    # For now, it just echoes the query
    return f"Query: {query}\nData: {data.shape}"
