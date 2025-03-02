import os
import shutil

def clean_converted_directory():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    converted_dir = os.path.join(base_dir, 'converted')

    if os.path.exists(converted_dir):
        for root, dirs, files in os.walk(converted_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                    for sub_file in sub_files:
                        sub_file_path = os.path.join(sub_root, sub_file)
                        os.remove(sub_file_path)

if __name__ == "__main__":
    clean_converted_directory()