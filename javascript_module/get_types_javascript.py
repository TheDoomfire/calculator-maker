import re


# TODO: Make this work! Work with params. Params for description and this for the rest.

def extract_function_details(js_code):
    """
    Extracts the parameters, their comments, and return object details from an export default JavaScript function.

    Args:
        js_code (str): The JavaScript code containing the function.

    Returns:
        dict: A dictionary with the function name, parameters, and return details.
    """
    # Regex to find the export default function and its parameters
    function_pattern = re.compile(
        r"export\s+default\s+function\s+(\w+)\s*\(([^)]*)\)", re.MULTILINE
    )

    # Regex to find parameters with inline comments
    param_comment_pattern = re.compile(r"(\w+)\s*,?\s*//\s*(.+)")

    # Regex to find the return object
    return_pattern = re.compile(r"return\s*\{\s*([\s\S]*?)\s*\};", re.MULTILINE)

    # Regex to extract return object properties and comments
    return_comment_pattern = re.compile(r"(\w+)\s*,?\s*//\s*(.+)")

    # Find the function definition
    match = function_pattern.search(js_code)
    if not match:
        return None

    function_name = match.group(1)
    params_block = match.group(2)

    # Extract parameters and their comments
    parameters = []
    for param_match in param_comment_pattern.finditer(params_block):
        parameters.append({
            "name": param_match.group(1),
            "comment": param_match.group(2)
        })

    # Find the return block
    return_match = return_pattern.search(js_code)
    returns = []
    if return_match:
        return_block = return_match.group(1)
        for return_item_match in return_comment_pattern.finditer(return_block):
            returns.append({
                "name": return_item_match.group(1),
                "comment": return_item_match.group(2)
            })

    return {
        "function_name": function_name,
        "parameters": parameters,
        "returns": returns
    }


""" def extract_param_types(js_content):
    # Regular expression to extract parameter info
    pattern = r'@param\s+{(\w+)}\s+(\w+)\s+-\s+(.*)'
    params = re.findall(pattern, js_content)
    return [{"type": p[0], "name": p[1], "description": p[2]} for p in params]
 """

# Example: marketValueCurrency - Market Value ($)
# Example 2: marketValueCurrencyAdded - Market Value Added ($)
# Remove the name that is in "detect_type(name)"
# Makes years - S
""" def make_name_pretty(name):
    print("name")
    print(name)
    element_type = detect_type(name)
    print("element_type")
    if element_type != "unsupported type" or element_type != "unsupported":
        # removes the element type from the name.
        name = re.sub(element_type, '', name, flags=re.IGNORECASE) # THE PROBLEM IS HERE
        print("name2:", name)
        # Seperates them.
        name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
        print("name3:", name)
        # Make each word capitalized.
        name = ' '.join(word.capitalize() for word in name.split())
        print("name4:", name)

    return name """


def make_name_pretty(name):

    element_type = detect_type(name)  # Ensure this returns correct values
    if element_type != "unsupported type" and element_type != "unsupported":
        # Escape the element_type to avoid regex issues
        escaped_type = re.escape(element_type)
        # Removes the element type from the name
        name = re.sub(rf'\b{escaped_type}\b', '', name, flags=re.IGNORECASE)

    # Separates words by detecting uppercase letters
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)

    # Capitalize each word
    name = ' '.join(word.capitalize() for word in name.split())

    return name



def extract_param_types(js_content):
    # Regular expression to extract parameter info
    pattern = r'@param\s+{(\w+)}\s+(\w+)\s+-\s+(.*)'
    params = re.findall(pattern, js_content)
    
    # Now you can manipulate 'param' before returning
    processed_params = []
    for param in params:
        the_type = param[0]
        name = param[1]
        description = param[2]
        element_type = detect_type(param[1])
        pretty_name = make_name_pretty(param[1]) # ERROR: UnboundLocalError: cannot access local variable 'pretty_name' where it is not associated with a value

        processed_params.append({"type": the_type, "name": name, "description": description, "element": element_type, "pretty_name": pretty_name})
    
    return processed_params

""" def extract_return_type(js_content):
    # Regular expression to extract return info
    pattern = r'@property\s+{(\w+)}\s+(.*)'
    returns = re.findall(pattern, js_content)
    return [{"type": ret[0], "name": ret[1].split("-")[0].strip(), "description": ret[1].split("-")[1].strip()} for ret in returns] """

