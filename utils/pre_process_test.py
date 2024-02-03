import os
import h5py
import numpy as np
import argparse

def minmax_scale(data, min_value=-125, max_value=275):
    # Clip the data
    clipped_data = np.clip(data, min_value, max_value)
    
    # Apply min-max scaling
    scaled_data = (clipped_data - min_value) / (max_value - min_value)
    
    return scaled_data

def scale_h5_files(input_folder, output_folder, min_value, max_value):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through HDF5 files in the input folder
    for h5_file in os.listdir(input_folder):
        if h5_file.endswith(".h5"):
            # Load HDF5 file
            h5_path = os.path.join(input_folder, h5_file)
            
            with h5py.File(h5_path, 'r') as hf:
                # Extract the data and label images
                data_image = hf['image']
                label_image = hf['label']
                
                # Apply min-max scaling to each channel for both images
                scaled_data_image = minmax_scale(data_image, min_value, max_value)
                scaled_label_image = minmax_scale(label_image, 0, 1)

                # Extract the number of slices
                num_slices = data_image.shape[2]

                # Iterate through each slice
                for slice_idx in range(num_slices):
                    # Extract individual slices
                    data_slice = scaled_data_image[:, :, slice_idx]
                    label_slice = scaled_label_image[:, :, slice_idx]

                    # Save each slice to a new NPZ file
                    output_npz_filename = f"{os.path.splitext(h5_file)[0]}_slice{slice_idx + 1}.npz"
                    output_npz_path = os.path.join(output_folder, output_npz_filename)
                    np.savez(output_npz_path, image=data_slice, label=label_slice)

                    print(f"{output_npz_filename} was normalized and saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply min-max scaling to slices in HDF5 files.")
    parser.add_argument("--input_folder", required=True, help="Path to the folder containing HDF5 files.")
    parser.add_argument("--output_folder", required=True, help="Path to the folder to save scaled NPZ files.")
    parser.add_argument("--min_value", type=float, default=-125, help="Minimum value for scaling.")
    parser.add_argument("--max_value", type=float, default=275, help="Maximum value for scaling.")
    args = parser.parse_args()

    scale_h5_files(args.input_folder, args.output_folder, args.min_value, args.max_value)
