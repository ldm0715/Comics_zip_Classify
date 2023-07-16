import os
import shutil

def move_files(source_folder, destination_folder):
    files = os.listdir(source_folder)
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder)
        if os.path.isdir(source_path):
            print("文件夹：", file)
            move_files(source_path, destination_path)
        else:
            shutil.move(source_path, destination_path)
            print(f"Moved file: {file}")

source_folder = r"F:\分类结果"
destination_folder = r"F:\分类结果1"
move_files(source_folder, destination_folder)
