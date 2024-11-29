from langchain_ollama import OllamaLLM
from langchain_core import ChatPromptTemplate

stronger_model_name = "llama3.2-vision" # Very slow.
weaker_model_name = "llama3.2" # Still slow :(
current_model_name = stronger_model_name

model = OllamaLLM(model=current_model_name)

template = """
You are a helpful assistant that translates English to Swedish.

Context: {context}

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model # It runs prompt first then model.


def handle_conversation(conversation):
    context = ""
    

#result = model.invoke(input="Är Emma Åberg Bäst?")
result = model.invoke({"context": "", "question": "Är Emma Åberg Bäst?"})
print(result)


def main():
    print("Running AI.")

if __name__ == '__main__':
    main()