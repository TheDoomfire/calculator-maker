import os
import json
from typing import Dict, Set, Tuple


def get_form_path(base_path: str):
    """
    Normalize and validate the forms directory path.
    
    Args:
        base_path (str): Base directory path for forms
        
    Returns:
        str: Normalized path
    """
    # Normalize path (converts backslashes to forward slashes)
    normalized_path = os.path.normpath(base_path)
    
    # Create directory if it doesn't exist
    if not os.path.exists(normalized_path):
        try:
            os.makedirs(normalized_path)
            print(f"Created directory: {normalized_path}")
        except Exception as e:
            print(f"Error creating directory: {e}")
            return None
            
    return normalized_path



def generate_js_file(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str]):
    """
    Generate a JavaScript file with appropriate imports based on parameter types.
    
    Args:
        params (dict): Dictionary of parameter names and their types
        file_names (dict): Dictionary containing form, file and html names
        base_path (str): Base directory path for forms
    """
    formName = file_names['form']
    htmlName = file_names['html']
    fileName = file_names['file']
    functionName = file_names['function']
        
    # Rest of your existing code...
    # (imports detection, file generation, etc.)
        # Predefined imports to always include
    
    # --------- All Imports --------

    new_javascript_file = """// Local Imports.
import AttachDocumentListener from '/scripts/listeners/attachDocumentListener.js'
import { toggle_class_if_contains_this_text } from '/scripts/dom/ClassToggler.js'
import { generate_main_chart } from '/scripts/charts/mainChart.js'
"""

    # -------- Add imports for all types --------
    all_types = [] # change to "all_input_types"
    all_units = ["share", "unit", "piece"]

    #for pr in params_return:
    print("PARAMS:::", params)
    print("RETURNS:::", returns)
    # TODO: Make so "returns" looks like "params".
    print("Params:", params)

    # For what imports to use.
    params_return = [params, returns]
    for pr in params_return:
        for param in pr:
            print("param:", param)
            if 'element' in param:
                element = param['element']
                if element == 'currency' and not 'currency' in all_types :
                    all_types.append("currency")
                elif element == "percent" and not "percent" in all_types:
                    all_types.append("percent")
                elif element == "share" and not "share" in all_types:
                    all_types.append("share")
                elif element == "table" and not "table" in all_types:
                    all_types.append("table")

    for type in all_types:
        if type == "currency":
            new_javascript_file += "import { prettifyMoney } from '/scripts/formats/Money.js';\n"   
        elif type == "percent":
            new_javascript_file += "import { prettifyPercent } from '/scripts/formats/Percent.js';\n"
        elif type == "table":
            new_javascript_file += "import { arrayToTable } from '/scripts/tables/ArrayToTable.js';\n"
        else:
            new_javascript_file += "import { separateNumber } from '/scripts/formats/SeparateNumber.js';\n"


    new_javascript_file += "\n\n"

    new_javascript_file += f"""AttachDocumentListener({formName});
window.onload = {formName};


function {formName}() {{
\tconst getValue = id => parseFloat(document.getElementById(id).value) || 0;\n
 """
    all_inputs = []
    for param in params:
        if 'name' in param:
            key = param['name']
            new_javascript_file += f"""\tconst {key} = getValue("{key}");\n"""
            all_inputs.append(key)

    all_inputs_string = ", ".join(all_inputs)
    new_javascript_file += f"""\n\tconst results = {functionName}({all_inputs_string});\n\n"""


    tableID = "chart-" + htmlName
    for ret in returns:
        element = ret['element']
        name = ret['name']
        if element == 'currency':
            new_javascript_file += f"""\tdocument.getElementById("{name}").innerHTML = prettifyMoney(results.{name});\n"""
        elif element == "percent":
            new_javascript_file += f"""\tdocument.getElementById("{name}").innerHTML = results.{name};\n"""
        elif element == "table":
            new_javascript_file += f"""\tarrayToTable({name}, {tableID});\n"""


    new_javascript_file +="""\n\n\ttoggle_class_if_contains_this_text();"""

    # Creates a chart.
    chartLabels = []
    chartDataset = []
    chartID = "chart-" + htmlName
    for ret in returns:
        element = ret['element']
        name = ret['name']
        if element == 'currency':
            chartLabels.append(ret['pretty_name'])
            chartDataset.append("results." + name)

    print("chartDataset:", chartDataset)
    chartDataString = ", ".join(chartDataset)

    new_javascript_file += f"""\n\tgenerate_main_chart("{chartID} Chart", "bar", {chartLabels}, [{chartDataString}], "{chartID}");\n"""


    new_javascript_file += f"""\n}};"""
    return new_javascript_file


