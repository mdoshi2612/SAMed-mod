import os
import argparse
import random

def list_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return files

def write_to_txt(file_list, output_file):
    with open(output_file, 'w') as f:
        for file_name in file_list:
            file_name_without_extension, _ = os.path.splitext(file_name)
            f.write(f"{file_name_without_extension}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files in a folder, write to a text file, and select a random number of files.")
    parser.add_argument("--input_folder", required=True, help="Path to the folder to list files from.")
    parser.add_argument("--output_txt", required=True, help="Path to the output text file.")
    parser.add_argument("--num_random_files", type=int, required=True, help="Number of files to randomly select.")
    args = parser.parse_args()

    folder_path = args.input_folder
    output_txt_file = args.output_txt
    num_random_files = args.num_random_files
    
    output_folder = os.path.dirname(output_txt_file)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    files_list = list_files(folder_path)

    print(f"\nTotal files in {folder_path}: {len(files_list)}")
    

    # Select a random number of files
    selected_files = random.sample(files_list, min(num_random_files, len(files_list)))

    print("\nSelected random files:")
    for file_name in selected_files:
        print(file_name)

    write_to_txt(selected_files, output_txt_file)
    print(f"\nRandomly selected file list written to {output_txt_file}.")