# TODO: Add pretty return.
def extract_return_type(js_content):
   # Regular expression to extract return info
   pattern = r'@property\s+{(\w+)}\s+(.*)'
   returns = re.findall(pattern, js_content)
   
   processed_returns = []
   for ret in returns:
       # Split description and handle potential variations
       parts = ret[1].split("-", 1)
       name = parts[0].strip()
       description = parts[1].strip() if len(parts) > 1 else ""
       element_type = detect_type(name)
       pretty_name = make_name_pretty(name)
       
       processed_returns.append({
           "type": ret[0], 
           "name": name, 
           "description": description,
           "element": element_type,
           "pretty_name": pretty_name
       })
   
   return processed_returns



# DELETE?
def categorize_parameters(parameters, currencies, shares, percentages):
    """
    Categorizes parameters based on their name and type.

    :param parameters: A list of parameter dictionaries, e.g.,
        [
            {"name": "sharePrice", "type": "number", "description": "..."},
            {"name": "sharesOutstanding", "type": "number", "description": "..."},
            {"name": "capitalInvested", "type": "number", "description": "..."}
        ]
    :param currencies: A list of keywords related to currencies, e.g., ["price", "capital"].
    :param shares: A list of keywords related to shares, e.g., ["share", "shares"].
    :return: A dictionary mapping parameter names to their categories (e.g., "currency" or "share").
    """
    result = {}
    for param in parameters:
        if param["type"] == "number":
            name = param["name"].lower()
            # Check if the name matches any keyword in currencies

            if any(keyword in name for keyword in percentages):
                result[param["name"]] = "percentage"
            elif any(keyword in name for keyword in currencies):
                result[param["name"]] = "currency"
            # Check if the name matches any keyword in shares
            elif any(keyword in name for keyword in shares):
                result[param["name"]] = "share"
            else:
                result[param["name"]] = "unknown"
        else:
            result[param["name"]] = "unsupported type"
    return result


# To detect which element type I should use.
# And what to return in the javascript file. For example "currency" or "share". Or put in a table.
# So I know if I should make a input or a select.
# Or create a table.
def detect_type(input_string):
    """
    Detect the type of the input string based on specific keywords.
    
    Args:
        input_string (str): The string to be analyzed
    
    Returns:
        str: The detected type or "unsupported type"
    """
    type_keywords = {
        "percent": ["percentage", "percent", "percentile"], #  "rate", "ratio"
        "currency": ["currency", "money", "capital"], # "price", "cost", "dollar", "euro", "pound",
        "share": ["share", "stock", "equity", "ownership", "holding"],
        "unit": ["volume", "quantity", "amount", "count"],
        "table": ["table", "data", "information"],
        "select": ["select", "option", "choice"],
        "compoundInterestSelect": ["compoundinterestfrequency",],
        "year": ["years", "year"],
    }
    
    # Convert to lowercase to make the check case-insensitive
    lower_string = input_string.lower()
    
    # Check each type group for matching keywords
    for type_name, keywords in type_keywords.items():
        if any(keyword in lower_string for keyword in keywords):
            return type_name
    
    # If no keywords are found
    return "unsupported type"



def main():
    # Test js content.
    js_content = """
/**
 * Calculates the market value and market value added (MVA).
 * @param {number} sharePrice - The price per share of the stock.
 * @param {number} sharesOutstanding - The total number of outstanding shares.
 * @param {number} capitalInvested - The amount of capital invested.
 * @returns {Object} An object containing the calculated values.
 * @property {number} marketValue - The total market value of the company.
 * @property {number} marketValueAdded - The market value added (MVA).
 */

export default function MarketValueAdded(
    sharePrice, // Currency
    sharesOutstanding, // Units
    capitalInvested // Currency
) {
    const marketValue = sharePrice * sharesOutstanding;
    const marketValueAdded = marketValue - capitalInvested;

    return {
        marketValue, // Currency
        marketValueAdded // Currency
    };
};
    """
    print("get_types_javascript.py")
    params = extract_param_types(js_content)
    return_type = extract_return_type(js_content)

    print("Parameters:", params)
    print("Return Type:", return_type)

    test = extract_function_details(js_content)
    print("test")
    print(test)

    # {'function_name': 'MarketValueAdded', 'parameters': [{'name': 'sharePrice', 'comment': 'Currency'}, {'name': 'sharesOutstanding', 'comment': 'Units'}, {'name': 'capitalInvested', 'comment': 'Currency'}]}

if __name__ == '__main__':
    main()
