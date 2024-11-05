import pandas as pd
import os

data_folder = '../data/'


def read_file_info(file_df_list):
    # Read the first row of the df
    info_df = file_df_list[0]
    site_name = info_df.iloc[0, 1]


    print("File information (first row):\n", df_info)
    exit()


# For all folders in data folder
for site_folder in os.listdir(data_folder):
    # Sanity check (.DS_Store and other hidden files)
    if site_folder.startswith('.'):
        continue

    # Path to raw files
    raw_folder = os.path.join(data_folder, site_folder, 'raw')
    if not os.path.exists(raw_folder):
        print(f"Raw folder not found for site: {site_folder}")
        continue

    # For all files in raw
    for file in os.listdir(raw_folder):
        # Construct full file path
        file_path = os.path.join(raw_folder, file)

        try:
            df_list = pd.read_html(file_path)
            read_file_info(df_list)

            # Save cleaned file (optional, uncomment to use)
            # clean_folder = os.path.join(data_folder, site_folder, 'class')
            # os.makedirs(clean_folder, exist_ok=True)
            # output_path = os.path.join(clean_folder, f"{os.path.splitext(file)[0]}.csv")
            # df.to_csv(output_path, index=False)

        except Exception as e:
            print(f"Error reading {file_path}: {e}")
