import os
import argparse
import random
            
## example command - python3 utils/create_list.py --input_file_1 /home/manav/SAMed-mod/Pleural-Effusion/lists/main/with_area.txt --input_file_2 /home/manav/SAMed-mod/Pleural-Effusion/lists/main/without_area.txt --output_txt /home/manav/SAMed-mod/Pleural-Effusion/lists/Train200_200/train.txt --num_files_from_1 200 --num_files_from_2 200

def read_file_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
    
def select_random_files(file_list, num_files):
    return random.sample(file_list, min(num_files, len(file_list)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files in a folder, write to a text file, and select a random number of files.")
    parser.add_argument("--train_list", required=True, help="Path to the folder to list files from.")
    parser.add_argument("--test_list", required=True, help="Path to the folder to list files from.")
    parser.add_argument("--output_dir", required=True, help="Path to the output text file.")
    parser.add_argument("--train_samples", type=int, help="Number of files to randomly select form file 1.")
    parser.add_argument("--test_samples", type=int, help="Number of files to randomly select from file 2.")
    args = parser.parse_args()
    
    
    files_from_1 = read_file_list(args.input_file_1)
    files_from_2 = read_file_list(args.input_file_2)
    
    selected_files_from_1 = select_random_files(files_from_1, args.num_files_from_1)
    selected_files_from_2 = select_random_files(files_from_2, args.num_files_from_2)
    
    print("files selected from 1" , len(selected_files_from_1))
    print("files selected from 2" , len(selected_files_from_2))
    
    selected_files = selected_files_from_1 + selected_files_from_2
    
    print ('total filed selected', len(selected_files))



    with open(os.path.join(args.output_txt, 'train.txt'), 'w') as output_file:
        for file_name in selected_files:
            output_file.write(file_name + '\n')
