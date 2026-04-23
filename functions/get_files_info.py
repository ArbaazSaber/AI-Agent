from pathlib import Path

def get_files_info(working_directory, directory="."):
    pwd_path = Path(working_directory).absolute()
    full_path_dir = (pwd_path / directory).resolve()

    if not full_path_dir.is_dir():
        return f'Error: "{directory}" is not a directory'

    if not full_path_dir.is_relative_to(pwd_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    items_metadata = []
    try:
        for item in full_path_dir.rglob("*"):
            items_metadata.append(f"{item.name}: file_size={item.stat().st_size} bytes, is_dir={item.is_dir()}")
    except Exception as e:
        return str(e)
    return "\n".join(items_metadata)