from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
import sys
import random
import re
import colorama
from colorama import Back, Fore, Style

# Local Imports:
# ERROR: if I run from main it's "ai_templates" otherwise if I run the main.py it's ".ai_templates".
from .ai_templates import templateContent, templateCalculator, templateMetaDescriptionHistory, templateFormula, templateMeaning, templateExample, checkExampleCalculation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import variables


# All models are very slow on my PC.
summarization_model_name = "llama3.2:3b" # llama3.1:8b AND ollama run llama3.2:3b AND "mistral:7b"
image_generating_model_name = "llama3.2-vision"
code_model_name = "qwen2.5-coder:14b"
math_model_name = "phi3:medium" # 14B
code_gemma = "codegemma:7b"
code_model_name_lightweight = summarization_model_name #"codegemma:7b"
current_model_name = summarization_model_name

colorama.init(autoreset=True)


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
    # TODO: Make it us the meta_description_history to generate the meta description since some AI models clearly dont understand character count.
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
        #name = returns[0]['pretty_name']
        formula = returns[0]['html_formula']
        formula_example = returns[0]['html_ugly']
        new_formula_html = f"""<h2>Formula</h2>
{formula}
"""
        
        # TODO: Add example numbers formula before/after the actual example text.
        #formula_example = extract_text_from_tags(formula)
        #print("FORMULA EXAMPLE before fix", formula_example)
        formula_example = create_example_formula(formula_example, params, returns)

        article_content += new_formula_html
        example = write_example(chain_example, chain_check_example, formula, formula_example)

        article_content += example

    else:
        #new_title = """<h2>Formulas</h2>\n\n"""
        #article_content += new_title
        # TODO: Add example numbers for the formulas. Based on the type like "Currency", "Percent" etc.
        # TODO: Then make a python function that calculates the answer to that formula.

        for ret in returns:
            print("-------------------------------------")
            print("RETURN:", ret)
            print("-------------------------------------")
            formula = ret['html_formula']
            formula_example = ret['html_ugly']
            print("-------------------------------------")
            print("FORMULA in ret:", formula)
            print("-------------------------------------")
            formula_variables = ret['formula_variables']
            mylist = get_names_and_elements_by_words(params, formula_variables)
            print("mylist", mylist)
            if formula != "":
                pretty_name = ret['pretty_name']
                new_formula_html = f"""<h2>{pretty_name} Formula</h2>

{formula}
"""
                article_content += new_formula_html
                formula = extract_text_from_tags(formula)
                #print("FORMULA EXAMPLE before fix", formula_example)
                formula_example = create_example_formula(formula_example, params, returns)
                example = write_example(chain_example, chain_check_example, formula, formula_example)
                article_content += example         
        
    #article_content = chain_article.invoke({"question": title, "files": content_formatted_string})

    #formula_content = chain_formula.invoke({"files": content_formatted_string})
    #article_content += "\n" + formula_content

    meaning_content = chain_meaning.invoke({"title": title})

    # TODO: Have "meaning" being a constant and not with AI.
    article_content += "\n" + '<h2 id="meaning">Meaning</h2>' + "\n"  + meaning_content


    # Had to make it a dict ("meta_description": meta_description vs just meta_description) because it was giving me this error:
    # TypeError: 'set' object is not subscriptable
    return {
        "meta_description": meta_description,
        "article_content": article_content
    }


def extract_text_from_tags(html):
    """
    Extracts text from all HTML tags in a given string.
    
    Parameters:
        html (str): A string containing HTML content.
        
    Returns:
        list: A list of text content from all tags.
    """
    # Regular expression to match content inside HTML tags
    return re.findall(r'>([^<]+)<', html)



def simplify_number(num, max_decimals=5):
    """Simplifies a number by rounding to an appropriate number of decimals."""
    if num == 0:
        return 0
    magnitude = abs(num)
    
    # Determine the number of decimals based on the size of the number
    if magnitude >= 1:
        decimals = max(1, max_decimals - len(str(int(magnitude))))  # Fewer decimals for large numbers
    else:
        decimals = max_decimals  # Keep more decimals for small numbers

    return round(num, decimals)



def get_names_and_elements_by_words(params, word_list):
    """
    Checks if any word from the word list exists in the 'name' field of the params
    and returns the corresponding 'name' and 'element' values.

    :param params: List of dictionaries containing parameter details
    :param word_list: List of words to search for in the 'name' field
    :return: List of dictionaries with matched 'name' and 'element' pairs
    """
    matched_items = []
    
    for param in params:
        # Check if any word in the word_list is present in the 'name' field
        if any(word in param['name'] for word in word_list):
            matched_items.append({'name': param['name'], 'element': param['element']})
    
    return matched_items

