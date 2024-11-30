from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

stronger_model_name = "llama3.2-vision" # Very slow.
weaker_model_name = "llama3.2" # Still very slow :(
current_model_name = stronger_model_name



# TODO: Maybe add more H2 tags. For example:
# "Common Scenarios"
# "Limitations and Assumptions
# "Real-World Applications"
# "FAQs"??

# Grab all the information needed for an article.
def create_ai_content(title, *content):

    # If the content is already an array, use it as-is.
    # Check if the first argument in *content is a list
    if len(content) == 1 and isinstance(content[0], list):
        content_list = content[0]  # Use the provided list as-is
    else:
        content_list = list(content)  # Convert individual arguments to a list

    # Format the content into a single string.
    content_formatted_string = "\n".join([f"File {i + 1}: {file_content}" for i, file_content in enumerate(content_list)])

    # Meta description.
    templateCalculator = """
    You will write a meta description for a given title. The max character count is 150 characters.
    The meta description should be a detailed description of the title.
    The meta description be written in a way that is understandable by a human. Easy and direct language is preferred.
    Base it on these files data, the meta description is for the calculator in these files.
    The javascript file is the actual formula for the calculator. And the html/nunjucks file is the template for the calculator.

    Files: {files}

    Title: {question}

    Do not include any additional text, explanations, or comments before or after the response.

    Answer:
    """


    # Template for the sections and all the H2 titles.
    templateContent = """
    You will write for the title "{question}". The text will be html ready, each h2 will be a section. There will be no boilerplate html surrounding the sections they will be the highest level of the html.
    All text should be in a paragraph tag for each text piece.
    Here is a list of all the H2 titles in the content:
    1. Formula - The formula for "{question}". It should be a H2 tag. It works like the javascript content and the inputs is from the html/nunjucks file and should mimic them and is only acceptable to change them slighly and if it increases the readability.
    If there are several return values from the javascript file and about the under the "results" in the results part of the html/nunjucks file then write each forumla with it's name and it's own h3 or h4 "Example".
    The formula should be inside a code tag with the class "formula". The formula should look the a formula, with the inputs in them as variables. There should be a h3 or h4 "Example" that gives a short and easy to understand example.
    2. Meaning - The meaning of the "{question}". It should be a H2 tag and explain the meaning of the title but leave out the "calculator" part. It should be a short and easy to understand explanation.

    Content: {files}

    Title: {question}

    Do not include any additional text, explanations, or comments before or after the response.

    Answer:
    """


    # So I can switch templates easily.
    template = templateCalculator

    model = OllamaLLM(model=current_model_name)

    # Meta description.
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model # It runs prompt first then model.

    # Article content.
    prompt_article = ChatPromptTemplate.from_template(templateContent)
    chain_article = prompt_article | model # It runs prompt first then model.

    #meta_description = chain.invoke({"question": title}, input="My question.")
    meta_description = chain.invoke({"question": title, "files": content_formatted_string})
    article_content = chain_article.invoke({"question": title, "files": content_formatted_string})

    # Had to make it a dict ("meta_description": meta_description vs just meta_description) because it was giving me this error:
    # TypeError: 'set' object is not subscriptable
    return {
        "meta_description": meta_description,
        "article_content": article_content
    }


def main():
    print("Running AI main.")
    title = "Compound Annual Growth Rate Calculator"

if __name__ == '__main__':
    main()