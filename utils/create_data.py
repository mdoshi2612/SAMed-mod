import os
import numpy as np
import nibabel as nib
import h5py

ct_scans_folder = "../ct_scans"
effusions_folder = "../effusion_masks"
output_folder_npz = "../training_data"
output_folder_npyh5 = "../testing_data"

# Probability of saving as .npz file
save_npz_probability = 0.7

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

            # Decide whether to save as .npz or .npy.h5 based on probabilities
            save_as_npz = np.random.rand() <= save_npz_probability
            file_extension = ".npz" if save_as_npz else ".npy.h5"

            # Choose the output folder based on file extension
            output_folder = output_folder_npz if save_as_npz else output_folder_npyh5

            # Construct the output filename
            output_filename = f"{base_filename}_slice{slice_idx + 1}{file_extension}"
            output_path = os.path.join(output_folder, output_filename)

            # Save the data based on file extension
            if file_extension == ".npz":
                np.savez(output_path, image=ct_slice_data, label=effusion_slice_data)
            else:
                with h5py.File(output_path, "w") as hf:
                    hf.create_dataset("image", data=ct_slice_data)
                    hf.create_dataset("label", data=effusion_slice_data)

# Perform any additional operations as needed
print("Processing complete.")
