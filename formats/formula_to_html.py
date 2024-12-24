import os
import sys
import re

# Local Imports
# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import variables


# Creates a formula.
def js_to_readable(js_formula):
    # Define mappings for operators
    operator_map = {
        '*': {'plain': '×', 'html': '&times;'},
        '/': {'plain': '÷', 'html': '&divide;'},
        '**': {'plain': '^', 'html': '<sup>'},  # Special handling for superscript
        '+': {'plain': '+', 'html': '+'},
        '-': {'plain': '-', 'html': '-'},
        '%': {'plain': 'mod', 'html': 'mod'},
        '>=': {'plain': '≥', 'html': '&ge;'},
        '<=': {'plain': '≤', 'html': '&le;'},
        '>': {'plain': '>', 'html': '>'},
        '<': {'plain': '<', 'html': '<'},
        '=': {'plain': '=', 'html': '='},
    }
    
    # Replace operators
    readable_plain = js_formula
    readable_html = js_formula
    
    for js_op, symbols in sorted(operator_map.items(), key=lambda x: -len(x[0])):  # Sort by length to avoid partial matches
        # Plain text replacement
        if js_op == '**':
            readable_plain = re.sub(rf'(\w+)\s*\*\*\s*(\w+)', r'\1^\2', readable_plain)
            readable_html = re.sub(rf'(\w+)\s*\*\*\s*(\w+)', r'\1<sup>\2</sup>', readable_html)
        else:
            readable_plain = readable_plain.replace(js_op, symbols['plain'])
            readable_html = readable_html.replace(js_op, symbols['html'])
    
    return {
        'plain_text': readable_plain,
        'html': readable_html
    }


# Get the return values. Maybe dont need this got another one that does it.
def extract_js_return_values(js_content):
    """
    Extract return values and comments from an export default function in JavaScript content.

    Args:
        js_content (str): JavaScript content as a string.

    Returns:
        list of dict: A list of dictionaries with 'key' and 'comment' for each return value.
    """
    # Match the return block inside the export default function
    return_block_pattern = r"export\s+default\s+function.*?return\s*{([\s\S]*?)};"
    return_block_match = re.search(return_block_pattern, js_content)
    
    if not return_block_match:
        return []
    
    return_block = return_block_match.group(1)
    
    # Extract individual return keys and their comments
    return_values_pattern = r"(\w+)\s*,?\s*//\s*(.+)"
    matches = re.findall(return_values_pattern, return_block)
    
    return [
        {"key": match[0].strip(), "comment": match[1].strip()} for match in matches
    ]

# Grab variables "const = X" so I can use it.
def extract_js_constants(js_content):
    """
    Extract constants and their values from the export default function in JavaScript content.

    Args:
        js_content (str): JavaScript content as a string.

    Returns:
        list of dict: A list of dictionaries with 'name' and 'value' for each constant found.
    """
    # Match the export default function block
    export_function_pattern = r"export\s+default\s+function.*?{([\s\S]*?)}"
    function_match = re.search(export_function_pattern, js_content)
    
    if not function_match:
        return []
    
    function_body = function_match.group(1)
    
    # Match const declarations within the function body
    const_pattern = r"const\s+(\w+)\s*=\s*(.+?);"
    matches = re.findall(const_pattern, function_body)
    
    return [
        {"name": match[0].strip(), "value": match[1].strip()} for match in matches
    ]


# THIS IS USED FOR THE MAIN FUNCTION.
def readable_formulas(js_content, return_types):
    formulas = []
    for return_type in return_types:
        name = return_type['name']

        getVariables = find_const_declaration(js_content, name)
        splitVariable = getVariables.split('=', 1)
        const = splitVariable[0].strip()
        jsFormula = splitVariable[1].strip()
        if const.startswith("const ") and jsFormula != "[]":
            #print("jsFormula:", jsFormula)

            # TODO: Use: js_to_mathml to html, and create new function for plainText
            formula = js_to_readable(jsFormula)
            plainText = formula['plain_text']
            html = formula['html']
            new_object = {'name': name, 'plain_text': plainText, 'html': html}
            formulas.append(new_object)

    return formulas


