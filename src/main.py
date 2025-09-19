import os
import shutil

def main():
    transfer_files_to_public()

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
    if os.path.isfile(file):
        print(f"New file for {current_path}: {file}")
        shutil.copy(file, current_path)
    else:
        new_path = os.path.join(current_path, file)
        old_directory = os.path.join(old_path, file)
        os.mkdir(new_path)
        print(f"New directory made: {new_path}")
        for item in os.listdir(new_path):
            transfer_file(item, new_path, old_directory)
    return

main()
