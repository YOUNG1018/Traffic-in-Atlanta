import os
from datetime import datetime
import pandas as pd

DATA_FOLDER = '../data/data_processed/'
SAVE_FOLDER = '../data/'


def join_site(site_folder):
    """Join all CSV files in the specified site's 'class' and 'speed' subfolder."""

    # Process 'class' first
    class_folder = os.path.join(DATA_FOLDER, site_folder, 'class')

    # Check if the 'class' folder exists
    if not os.path.exists(class_folder):
        print(f"Class folder not found for site: {site_folder}")
        return

    # Process each file in the 'class' folder
    dfs = []
    for file_name in os.listdir(class_folder):
        # Skip hidden files
        if file_name.startswith('.'):
            continue

        # Parse file_name to get the date, site and direction
        site_name = file_name.split('_')[0]
        date = file_name.split('_')[1]
        direction = file_name.split('_')[2].split('.')[0].split(' ')[-1]

        file_path = os.path.join(class_folder, file_name)
        try:
            df = pd.read_csv(file_path)
            # Add columns for site and date
            df['site'] = site_name
            df['date'] = date
            df['direction'] = direction
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Concatenate all dataframes
    df_site = pd.concat(dfs, ignore_index=True)

    # first colomn is unnamed, name it 'time'
    df_site.rename(columns={'Unnamed: 0': 'time'}, inplace=True)

    # Add 'Speed' columns
    df_site['Speed'] = None

    # Process 'speed' next
    speed_folder = os.path.join(DATA_FOLDER, site_folder, 'speed')

    # Check if the 'speed' folder exists
    if not os.path.exists(speed_folder):
        print(f"Speed folder not found for site: {site_folder}")
        return

    # Process each file in the 'speed' folder
    for file_name in os.listdir(speed_folder):
        # Skip hidden files
        if file_name.startswith('.'):
            continue

        # Parse file_name to get the date
        site_name = file_name.split('_')[0]
        date = file_name.split('_')[1]
        direction = file_name.split('_')[2].split('.')[0].split(' ')[-1]

        file_path = os.path.join(speed_folder, file_name)

        try:
            df = pd.read_csv(file_path)
            # first colomn is unnamed, name it 'time'
            df.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
            # Add values to 'Speed' and 'Speed Limit' columns
            # Iterate df by row (time) and column (date)
            for index, row in df.iterrows():
                for col in df.columns[1:8]:
                    # Locate to the cell by site, date, direction, and time
                    df_site.loc[(df_site['site'] == site_name) & (df_site['date'].apply(lambda x: datetime.strptime(x, '%B %d, %Y').strftime('%Y-%m-%d')) == datetime.strptime(col, '%Y-%m-%d').strftime('%Y-%m-%d')) & (df_site['direction'] == direction) & (df_site['time'] == row['time']), 'Speed'] = row[col]
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return df_site


def main():
    """Main function to process each site folder within the data directory."""
    # Join all df_site into one dataframe
    dfs = []

    for site_folder in os.listdir(DATA_FOLDER):
        # Skip hidden files or folders
        if site_folder.startswith('.'):
            continue
        df_site = join_site(site_folder)
        dfs.append(df_site)
        print(f"Site folder joined: {site_folder}")

    df_all = pd.concat(dfs, ignore_index=True)

    # Clean df_all dataframe
    # Move 'site' and 'date' columns to the fist and second columns and keep the rest of the columns in the same order
    df_all = df_all[['site', 'date', 'direction'] + [col for col in df_all.columns if col not in ['site', 'date', 'direction']]]

    # Save the joined dataframe to a CSV file
    df_all.to_csv(os.path.join(SAVE_FOLDER, 'all_sites_class_speed.csv'), index=False)


if __name__ == '__main__':
    main()