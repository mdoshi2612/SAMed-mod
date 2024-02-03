import os
import numpy as np
import argparse

def minmax_scale(data, min_value=-125, max_value=275):
    # Clip the data
    clipped_data = np.clip(data, min_value, max_value)
    
    # Apply min-max scaling
    scaled_data = (clipped_data - min_value) / (max_value - min_value)
    
    return scaled_data

def scale_npz_files(input_folder, output_folder, min_value, max_value):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through NPZ files in the input folder
    for npz_file in os.listdir(input_folder):
        if npz_file.endswith(".npz"):
            # Load NPZ file
            npz_path = os.path.join(input_folder, npz_file)
            data = np.load(npz_path)

            # Apply min-max scaling to training array
            scaled_training = minmax_scale(data['image'], min_value, max_value)

            # Apply min-max scaling to segmentation array
            scaled_segmentation = minmax_scale(data['label'], 0, 1)

            # Save the scaled data to a new NPZ file in the output folder
            output_npz_path = os.path.join(output_folder, npz_file)
            np.savez(output_npz_path, image=scaled_training, label=scaled_segmentation)

            print(f"{npz_file} normalized and saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply min-max scaling to training and segmentation arrays in NPZ files.")
    parser.add_argument("--input_folder", required=True, help="Path to the folder containing NPZ files.")
    parser.add_argument("--output_folder", required=True, help="Path to the folder to save scaled NPZ files.")
    parser.add_argument("--min_value", type=float, default=-125, help="Minimum value for scaling.")
    parser.add_argument("--max_value", type=float, default=275, help="Maximum value for scaling.")
    args = parser.parse_args()

    scale_npz_files(args.input_folder, args.output_folder, args.min_value, args.max_value)
