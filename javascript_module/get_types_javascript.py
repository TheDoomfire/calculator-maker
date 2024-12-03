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
    # Lazy way to get the old params and returns.
    # To grab the descriptions. Might use them for hover titles.
    old_params = extract_param_types(js_code)
    old_returns = extract_return_type(js_code)

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

    # Old: {"type": the_type, "name": name, "description": description, "element": element_type, "pretty_name": pretty_name}
    # Extract parameters and their comments
    parameters = []
    for param_match in param_comment_pattern.finditer(params_block):
        parameters.append({
            "name": param_match.group(1),
            "pretty_name": make_name_pretty(param_match.group(1)),
            "element": detect_type(param_match.group(2)),
            "description": find_value_by_key(old_params, "name", param_match.group(1), 'description'),
            "last_word": get_last_word(param_match.group(1))
        })

    # Find the return block
    return_match = return_pattern.search(js_code)
    returns = []
    if return_match:
        return_block = return_match.group(1)
        for return_item_match in return_comment_pattern.finditer(return_block):
            returns.append({
                "name": return_item_match.group(1),
                "pretty_name": make_name_pretty(return_item_match.group(1)),
                "element": detect_type(return_item_match.group(2)),
                "description": find_value_by_key(old_returns, "name", return_item_match.group(1), 'description'),
                "last_word": get_last_word(return_item_match.group(1))
            })

    return {
        "function_name": function_name,
        "parameters": parameters,
        "returns": returns
    }


def get_last_word(input_string):
    """
    Splits the input string by capital letters and returns the last word.
    If no separation occurs, returns the input string itself.
    
    :param input_string: The string to process.
    :return: The last word or the input string if it's a single word.
    """
    words = re.findall(r'[A-Z][a-z]*|[a-z]+', input_string)
    return words[-1] if words else input_string.lower()


def find_value_by_key(objects, match_key, match_value, return_key):
    """
    Find the value of a specific key in an object within a list, 
    based on a matching key-value pair.

    Args:
        objects (list): List of dictionaries to search.
        match_key (str): The key to match (e.g., 'name').
        match_value (str): The value to match for the key (e.g., 'banana').
        return_key (str): The key whose value you want to retrieve.

    Returns:
        Any or None: The value of the return_key, or None if no match is found.
    """
    return next((obj[return_key] for obj in objects if obj.get(match_key) == match_value), None)



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
        "unit": ["volume", "quantity", "amount", "count", "unit", "units"],
        "table": ["table", "data", "information"],
        "select": ["select", "option", "choice"],
        "compoundInterestSelect": ["compoundinterestfrequency", "select:compoundinterest"],
        "year": ["years", "year"],
    }
    
    # Convert to lowercase to make the check case-insensitive
    lower_string = input_string.lower()
    
    # Check each type group for matching keywords
    for type_name, keywords in type_keywords.items():
        if any(keyword in lower_string for keyword in keywords):
            return type_name.lower()
    
    # TODO: Maybe return the last word or something instead of "unsupported type". Or with a better PC, have AI.
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

    print("js_content", type(js_content))

    print("Parameters:", params)
    print("Return Type:", return_type)

    # TODO: Add description and pretty_name form the params/return.
    # TODO: Create a new "elements" 
    test = extract_function_details(js_content)
    print("test")
    print("test type", type(test))
    #print(test)
    print("New Params:", test['parameters'])
    print("New Returns:", test['returns'])


    # {'function_name': 'MarketValueAdded', 'parameters': [{'name': 'sharePrice', 'comment': 'Currency'}, {'name': 'sharesOutstanding', 'comment': 'Units'}, {'name': 'capitalInvested', 'comment': 'Currency'}]}

""" 
    Parameters: [{'type': 'number', 'name': 'sharePrice', 'description': 'The price per share of the stock.', 'element': 'share', 'pretty_name': 'Share Price'}, {'type': 
    'number', 'name': 'sharesOutstanding', 'description': 'The total number of outstanding shares.', 'element': 'share', 'pretty_name': 'Shares Outstanding'}, {'type': 'number', 'name': 'capitalInvested', 'description': 'The amount of capital invested.', 'element': 'currency', 'pretty_name': 'Capital Invested'}]
    Return Type: [{'type': 'number', 'name': 'marketValue', 'description': 'The total market value of the company.', 'element': 'unsupported type', 'pretty_name': 'Market Value'}, {'type': 'number', 'name': 'marketValueAdded', 'description': 'The market value added (MVA).', 'element': 'unsupported type', 'pretty_name': 'Market Value Added'}]
    test
    {'function_name': 'MarketValueAdded', 'parameters': [{'name': 'sharePrice', 'comment': 'Currency'}, {'name': 'sharesOutstanding', 'comment': 'Units'}, {'name': 'capitalInvested', 'comment': 'Currency'}], 'returns': [{'name': 'marketValue', 'comment': 'Currency'}, {'name': 'marketValueAdded', 'comment': 'Currency'}]}
 """
if __name__ == '__main__':
    main()
