import subprocess
import os
from typing import List, Dict
from userpaths import get_my_documents
from src.config_loader import output_dir, input_dir


# def process_local(output_dir: str, num_processes: int, input_path: str = get_my_documents()):

def process_local(output_path: str, num_processes: int, input_path: str):
    command = [
        "unstructured-ingest",
        "local",
        "--input-path", input_path,
        "--output-dir", output_path,
        "--num-processes", str(num_processes),
        "--recursive",
        "--verbose",
    ]

    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    print(process)
    output, error = process.communicate()

    # Print output
    if process.returncode == 0:
        print('Command executed successfully. Output:')
        print(output.decode())
    elif error is not None:
        print(error.decode())
    else:
        print("No error message available.")


def get_result_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


print(input_dir)
print(output_dir)
print(process_local(output_path=output_dir, num_processes=2, input_path=input_dir))
files = get_result_files(output_dir)
print(files)
