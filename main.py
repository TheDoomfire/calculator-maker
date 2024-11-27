# Local Imports
from javascript_module import read_javascript, get_types_javascript, create_js_form
from formats import format_for_javascript
from html_module import create_html_file


javascript_folder_path = r"D:\Documents\GitHub\chooseinvesting\src\scripts\calc"
javascript_file_name = "compoundAnnualGrowthRate.js" # compoundAnnualGrowthRate.js marketValueAdded.js
forms_path = r"D:\Documents\GitHub\chooseinvesting\src\scripts\forms"


percentages = ["percent", "percentage"]
currencies = ["price", "capital"]
shares = ["share", "shares"]

# Get all Inputs - add elementType
# Get all returns - add elementType
# Split returns, numbers and additionalData. Like "table"



def main():
    print("Running the main app.")
    # Read the javascript file
    js_content = read_javascript.read_js_file(javascript_folder_path, javascript_file_name)
    print(js_content)
    # Get the types of the parameters and return value
    param_types = get_types_javascript.extract_param_types(js_content) # ERROR HERE?
    print("Parameters:")
    print(param_types)

    # TODO: Make this also return the export type. Like "table", "percentage", "currency", "share", "custom"
    return_types = get_types_javascript.extract_return_type(js_content)
    print("All Returns:")
    print(return_types)
    print("-------------")

    # TODO: Add pretty name?
    new_javascript_file_names = format_for_javascript.format_js_function_name(javascript_file_name)
    fileName = new_javascript_file_names['file'] # New file name for example "nameForm.js"
    #formName = new_javascript_file_names['form'] # New file name for example "nameForm"
    #htmlName = new_javascript_file_names['html'] # New file name for example "name-form"
    print("new_javascript_file_names")
    print(new_javascript_file_names)

    print("Creating JS file.")
    new_javascript_content = create_js_form.generate_js_file(param_types, return_types, new_javascript_file_names)
    print("new_javascript_content:")
    print(new_javascript_content)

    new_html_content = create_html_file.create_html_content(param_types, return_types, new_javascript_file_names)
    print("HTML:")
    print(new_html_content)

    # TODO: Add new_html_content so it gets created to.
    # Creates the form javascript file.
"""     new_form_path = create_js_form.create_file(new_javascript_content, forms_path, fileName)
    if new_form_path:
        print("New file created at:", new_form_path) """

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