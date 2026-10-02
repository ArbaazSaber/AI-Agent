from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    pwd_path = Path(working_directory).absolute()
    full_path_dir: Path = (pwd_path / file_path).resolve()

    if not full_path_dir.is_relative_to(pwd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if full_path_dir.is_dir():
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    full_path_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(full_path_dir, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file content located at the file_path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
            ),
        },
        required=["file_path", "content"]
    ),
)