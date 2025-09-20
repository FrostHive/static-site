import os
import shutil
from generate_page import generate_page

def main():
    transfer_files_to_public()
    generate_page("./content/index.md", "./template.html", "./public/index.html")


def transfer_files_to_public():
    public_path = os.path.abspath("./public")
    static_path = os.path.abspath("./static")

    if os.path.exists(public_path):
        print(f"{public_path} deleted.")
        shutil.rmtree(public_path)

    os.mkdir(public_path)
    print(f"{public_path} created.")

    for item in os.listdir(static_path):
        transfer_file(item, public_path, static_path)
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
