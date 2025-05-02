from textnode import *
import os
import shutil



static_directory_path = "./static"
public_directory_path = "./public"



def copy_directory_recursive(source, destination, first_level_call=True):
    if not os.path.exists(source):
        raise Exception(f"'{source}' does not exist")

    if first_level_call:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        
        os.mkdir(destination)
    
    for item in os.listdir(source):
        current_source = os.path.join(source, item)
        current_destination = os.path.join(destination, item)
        
        if os.path.isdir(current_source):
            os.mkdir(current_destination)
            copy_directory_recursive(current_source, current_destination, False)
        elif os.path.isfile(current_source):
            shutil.copy(current_source, current_destination)
        else:
            raise Exception("path is neither a file nor a directory")
    

def main():
    print("\ncopying static files to public directory...")
    copy_directory_recursive(static_directory_path, public_directory_path)
    print(f"copied files from '{static_directory_path}' to '{public_directory_path}'\n")
    


if __name__ == "__main__":
    main()