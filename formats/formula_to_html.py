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
    return match.group(0) if match else None


def main():
    print("Running js_to_readable.py")
    #print(variables.test_js_content)
    # Example Usage
    js_formula = "a * b + c ** 2 / d >= e"
    result = js_to_readable(js_formula)

    print("Plain Text:", result['plain_text'])
    print("HTML:", result['html'])


    # TODO: Get all Variables from the function.
    getAllVariables = extract_js_constants(variables.test_js_content)
    print("getAllVariables:", getAllVariables)

    # Gets the constant variable.
    getVariable = find_const_declaration(variables.test_js_content, "investmentReturn")
    print("getConst", getVariable)

    # Split the variable and its value.
    splitVariable = getVariable.split('=', 1)
    const = splitVariable[0].strip()
    jsFormula = splitVariable[1].strip()
    print("const:", const)
    print("jsFormula:", jsFormula)
    
    # TODO: Remove the ; at the end of the formula.
    new_formula = js_to_readable(jsFormula)
    print("new_formula", new_formula)


if __name__ == '__main__':
    main()
