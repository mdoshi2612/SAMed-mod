import os
import re
import argparse
import matplotlib.pyplot as plt


directory_mean_dice_dict = {}

def extract_mean_dice(log_file_path):
    try:
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.read()
            
            second_last_line = log_data.split('\n')[-3]
            

            # Regular expression pattern to match mean_dice value
            pattern = r"mean_dice : (\d+\.\d+)"
            mean_dice_value = re.search(pattern, second_last_line)

            if mean_dice_value:
                return float(mean_dice_value.group(1))
            else:
                return None
    except Exception as e:
        print("Error occurred while extracting mean_dice value:", e)
        return None

def plot_directory_vs_loss(directory_mean_dice_dict):
    directory_names = list(directory_mean_dice_dict.keys())
    mean_dice_values = list(directory_mean_dice_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.plot(directory_names, mean_dice_values, marker='o', linestyle='-')
    plt.title('Directory vs. Mean Dice Value')
    plt.xlabel('Directory')
    plt.ylabel('Mean Dice Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main(directory):


    for root, dirs, files in os.walk(directory):
        if 'test' in dirs:
            test_log_dir = os.path.join(root, 'test', 'test_log')
            if os.path.exists(test_log_dir):
                log_file_path = os.path.join(test_log_dir, 'log.txt')
                if os.path.isfile(log_file_path):
                    mean_dice = extract_mean_dice(log_file_path)
                    if mean_dice is not None:
                        directory_name = os.path.basename(root)
                        directory_mean_dice_dict[directory_name] = mean_dice

    if directory_mean_dice_dict:
        plot_directory_vs_loss(directory_mean_dice_dict)
    else:
        print("No log files found or mean dice values extracted.")
       
    print(directory_mean_dice_dict)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot directory vs. mean dice value")
    parser.add_argument("directory", help="Directory path")
    args = parser.parse_args()

    main(args.directory)
