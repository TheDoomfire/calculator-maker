from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Local Imports:
from .ai_templates import templateContent, templateCalculator, templateMetaDescriptionHistory, templateFormula, templateMeaning, templateExample


stronger_model_name = "llama3.2-vision" # Very slow.
weaker_model_name = "llama3.2" # Still very slow :(
current_model_name = stronger_model_name




# TODO: Maybe add more H2 tags. For example:
# "Common Scenarios"
# "Limitations and Assumptions
# "Real-World Applications"
# "FAQs"??


# TODO: To improve this:
# Make several small AI requests. Easier to get it right and not skipping anything.
# Mix up the AI with programming. Since programming is always done the same way.



# Templates:



# Grab all the information needed for an article.
def create_ai_content(title, returns, *content):
    meta_description_history = ""

    # If the content is already an array, use it as-is.
    # Check if the first argument in *content is a list
    if len(content) == 1 and isinstance(content[0], list):
        content_list = content[0]  # Use the provided list as-is
    else:
        content_list = list(content)  # Convert individual arguments to a list

    # Format the content into a single string.
    content_formatted_string = "\n".join([f"File {i + 1}: {file_content}" for i, file_content in enumerate(content_list)])

    # AI model to use.
    model = OllamaLLM(model=current_model_name)

    # Meta description.
    prompt = ChatPromptTemplate.from_template(templateCalculator)
    chain = prompt | model # It runs prompt first then model.
    
    meta_description = chain.invoke({"question": title, "files": content_formatted_string})

    character_count = len(meta_description.strip())
    prompt_meta_description_history = ChatPromptTemplate.from_template(templateMetaDescriptionHistory)
    chain = prompt_meta_description_history | model # It runs prompt first then model.
    while character_count > 160:
        meta_description_history += f"\nAI Result: {meta_description}"
        meta_description = chain.invoke({"meta_description": meta_description, "character_count": character_count})
        character_count = len(meta_description)
        print("character_count", character_count)


    # Article content.
    #prompt_article = ChatPromptTemplate.from_template(templateContent)
    #chain_article = prompt_article | model # It runs prompt first then model.
    #prompt_formula = ChatPromptTemplate.from_template(templateFormula)
    #chain_formula = prompt_formula | model # It runs prompt first then model.
    prompt_meaning = ChatPromptTemplate.from_template(templateMeaning) 
    chain_meaning = prompt_meaning | model
    prompt_example = ChatPromptTemplate.from_template(templateExample) 
    chain_example = prompt_example | model


    # TODO: For each return, create a formula.
    article_content = ""
    if len(returns) == 1: # If only one return.
        name = returns[0]['pretty_name']
        formula = returns[0]['html_formula']
        new_formula_html = f"""<h2>Formula</h2>
{formula}
<h3>Example</h3>
"""
        article_content += new_formula_html
        example = write_example(chain_example, formula)
        article_content += example

    elif formula != "": # To remove empty formulas.
        new_title = """<h2>Formula</h2>\n\n"""
        article_content += new_title
        for ret in returns:
            print("RET:", ret)
            formula = ret['html_formula']
            if formula != "[]": # TODO: It still doesn't work since "Table Data =" still returns.
                pretty_name = ret['pretty_name']
                new_formula_html = f"""<h3>{pretty_name} Formula</h3>

{formula}
"""
                article_content += new_formula_html
                example = write_example(chain_example, formula)
                article_content += example         
        
    #article_content = chain_article.invoke({"question": title, "files": content_formatted_string})

    #formula_content = chain_formula.invoke({"files": content_formatted_string})
    #article_content += "\n" + formula_content

    meaning_content = chain_meaning.invoke({"title": title})

    article_content += "\n" + meaning_content


    # Had to make it a dict ("meta_description": meta_description vs just meta_description) because it was giving me this error:
    # TypeError: 'set' object is not subscriptable
    return {
        "meta_description": meta_description,
        "article_content": article_content
    }

def write_example(chain, formula):
    example_content = chain.invoke({"formula": formula})
    html = "\n<p class='example'>" + example_content + "</p>\n"
    return html


def test_variables():
    print("test_variables")
    print(templateContent)


def main():
    print("Running AI main.")
    print(templateContent)

if __name__ == '__main__':
    main()