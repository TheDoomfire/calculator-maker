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



def generate_js_file(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str], base_path: str):
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

    # Get normalized path
    output_dir = get_form_path(base_path)
    if not output_dir:
        return False
        
    file_path = os.path.join(output_dir, file_names['file'])
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"File {file_path} already exists. Skipping creation.")
        return False

        
    # Rest of your existing code...
    # (imports detection, file generation, etc.)
        # Predefined imports to always include
    
    # --------- All Imports --------

    new_javascript_file = """// Local Imports.
import AttachDocumentListener from '/scripts/listeners/attachDocumentListener.js'
import {{ toggle_class_if_contains_this_text }} from '/scripts/dom/ClassToggler.js'
import {{ generate_main_chart }} from '/scripts/charts/mainChart.js'
"""

    # -------- Add imports for all types --------
    all_types = []
    all_units = ["share", "unit", "piece"]
    params_return = [params, returns]

    #for pr in params_return:
    print("PARAMS:::", params)
    print("RETURNS:::", returns)
    # TODO: Make so "returns" looks like "params".
    for param_type in params.values():
        param_type = param_type.lower()
        if param_type == "currency" and not "currency" in all_types:
            all_types.append("currency")
        elif param_type == "percentage" and not "percentage" in all_types:
            all_types.append("percentage")
        elif param_type in all_units and param_type not in all_types:
            all_types.append("share")

    for type in all_types:
        print(type)
        if type == "currency":
            new_javascript_file += "import { prettifyMoney } from '/scripts/formats/Money.js';\n"   
        elif type == "percentage":
            new_javascript_file += "import { prettifyPercent } from '/scripts/formats/Percent.js';\n"
        elif type == "share":
            new_javascript_file += "import { separateNumber } from '/scripts/formats/SeparateNumber.js';\n"

    new_javascript_file += "\n\n"

    new_javascript_file += "window.onload = " + formName + "\n\n"

    new_javascript_file += f"""AttachDocumentListener({formName});
window.onload = {formName};


function {formName}() {{
\tconst getValue = id => parseFloat(document.getElementById(id).value) || 0;

}}
 """
    all_inputs = []
    for key, value in params.items():
        new_javascript_file += f"""\tconst {key} = getValue("{key}");\n"""
        all_inputs.append(key)

    all_inputs_string = ", ".join(all_inputs)
    new_javascript_file += f"""\n\tconst results = {functionName}({all_inputs_string});"""

    # TODO: Get all the export names.
    


    return new_javascript_file


    
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