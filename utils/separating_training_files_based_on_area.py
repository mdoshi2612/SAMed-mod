import os
import numpy as np
import nibabel as nib
import argparse



def process_npz_files(input_folder, output_folder):
    
    area_number = 0
    
    output_file_path_with_area = os.path.join(output_folder, 'with_area.txt')
    output_file_path_without_area = os.path.join(output_folder, 'without_area.txt')
    
    # Iterate through files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".npz"):
            file_path = os.path.join(input_folder, filename)

            # Load data from npz file
            data = np.load(file_path)
            
            label =  data['label']

            # Check the number of ones in the array
            count_ones = np.sum(label == 1)
            
            if count_ones > 0:
                with open(output_file_path_with_area, 'a') as output_file:
                    output_file.write(os.path.splitext(filename)[0] + '\n')
                    
            else:
                with open(output_file_path_without_area, 'a') as output_file:
                    output_file.write(os.path.splitext(filename)[0] + '\n')

# for pleural effusion training data, out of 6558 images, 2698 contains some area where it is present




if __name__ == "__main__":
    input_folder = "/home/manav/SAMed-mod/Pleural-Effusion/preprocessed_data/training_data"
    output_folder = "/home/manav/SAMed-mod/Pleural-Effusion/lists/main"

    process_npz_files(input_folder, output_folder)