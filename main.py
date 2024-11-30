#!/usr/bin/env python3
import os
import argparse
import webbrowser # For opening the browser.

# Local Imports
from javascript_module import read_javascript, get_types_javascript, create_js_form
from article_module import create_article_file
from formats import format_for_javascript, format_for_html
from html_module import create_html_file
from ai_module import get_ai_content

# Paths
main_path = r"D:\Documents\GitHub\chooseinvesting\src"
javascript_folder_path = os.path.join(main_path, "scripts", "calc")
forms_path = os.path.join(main_path, "scripts", "forms")
html_path = os.path.join(main_path, "_includes", "components", "calc")
articles_path = os.path.join(main_path, "calc")

# URL
main_url = "https://chooseinvesting.com/"
local_url = "http://localhost:8081/"

# File names
# javascript_file_name = "compoundAnnualGrowthRate.js" # compoundAnnualGrowthRate.js marketValueAdded.js


percentages = ["percent", "percentage"]
currencies = ["price", "capital"]
shares = ["share", "shares"]

# Get all Inputs - add elementType
# Get all returns - add elementType
# Split returns, numbers and additionalData. Like "table"



def main():

    # TODO: Make in the command prompt you can choose to delete the chosen one?
    run = True # If I should run the program (True) OR delete the files (False).

    print("Welcome to the calculator maker.")

    # ----------- Arguments -----------
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Helps creating the forms for calculators.")

    # Add a required text argument
    parser.add_argument(
        "text",  # This is a positional argument (no `--` required when passing it)
        type=str,  # The expected type of the argument
        help="The text to process",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Get the text from the arguments
    javascript_file_name = args.text + ".js"

    # ----------- Main -----------

    # TODO: See if any files been added to "javascript_folder_path" folder, if so, add them all to an array
    # TODO: Then run them all in this function.
    # Make this when I have tried it more.

    # Read the javascript file
    js_content = read_javascript.read_js_file(javascript_folder_path, javascript_file_name)

    # Get the types of the parameters and return value
    param_types = get_types_javascript.extract_param_types(js_content)
    return_types = get_types_javascript.extract_return_type(js_content)

    new_javascript_file_names = format_for_javascript.format_js_function_name(javascript_file_name)
    fileName = new_javascript_file_names['file'] # New file name for example "nameForm.js"
    htmlName = new_javascript_file_names['html'] # New file name for example "name-form"
    #pretty_name = new_javascript_file_names['pretty_name']
    nunjucksName = htmlName + ".njk"
    #formName = new_javascript_file_names['form'] # New file name for example "nameForm"
    #htmlName = new_javascript_file_names['html'] # New file name for example "name-form"

    new_javascript_content = create_js_form.generate_js_file(param_types, return_types, new_javascript_file_names)

    new_html_content = create_html_file.create_html_content(param_types, return_types, new_javascript_file_names)

    # TODO: Add "js_content", "new_javascript_content" and "new_html_content"
    new_calculator_article_content = create_article_file.create_article_content(param_types, return_types, new_javascript_file_names, [js_content, new_javascript_content,  new_html_content])


    # Creates files and returns the paths. Else returns paths of the files that already exist.
    new_form_path = create_js_form.create_file(new_javascript_content, forms_path, fileName)
    new_html_path = create_js_form.create_file(new_html_content, html_path, nunjucksName)
    new_calculator_article_path = create_js_form.create_file(new_calculator_article_content, articles_path, nunjucksName)

    all_new_files = [new_form_path, new_html_path, new_calculator_article_path]

    for file in all_new_files:
        if os.path.exists(file) and run:
            print("File at:", file)
        elif run == False:
            os.remove(file)
            print("Deleted:", file)        

    if run:
        # Open the browser.
        article_local_url = local_url + "calc/" + htmlName
        webbrowser.open(article_local_url)
        print("URL:", article_local_url)

"""     if run_or_delete != 1:
        # Deletes the form javascript file.
        os.remove(new_form_path)
        print("Deleted:", new_form_path)
        os.remove(new_html_path)
        print("Deleted:", new_html_path)
        os.remove(new_calculator_article_path)
        print("Deleted:", new_calculator_article_path) """


"""     test = get_types_javascript.detect_type("hello")
    print("TEST:", test) """

    #create_js_form.generate_js_file(param_types, new_javascript_file_names, forms_path)
    #test = create_js_form.get_imports(param_types)
    #print("test")
    #print(test)

    # TODO: Write the new javascript.
    # TODO: Create a javascript file (if it doesn't exit)

    # test(param_types, new_javascript_file_names) params, fileNames

if __name__ == '__main__':
    main()