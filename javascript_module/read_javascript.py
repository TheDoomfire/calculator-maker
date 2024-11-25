import os

def read_js_file(folder_path, js_filename):
    """
    Read the contents of a specific JavaScript file from a predetermined folder.
    
    Args:
        folder_path (str): Path to the folder containing the JavaScript file
        js_filename (str): Name of the JavaScript file to read
    
    Returns:
        str: Contents of the JavaScript file
        None: If file is not found or cannot be read
    """
    try:
        file_path = os.path.join(folder_path, js_filename)
        with open(file_path, 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error reading file: {e}")
        return None

# Example usage
# js_content = read_js_file("/path/to/folder", "example.js")