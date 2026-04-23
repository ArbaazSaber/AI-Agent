from pathlib import Path

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