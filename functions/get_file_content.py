from pathlib import Path
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    pwd_path = Path(working_directory).absolute()
    full_path_dir = (pwd_path / file_path).resolve()

    if not full_path_dir.is_relative_to(pwd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if full_path_dir.is_dir():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    content = None
    try:
        with open(full_path_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {str(e)}"
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the file content of a file relative to the working directory upto 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the file content, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)