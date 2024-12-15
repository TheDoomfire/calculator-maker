from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Local Imports:
from .ai_templates import templateContent, templateCalculator, templateMetaDescriptionHistory, templateFormula, templateMeaning, templateExample, checkExampleCalculation


# All models are very slow on my PC.
summarization_model_name = "llama3.2:3b" # llama3.1:8b AND ollama run llama3.2:3b
image_generating_model_name = "llama3.2-vision"
code_model_name = "qwen2.5-coder:14b"
math_model_name = "phi3:medium" # 14B
code_gemma = "codegemma:7b"
code_model_name_lightweight = "codegemma:7b"
current_model_name = summarization_model_name


def remove_surrounding_quotes(input_string):
    """
    Removes any excess double quotes surrounding a string.
    
    Args:
        input_string (str): The input string potentially surrounded by double quotes.
    
    Returns:
        str: The string without surrounding double quotes.
    """
    # Remove leading and trailing quotes
    return input_string.strip('"')




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
def create_ai_content(title, returns, params, *content):
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
    model_code_lightweight = OllamaLLM(model=code_model_name_lightweight) # Maybe just dont use it.

    # Meta description.
    prompt = ChatPromptTemplate.from_template(templateCalculator)
    chain = prompt | model # It runs prompt first then model.
    
    meta_description = chain.invoke({"question": title, "files": content_formatted_string})

    character_count = len(meta_description.strip())
    prompt_meta_description_history = ChatPromptTemplate.from_template(templateMetaDescriptionHistory)
    chain = prompt_meta_description_history | model # It runs prompt first then model.
    while character_count > 160:
        meta_description_history += f"\nAI Result: {meta_description}"
        meta_description = chain.invoke({"meta_description": meta_description, "character_count": character_count, "question": title, "files": content_formatted_string})
        character_count = len(meta_description)
        print("character_count", character_count)

    meta_description = remove_surrounding_quotes(meta_description)


    # Article content.
    #prompt_article = ChatPromptTemplate.from_template(templateContent)
    #chain_article = prompt_article | model # It runs prompt first then model.
    #prompt_formula = ChatPromptTemplate.from_template(templateFormula)
    #chain_formula = prompt_formula | model # It runs prompt first then model.
    prompt_meaning = ChatPromptTemplate.from_template(templateMeaning) 
    chain_meaning = prompt_meaning | model
    prompt_example = ChatPromptTemplate.from_template(templateExample) 
    chain_example = prompt_example | model
    prompt_check_example = ChatPromptTemplate.from_template(checkExampleCalculation) 
    chain_check_example = prompt_check_example | model_code_lightweight


    # ----------- Formulas -----------
    
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
        example = write_example(chain_example, chain_check_example, formula)
        article_content += example

    else:
        #new_title = """<h2>Formulas</h2>\n\n"""
        #article_content += new_title
        # TODO: Add example numbers for the formulas. Based on the type like "Currency", "Percent" etc.
        # TODO: Then make a python function that calculates the answer to that formula.

        for ret in returns:
            formula = ret['html_formula']
            if formula != "":
                pretty_name = ret['pretty_name']
                new_formula_html = f"""<h2>{pretty_name} Formula</h2>

{formula}
"""
                article_content += new_formula_html
                example = write_example(chain_example, chain_check_example, formula)
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


# TODO: VERY WRONG!!
def write_example(chain, chainCheckExample, formula):
    html = ""
    count = 1

    while True:
        # Generate the example content using the formula
        example_content = chain.invoke({"formula": formula})
        
        # Check the example calculation
        check_example_calculation = chainCheckExample.invoke({"example": example_content})
        
        # Normalize the check result for consistency
        normalized_check = check_example_calculation.strip().lower().replace('"', '')
        
        # Break the loop if the result is "true"
        if normalized_check == "true":
            html = f"\n<p class='example'>{example_content}</p>\n"
            print("check_example_calculation TRUE: ", check_example_calculation)
            break
        
        print("check_example_calculation not TRUE, retrying...")
        print("Try: ", count)
        count += 1
        if count >= 10:
            print("Too many retries. Going french.", count)
            break



    return html


def test_variables():
    print("test_variables")
    print(templateContent)


def main():
    print("Running AI main.")
    print(templateContent)

if __name__ == '__main__':
    main()