""" 
    // WORKS!
    const fundAssets = totalInvestments + cashAndCashEquivalents + accountReceivable;

    // WORKS!
    const fundLiabilities = shortTermLiabilities + longTermLiabilities;

    // DOESNT WORK! Doesnt understand the element type (currency, percent, etc.)
    const nav = fundAssets - fundLiabilities; 
"""

# Create a example formula.
# TODO: Fix so it can never get the error: ZeroDivisionError: float division by zero.
# Fix it by making it not divide by zero.
def create_example_formula(formula, params, returns):
    # If the formula is a list, get the first element.
    print("-------------------------------------")
    print("FORMULA:", Fore.RED + formula)
    print("-------------------------------------")
    print("Returns:", returns)
    print("-------------------------------------")
    print("Params:", params)
    print("-------------------------------------")
    if isinstance(formula, list) or isinstance(formula, tuple):
        formula = formula[0] # ERROR!

    items = [returns, params]

    # TODO:
    # Make it grab the element type (currency, percent, etc.) from already solved equations if its needed in futher down calculation.

    splitted_formula = formula.split()
    print("Splitted Formula:", splitted_formula)
    
    #last_char = None
    #solution_variable = ""
    all_elements = []
    all_numbers = []
    all_numbers_with_elements = []
    # --- Get all the elements. ---
    #count = 0
    for char in splitted_formula:
        #print("-------------------------------------")
        #print("Char:", char)
        #print("-------------------------------------")

        # Trying to get the solution variable. Example: solution_variable = 1 + 1
        #if count == 0:
        #    solution_variable = char
        #count += 1

        # If more then one character (+ - * / etc.)
        # TODO: Maybe have to add to check ret for elements too? because it wont exist inside of params.
        # What if the character a = x + y is all returns?
        # Make ir run twice with params and returns so I dont have to write the code twice.

        # TODO: Need to not count the first one. and not add in the result?
        count = 0
        if len(char) > 1:
            
            # TODO: Doesn't count 1.2 as a number.
            #if char.isnumeric(): # Check if it's a number.
            if isfloat(char): # Check if it's a number.
                #print("Number:", char)
                all_elements.append("number")
                all_numbers.append(float(char))
                all_numbers_with_elements.append(str(char))
                print("Number:", Fore.GREEN + char)
            else: # Not a number.
                print("Not a number:", Fore.RED + char)
                for item in items: # items = returns + params
                    for i in item:
                        if i['name'] == char:
                            element = i['element']
                            all_elements.append(element)
                            #print("Elements:", element)
                            random_number = made_up_numbers(element, all_numbers)
                            all_numbers.append(random_number)
                            if element == "currency":
                                all_numbers_with_elements.append("$" + str(random_number))
                            elif element == "percent":
                                all_numbers_with_elements.append(str(random_number) + "%")
                            elif element == "share":
                                all_numbers_with_elements.append(str(random_number) + " shares")
                                #all_numbers_with_elements.append(str(random_number))
                            else:
                                all_numbers_with_elements.append(str(random_number))
                            

            # TODO: Add a checker if it's not in returns or params and still is a number.
            #last_char = char
        else:
            print("Character (NOT FOUND):", char)

    
    # ERROR: If both rhs is also in return they dont show in either.
    print("All Elements:", all_elements)
    solution_name = all_numbers[0]
    all_numbers.pop(0) # Remove the first one, aka "the solution".
    print("All Numbers:", all_numbers)
    print("All Numbers with elements:", all_numbers_with_elements)
    
    formula_solution = formula.split("=")[0]
    formula_right_hand_side = formula.split("=")[1]
    print("Formula Right Hand Side:", formula_right_hand_side)
    print("Formula Solution:", formula_solution) # just returns nav

    # ERROR: I get this:
    #All Elements: ['currency']
    #All Numbers with elements: ['$17100']
    #Formula Right Hand Side:  fundAssets - fundLiabilities
    #Formula Solution: nav
    # But there should be a total of 3 elements.

    rhs_chars = formula_right_hand_side.split()
    # TODO: Fix this. Make it turn "hello + jkasdjka + hey" into numbers like "1 + 2 + 3".
    rhs_words = []
    count = 0
    for char in rhs_chars:
        if len(char) > 1:
            print("Char:", Fore.RED + char)
            rhs_chars[rhs_chars.index(char)] = str(all_numbers[count]) # problem?
            rhs_words.append(char)
            count += 1

    rhs_formula = " ".join(rhs_chars)

    print("RHS Words:", rhs_words) # Works.
    print("RHS Chars:", rhs_chars) # Do not work.
    print("RHS Formula:", rhs_formula)

    solution = eval(rhs_formula)
    print("Solution (without rounding):", solution, type(solution))
    solution = simplify_number(solution)
    print("Solution (with rounding):", solution, type(solution))

    # Changed place on solution and rhs_formula. Might not work correctly..
    #completed_formula = str(solution) + " = " + rhs_formula # Or the other way around?
    completed_formula = rhs_formula + " = " + str(solution)
    print("All Elements:", all_elements)
    print("Completed Formula:", completed_formula)


    fixed_element_list = all_elements[1:] + all_elements[:1]
    print("Fixed Elements:", fixed_element_list)

    # TODO: Parts wont be the same 
    parts = completed_formula.split()
    count = 0
    # all_elements or fixed_element_list
    for i, part in enumerate(parts):
        #if isinstance(part, (int, float)) or len(part) > 1: # Tried to make if its a number or more then one character.
        # try float(part):
        # TODO: ERROR HERE!
        if len(part) > 1:
            #print("count:", count)
            if fixed_element_list[count] == "currency": # TODO: Error here. IndexError: list index out of range. If I have a constant (like 100 or whatever) it won't have a element type.
                parts[i] = "$" + str(part)
                print("Currency:", parts[i])
            elif fixed_element_list[count] in ["number", "ratio"]:
                parts[i] = str(part)
                print("Number:", parts[i])
            elif fixed_element_list[count] == "percent":
                parts[i] = str(part) + "%"
                print("Percent:", parts[i])
            elif fixed_element_list[count] == "share":
                parts[i] = str(part) + " shares"
                print("Share:", parts[i])
            else:
                parts[i] = str(part)
                print("Default:", parts[i])
            count += 1

    fancy_formula = " ".join(parts)
    print("Fancy Formula:", Fore.GREEN + fancy_formula)
    

    # TODO: Make up numbers for the formula.
    #for rhs in formula_right_hand_side:
    #    print()
    

    return fancy_formula


