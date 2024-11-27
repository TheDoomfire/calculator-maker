import os
import re
import sys

# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from javascript_module import get_types_javascript


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

    functionName = name[:1].upper() + name[1:] # Capitalize the first letter
    formName = name + "Form"
    formNameFile = formName + extension

    htmlName = camel_to_kebab(name)

    pretty_name = get_types_javascript.make_name_pretty(name)

    return {
        'function': functionName,
        'form': formName,
        'file': formNameFile,
        'html': htmlName,
        'pretty_name': pretty_name
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