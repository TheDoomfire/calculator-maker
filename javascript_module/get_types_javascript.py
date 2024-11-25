import re


# TODO: Need to return all the types too?


def extract_param_types(js_content):
    # Regular expression to extract parameter info
    pattern = r'@param\s+{(\w+)}\s+(\w+)\s+-\s+(.*)'
    params = re.findall(pattern, js_content)
    return [{"type": p[0], "name": p[1], "description": p[2]} for p in params]


def extract_return_type(js_content):
    # Regular expression to extract return info
    pattern = r'@property\s+{(\w+)}\s+(.*)'
    returns = re.findall(pattern, js_content)
    return [{"type": ret[0], "name": ret[1].split("-")[0].strip(), "description": ret[1].split("-")[1].strip()} for ret in returns]


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


def main():
    js_content = """
    // Your JavaScript function here
    """
    print("get_types_javascript.py")
    params = extract_param_types(js_content)
    return_type = extract_return_type(js_content)

    print("Parameters:", params)
    print("Return Type:", return_type)

if __name__ == '__main__':
    main()
