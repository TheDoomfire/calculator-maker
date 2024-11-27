import os
import re
import sys

# MAYBE DONT NEED THIS AT ALL.

# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from javascript_module import get_types_javascript


def format_html_function_name(file_name):
    print("file_name:", file_name)

    pretty_name = get_types_javascript.make_name_pretty(file_name)

    # Make the text pretty.
    # Create a title + add "Calculator" to the end.
    returnObj = {
        pretty_name
    }

    return returnObj


def create_calculator_title(name):
    return name + " Calculator"