# TODO: all words inside it should be splitted and capitalized.
def js_to_mathml(expression):
    """
    Convert a JavaScript math expression to an HTML math tag.
    
    Args:
        expression (str): A math expression in JavaScript syntax
    
    Returns:
        str: An HTML math tag representation of the expression
    """
    # Replace Python/JavaScript-specific operators

    print("expression", expression)
    if not expression == "":
        html_expression = expression.replace('**', '^')  # Exponentiation
        html_math_tag_ugly = html_expression
        print("html_math_tag_ugly", html_math_tag_ugly)
        html_expression = prettify_formula(html_expression)
        
        # Wrap the expression in an HTML math tag
        html_math_tag = f'<math xmlns="http://www.w3.org/1998/Math/MathML" class="formula">{html_expression}</math>'
        
        return {"html": html_math_tag, "html_ugly": html_math_tag_ugly}
    return "", ""



def prettify_formula(formula: str) -> str:
    """
    Prettifies a formula string by converting variable names into more human-readable titles.
    
    Args:
        formula (str): The formula string to prettify.
    
    Returns:
        str: The prettified formula string.
    """
    def prettify_variable(variable: str) -> str:
        # Split camelCase or snake_case and capitalize each word
        words = re.split(r'[_]', re.sub(r'([a-z])([A-Z])', r'\1 \2', variable))
        return ' '.join(word.capitalize() for word in words)
    
    # Extract variable names and prettify them
    prettified_formula = re.sub(r'\b[a-zA-Z_]+\b', lambda match: prettify_variable(match.group()), formula)
    return prettified_formula


# TODO: If formula is for example just "Table Data =" then just have it as none.
# TODO: Add a function that returns the formula and the variables.
def readable_formula(js_content, name):
    formulas = []

    getVariables = find_const_declaration(js_content, name)
    splitVariable = getVariables.split('=', 1)
    #const = splitVariable[0].strip() # .replace("const ", "")
    jsFormula = splitVariable[1].strip()

    words = re.findall(r'\b\w+\b', jsFormula)
    # TODO: Add array to words for each element.

    if "[]" not in jsFormula:
        both_formula = js_to_mathml(getVariables)
        formula_html = both_formula['html']
        formula_ugly = both_formula['html_ugly']

        new_object = {
            'name': name, 
            'html': formula_html.replace("Const ", ""), 
            "formula_variables": words,
            'html_ugly': formula_ugly.replace("const ", "")
            }
        formulas = new_object
        return formulas

    #print("JSFORMULA", jsFormula)

    return {'name': name, 'html': "", "formula_variables": words}



# TODO: Fix this!
def all_formula_variables(js_content, name):
    variables = []
    #formulas = []

    getVariables = find_const_declaration(js_content, name)
    splitVariable = getVariables.split('=', 1)
    #const = splitVariable[0].strip() # .replace("const ", "")
    jsFormula = splitVariable[1].strip()

    print("splitVariable:", splitVariable)
    print("jsFormula:", jsFormula)
    print("Splitted:", jsFormula.split())
    words = re.findall(r'\b\w+\b', jsFormula)
    print("words:", words)

    if "[]" not in jsFormula:
        print("NOOOOT")
        formula = js_to_mathml(getVariables)

        new_object = {'name': name, 'html': formula.replace("Const ", "")}
        variables = new_object
        return variables

    #print("JSFORMULA", jsFormula)

    return {'name': name, 'html': ""}




def find_const_declaration(js_code: str, variable_name: str) -> str | None:
    """
    Finds and returns the constant declaration for a given variable name in JavaScript code.

    Args:
        js_code (str): The JavaScript code as a string.
        variable_name (str): The name of the variable to search for.

    Returns:
        str | None: The full constant declaration if found, otherwise None.
    """
    # Regex to match the entire constant declaration line
    pattern = rf"\bconst\s+{re.escape(variable_name)}\s*=\s*.*?;"
    match = re.search(pattern, js_code)
    return match.group(0).rstrip(";") if match else None


def main():
    print("Running js_to_readable.py")
    #print(variables.test_js_content)
    # Example Usage
    js_formula = "cagr = ((finalValue / initialValue) ^ ((1 / years) - 1)) * 100"

    result = js_to_mathml(js_formula)
    print("MathML:", result)

    js_table_formula = "const tableData = [];"
    test = js_to_mathml(js_table_formula)
    print("MathML table:", test)
    # Test with readable_formula
    js_table_test = readable_formula(variables.test_js_content, "tableData")
    print("js_table_test", js_table_test['html'])
    test2 = js_to_mathml(js_table_test['html'])
    print("Test2:", test2)
    js_table_test2 = all_formula_variables(variables.test_js_content2, "fundAssets")
    print("js_table_test2", js_table_test2)

    
if __name__ == '__main__':
    main()
