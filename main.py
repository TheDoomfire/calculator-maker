#!/usr/bin/env python3
import os
import argparse
import webbrowser # For opening the browser.
import subprocess
import colorama # Terminal coloring
from colorama import Back, Fore, Style

# Local Imports
from javascript_module import read_javascript, get_types_javascript, create_js_form
from article_module import create_article_file
from formats import format_for_javascript, format_for_html, formula_to_html
from html_module import create_html_file
from ai_module import get_ai_content

# Paths
main_path = r"D:\Documents\GitHub\chooseinvesting\src"
javascript_folder_path = os.path.join(main_path, "scripts", "calc")
forms_path = os.path.join(main_path, "scripts", "forms")
html_path = os.path.join(main_path, "_includes", "components", "calc")
articles_path = os.path.join(main_path, "calc")

python_path = r"D:\Documents\GitHub\calculator-maker"
input_file = os.path.join(python_path, "input.txt")
error_file = os.path.join(python_path, "error.txt")

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

def run_main(javascript_file_name, run, allow_ai):
    # TODO: Put all of this in a function.
    # Your processing code here
    print(Fore.LIGHTBLUE_EX + f"Processing: {javascript_file_name}")
        # Read the javascript file
    js_content = read_javascript.read_js_file(javascript_folder_path, javascript_file_name)


    # Get the types of the parameters and return value based on the comments on the function.
    all_returns = get_types_javascript.extract_function_details(js_content)
    print("all_returns", all_returns)
    param_types = all_returns['parameters']
    return_types = all_returns['returns']

    new_javascript_file_names = format_for_javascript.format_js_function_name(javascript_file_name)
    print("new_javascript_file_names", new_javascript_file_names)
    fileName = new_javascript_file_names['file'] # New file name for example "nameForm.js"
    htmlName = new_javascript_file_names['html'] # New file name for example "name-form"
    #pretty_name = new_javascript_file_names['pretty_name']
    nunjucksName = htmlName + ".njk"
    #formName = new_javascript_file_names['form'] # New file name for example "nameForm"
    #htmlName = new_javascript_file_names['html'] # New file name for example "name-form"


    new_javascript_content = create_js_form.generate_js_file(param_types, return_types, new_javascript_file_names)
    print("new_javascript_content", new_javascript_content)
    new_html_content = create_html_file.create_html_content(param_types, return_types, new_javascript_file_names)
    print("new_html_content", new_html_content)
    new_calculator_article_content = create_article_file.create_article_content(param_types, return_types, new_javascript_file_names, [js_content, new_javascript_content,  new_html_content], allow_ai)
    print("new_calculator_article_content", new_calculator_article_content) # Wrong here.

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
            print(Fore.RED + "Deleted:", file)        

    if run:
        # Open the browser.
        article_local_url = local_url + "calc/" + htmlName
        webbrowser.open(article_local_url)
        print("URL:", article_local_url)
    



def main():
    # TODO: Make in the command prompt you can choose to delete the chosen one?
    run = True  # If I should run the program (True) OR delete the files (False).
    allow_ai = True  # If I should allow AI to write the article.

    print("Welcome to the calculator maker.")

    # ----------- Arguments -----------
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Helps creating the forms for calculators.", add_help=False) # Adding: add_help=False to see if it helps my command. 

    # Add the primary command argument
    parser.add_argument(
        "command",  # The primary command (e.g., test)
        metavar="command",
        type=str,
        help="The primary command to run",
    )

    # Add optional subcommands or flags
    parser.add_argument(
        "-ai",
        action="store_true",  # Flag (True if provided, False otherwise)
        help="Disable AI only.",
    )

    # Add the -d argument as a flag
    parser.add_argument(
        "-d",
        action="store_true",  # Flag (True if provided, False otherwise)
        help="Disable running and AI.",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.d:
        print("Running deleting mode.")
        run = False
        allow_ai = False
    else:
        run = True
        allow_ai = True

    if args.ai:
        print("Disabling AI.")
        allow_ai = False


    # Derive file name from primary command
    command = args.command
    #javascript_file_name = args.command + ".js"

    # Print final settings for confirmation
    print(f"Command: {args.command}")
    print(f"Run: {run}")
    print(f"Allow AI: {allow_ai}")
    #print(f"JavaScript File Name: {javascript_file_name}")


    # ----------- Main -----------

    # TODO: Add so you can either run everything or just the file you want.
    # So you can manually go and delete/add.
    # TODO: Create a list from error.txt
    # If success, add to another txt file? SO I can easily just open up them all.

    if command == "all":
        print(Fore.LIGHTYELLOW_EX + "Running all files.")
        try:
            with open(input_file, "r") as f:
                lines = f.readlines()
            # Open the error file for writing errors
            with open(error_file, "w") as error_log:
                # Loop through each line
                for line in lines:
                    words = line.strip().split()  # Split line into words
                    for javascript_file_name in words:
                        try:
                            # TODO: Check if this works.
                            run_main(javascript_file_name, run, allow_ai)
                            
                        except Exception as e:
                            # Write the problematic word to the error log
                            error_log.write(f"{javascript_file_name}\n")
                            print(Fore.RED + f'Error processing "{javascript_file_name}": {e}')
        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        #javascript_file_name = command + ".js"
        javascript_file_name = command if command.endswith('.js') else command + '.js'
        print(Fore.LIGHTYELLOW_EX + "Running: " + javascript_file_name)
        run_main(javascript_file_name, run, allow_ai)

    # Open vscode. TODO: Check if it works!
"""     subprocess.call(["code", new_form_path])
    subprocess.call(["code", new_html_path])
    subprocess.call(["code", new_calculator_article_path]) """

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