def create_file(file_content, path, name):
    """
    Creates a file with the given content at the specified path and name.
    If the file already exists, it skips creation and returns a message.

    :param file_content: The content to write into the file.
    :param path: The directory where the file should be created.
    :param name: The name of the file to create.
    :return: A message indicating the result.
    """
    # Ensure the directory exists
    os.makedirs(path, exist_ok=True)
    
    # Full path to the file
    file_path = os.path.join(path, name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        return f"Skipped: File '{file_path}' already exists."
    
    # Create and write content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)
    
    return f"Created: File '{file_path}' has been created."
    
def get_imports(params: dict) -> str:
    """
    Generate JavaScript imports with and without curly braces based on type.
    Consolidates 'share', 'piece', and 'unit' imports.
    """
    # Map types to their imports (path and whether to use curly braces)
    type_to_import = {
        'currency': ('/scripts/formats/Money.js', True),  # True = use {}
        'percentage': ('/scripts/formats/Percent.js', True),
        'share': ('/scripts/formats/SeparateNumber.js', False),  # False = no {}
        'unit': ('/scripts/formats/SeparateNumber.js', False),
        'piece': ('/scripts/formats/SeparateNumber.js', False)
    }
   
    # Predefined imports to always include
    imports = {
        f"import AttachDocumentListener from '/scripts/listeners/attachDocumentListener.js'",
        f"import {{ toggle_class_if_contains_this_text }} from '/scripts/dom/ClassToggler.js'",
        f"import {{ generate_main_chart }} from '/scripts/charts/mainChart.js'"
    }
    
    # Map of custom import names
    import_names = {
        'currency': 'prettifyMoney',
        'percentage': 'prettifyPercent',
        'share': 'separateNumber',
        'unit': 'separateNumber',
        'piece': 'separateNumber'
    }
    
    piece_types = {'share', 'unit', 'piece'}
   
    for param_type in params.values():
        param_type = param_type.lower()
        for type_key, (path, use_braces) in type_to_import.items():
            # Special handling for piece-related types
            if type_key in piece_types and any(piece_type in param_type for piece_type in piece_types):
                if use_braces:
                    imports.add(f"import {{ separateNumber }} from '{path}';")
                else:
                    imports.add(f"import separateNumber from '{path}';")
            # Regular import for other types
            elif type_key in param_type:
                import_name = import_names.get(type_key)
                if use_braces:
                    imports.add(f"import {{ {import_name} }} from '{path}';")
                else:
                    imports.add(f"import {import_name} from '{path}';")
   
    return '\n'.join(sorted(imports)) + '\n' if imports else ''


# Example usage
if __name__ == "__main__":
    params = {
        'sharePrice': 'currency',
        'sharesOutstanding': 'share',
        'capitalInvested': 'currency'
    }
    
    file_names = {
        'form': 'marketValueAddedForm',
        'file': 'marketValueAddedForm.js',
        'html': 'market-value-added'
    }
    
    # Example with different path formats (all will work):
    paths = [
        "D:/src/scripts/forms",
        "D:\\src\\scripts\\forms",
        os.path.join("D:", "src", "scripts", "forms")
    ]
    
    generate_js_file(
        params=params, 
        file_names=file_names,
        base_path=paths[0]  # Choose your preferred path format
    )