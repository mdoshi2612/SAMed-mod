import os
import numpy as np
import nibabel as nib
import h5py
import argparse

def minmax_scale(data, min_value=-125, max_value=275):
    # Clip the data
    clipped_data = np.clip(data, min_value, max_value)
    
    # Apply min-max scaling
    scaled_data = (clipped_data - min_value) / (max_value - min_value)
    
    return scaled_data

def main(ct_scans_folder, effusions_folder, output_folder, test, min_value = -125, max_value = 275):

    if(test == True):
        save_slice_probability = 0.3
    else:
        save_slice_probability = 0.7

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through ct_scans folder
    for ct_scan_file in os.listdir(ct_scans_folder):
        if ct_scan_file.endswith(".nii"):

            # Construct the paths for ct_scan and effusion files
            ct_scan_path = os.path.join(ct_scans_folder, ct_scan_file)
            base_filename = os.path.splitext(ct_scan_file)[0]
            effusion_file = f"{base_filename}_effusion.nii"
            effusion_path = os.path.join(effusions_folder, effusion_file)

            # Load ct_scan and effusion NIfTI files (3D scan)
            ct_scan_img = nib.load(ct_scan_path)
            effusion_img = nib.load(effusion_path)

            # Get the number of slices
            num_slices = ct_scan_img.shape[-1]

            # Iterate through each slice
            for slice_idx in range(num_slices):
                # Access the slice data
                ct_slice_data = ct_scan_img.get_fdata()[:, :, slice_idx]
                effusion_slice_data = effusion_img.get_fdata()[:, :, slice_idx]

                # Decide whether to save according to train test splits
                if np.random.rand() <= save_slice_probability:
                    file_extension = ".npz"

                    # Construct the output filename
                    output_filename = f"{base_filename}_slice{slice_idx + 1}{file_extension}"
                    output_path = os.path.join(output_folder, output_filename)

                    # Apply min-max scaling to training array
                    scaled_training = minmax_scale(ct_slice_data, min_value, max_value)

                    # Apply min-max scaling to segmentation array
                    scaled_segmentation = minmax_scale(effusion_slice_data, 0, 1)

                    # Save the data based on file extension
                    np.savez(output_path, image=scaled_training, label=scaled_segmentation)
            
                    print(f"{output_filename} was normalized and saved.")

    # Perform any additional operations as needed
    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CT scans and effusion masks slices.")
    parser.add_argument("--ct_scans_folder", type=str, required=True, help="Path to the folder containing CT scans.")
    parser.add_argument("--effusions_folder", type=str, required=True, help="Path to the folder containing effusion masks.")
    parser.add_argument("--output_folder", type=str, required=True, help="Path to the output folder.")
    parser.add_argument("--test", action = 'store_true', help="Probability of saving each slice.")
    parser.add_argument("--min_value", type=float, default=-125, help="Minimum value for scaling.")
    parser.add_argument("--max_value", type=float, default=275, help="Maximum value for scaling.")

    args = parser.parse_args()
    main(args.ct_scans_folder, args.effusions_folder, args.output_folder, args.test, args.min_value, args.max_value)