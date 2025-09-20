import os
import shutil
import sys
from generate_page import generate_pages_recursive



def main():
    base_path = "/"
    if len(sys.argv) >= 2:
        base_path = sys.argv[1]
    transfer_files_to_public(base_path)
    generate_pages_recursive(f"{base_path}content", f"{base_path}template.html", f"{base_path}docs", base_path)


def transfer_files_to_public(path):
    docs_path = os.path.abspath(f"{path}docs")
    static_path = os.path.abspath(f"{path}static")

    if os.path.exists(docs_path):
        print(f"{docs_path} deleted.")
        shutil.rmtree(docs_path)

    os.mkdir(docs_path)
    print(f"{docs_path} created.")

    for item in os.listdir(static_path):
        transfer_file(item, docs_path, static_path)
    return

def transfer_file(file, current_path, old_path):
    new_path = os.path.join(current_path, file)
    old_directory = os.path.join(old_path, file)
    if os.path.isfile(old_directory):
        print(f"New file for {current_path}: {file}")
        shutil.copy(old_directory, current_path)
    else:
        os.mkdir(new_path)
        print(f"New directory made: {new_path}")
        for item in os.listdir(old_directory):
            transfer_file(item, new_path, old_directory)
    return

main()
