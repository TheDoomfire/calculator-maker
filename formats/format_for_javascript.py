import os
import re


def format_js_function_name(file_name):
    """
    Formats a function name for use in a JavaScript file.
    
    Args:
        function_name (str): The name of the function
    
    Returns:
        str: The formatted function name
    """
    splitted_function_name = get_file_info(file_name)
    extension = splitted_function_name['extension']
    name = splitted_function_name['name']

    functionName = name.capitalize()
    formName = name + "Form"
    formNameFile = formName + extension

    htmlName = camel_to_kebab(name)

    return {
        'function': functionName,
        'form': formName,
        'file': formNameFile,
        'html': htmlName
    }


def get_file_info(filename):
    name, extension = os.path.splitext(filename)
    return {
        'name': name,
        'extension': extension.lower(),
        'is_valid_type': extension.lower() in ['.js', '.py', '.txt']
    }


def camel_to_kebab(text):
    # Use regex to insert hyphens before capital letters
    kebab_text = re.sub(r'(?<!^)(?=[A-Z])', '-', text).lower()
    return kebab_text