from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import RobertaTokenizer, T5ForConditionalGeneration, pipeline


def get_huggingface_model(
        model_id="Salesforce/codet5-small",
        max_new_tokens=10,
        device="cpu"
):
    tokenizer = RobertaTokenizer.from_pretrained(model_id)
    model = T5ForConditionalGeneration.from_pretrained(model_id)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        trust_remote_code=True
    )
    hf = HuggingFacePipeline(pipeline=pipe)
    return hf


def main():
    hf = get_huggingface_model()
    template = """Instruction: {instruction}
    Input: {input}
    Output:"""
    prompt = PromptTemplate.from_template(template)

    chain = prompt | hf

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
    result = chain.invoke(params)
    print(result)


def process_query(query, data):
    # Implement your query processing logic here
    # For now, it just echoes the query
    return f"Query: {query}\nData: {data.shape}"


if __name__ == "__main__":
    main()
