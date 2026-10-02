import subprocess

from pathlib import Path
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    pwd_path = Path(working_directory).absolute()
    full_path_dir: Path = (pwd_path / file_path).resolve()

    if not full_path_dir.is_relative_to(pwd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not full_path_dir.is_file():
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if full_path_dir.suffix != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", full_path_dir]
    if args:
        command.extend(args)
    try:
        completed_subprocess = subprocess.run(
            command,
            cwd=pwd_path,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        ans_str = []
        
        if completed_subprocess.returncode != 0:
            ans_str.append(f"Process exited with code with {completed_subprocess.returncode}")
        if not (completed_subprocess.stderr or completed_subprocess.stdout):
            ans_str.append("No output produced")
        if completed_subprocess.stdout:
            ans_str.append(f"STDOUT: {completed_subprocess.stdout}")
        if completed_subprocess.stderr:
            ans_str.append(f"STDERR: {completed_subprocess.stderr}")
        return "\n".join(ans_str)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file located at the file_path relative to the working directory, along with any arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional Arguments parameter for running the python file",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
        required=["file_path"]
    ),
)