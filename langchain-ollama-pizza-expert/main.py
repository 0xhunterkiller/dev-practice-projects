from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from tts import say

model = OllamaLLM(model="gemma3:1b")

template = """
You are an expert in answering questions about a pizza restaurant. Response should be in plaintext.

Here are some relevant reviews: {reviews}

Here is a question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model 

while True:
    print("\n\n" +"-"*50)
    question = input("Ask your question (q to quit): ")
    if question.strip().lower() == "q":
        break
    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)
    say(result)