""" 
                    # NOT WORKING!!!
                    if ret != solution_variable:
                        print("--- Not Solution Variable:", char)
                        random_number = made_up_numbers(element, all_numbers)
                        all_numbers.append(random_number)
                        if element == "currency":
                            print("Currency:", random_number, char)
                            all_numbers_with_elements.append("$" + str(random_number))
                        elif element == "percent":
                            print("Percent:", random_number, char)
                            all_numbers_with_elements.append(str(random_number) + "%") """


# Map formats to symbols
def format_number(value, fmt):
    if fmt == 'currency':
        return f"${value}"
    elif fmt == 'percent':
        return f"{value}%"
    return value  # Default if no match


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# TODO: Add percentages, units, etc!
def made_up_numbers(element, last_numbers):
    number = False
    if element == "currency":
        # Generate random number between 1000-20000 in steps of 100
        while True:
            random_number = random.randrange(1000, 20000, 100)
            if random_number not in last_numbers:
                number = random_number
                break
    elif element == "percent":
        # Generate random number between 1-100 in steps of 1
        while True:
            random_number = random.randrange(1, 30, 1)
            if random_number not in last_numbers:
                number = random_number
                break
    elif element == "share":
        # Generate random number between 1-300k in steps of 1k
        while True:
            random_number = random.randrange(1000, 300000, 1000)
            if random_number not in last_numbers:
                number = random_number
                break
    else:
        while True:
            random_number = random.randrange(100, 10000, 100)
            if random_number not in last_numbers:
                number = random_number
                break
    return number


# TODO: Maybe add so only one chain works?
# Loops forever.
def write_example(chain, chainCheckExample, formula, formula_example):
    html = ""
    count = 1

    while True:
        # Generate the example content using the formula
        example_content = chain.invoke({"formula": formula, "formula_example": formula_example}) # Right inputs.
        print("EXAMPLE CONTENT:", example_content)
        
        # Check the example calculation
        #check_example_calculation = chainCheckExample.invoke({"example": example_content})
        
        # Normalize the check result for consistency
        #normalized_check = check_example_calculation.strip().lower().replace('"', '')

        # TODO: Remove this maybe?
        normalized_check = "true"
        
        # Break the loop if the result is "true"
        if normalized_check == "true":
            html = f"\n<p class='example'><span class='example_number'>{formula_example}.</span>{example_content}</p>\n"
            print("example_content TRUE: ", example_content)
            #print("check_example_calculation TRUE: ", check_example_calculation)
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
    #print(templateContent)
    print(create_example_formula(variables.test_formula, variables.test_params, variables.test_returns))
    print(made_up_numbers("currency", [1000, 2000, 3000]))

if __name__ == '__main__':
    main()