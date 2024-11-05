import os
import pandas as pd
from bs4 import BeautifulSoup

# DATA_FOLDER = '../data/class_debug/'
DATA_FOLDER = '../data/class_raw/'
SAVE_FOLDER = '../data/data_processed/'
PARSE_KEYWORDS = ['All Eastbound', 'All Westbound', 'All Northbound', 'All Southbound']


def parse_table(table, keywords=None):
    if keywords is None:
        keywords = PARSE_KEYWORDS
    df_dict = {}

    # Extract rows and manage colspan issues
    rows = []
    for row in table.find_all("tr"):
        cells = []
        for cell in row.find_all(["th", "td"]):
            # Add colspan handling
            colspan = int(cell.get("colspan", 1))
            cells.extend([cell.text.strip()] * colspan)
        rows.append(cells)

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows)

    # For each keyword, find the row index and extract the next 25 rows if the keyword is found
    for keyword in keywords:
        if keyword not in df.iloc[:, 0].to_string():
            continue
        else:
            print(f"Keyword '{keyword}' found in the table.")

        keyword_indices = df.index[df.iloc[:, 0].str.contains(keyword, na=False)].tolist()

        for index in keyword_indices:
            # Extract the next 25 rows after the keyword row
            extracted_df = df.iloc[index + 1:index + 26]
            # Set the first row of extracted_df as the column headers and remove it from the data
            extracted_df.columns = extracted_df.iloc[0]
            extracted_df = extracted_df[1:]
            # Add to df_dict
            if keyword not in df_dict:
                df_dict[keyword] = extracted_df

    return df_dict


def parse_html_file(file_path):
    """Parse the HTML file to extract title, site name, and date information."""
    # Load and parse the HTML content
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract title and parse it for site name and date
    title = soup.find('title').text.strip()
    site_name = title.split(' ')[2]
    date = ' '.join(title.split(' ')[-3:])

    print(f"\033[1m* {title} *\033[0m")
    print(f"Site Name: {site_name}, Date: {date}")

    # Find all tables
    tables = soup.find_all('table')
    # If the table contains the keyword 'All Eastbound' or 'All Westbound', parse it
    for table in tables:
        # if 'All Eastbound' in table.text or 'All Westbound' in table.text:
        if any(keyword in table.text for keyword in PARSE_KEYWORDS):
            df_dict = parse_table(table)

            # Save the dataframes to CSV files
            os.makedirs(os.path.join(SAVE_FOLDER, site_name, 'class'), exist_ok=True)
            for keyword, df_parsed in df_dict.items():
                output_path = os.path.join(SAVE_FOLDER, site_name, 'class', f'{site_name}_{date}_{keyword}.csv')
                df_parsed.to_csv(output_path, index=False)
                print(f"CSV file saved: {output_path}")

            break

    print("-" * 50)


def process_site_folder(site_folder):
    """Process each HTML file in the specified site's 'raw' subfolder."""
    raw_folder = os.path.join(DATA_FOLDER, site_folder)

    # Check if the 'raw' folder exists
    if not os.path.exists(raw_folder):
        print(f"Raw folder not found for site: {site_folder}")
        return

    # Process each file in the 'raw' folder
    for file_name in os.listdir(raw_folder):
        # Skip hidden files
        if file_name.startswith('.'):
            continue

        file_path = os.path.join(raw_folder, file_name)
        try:
            parse_html_file(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")


def main():
    """Main function to process each site folder within the data directory."""
    for site_folder in os.listdir(DATA_FOLDER):
        # Skip hidden files or folders
        if site_folder.startswith('.'):
            continue
        process_site_folder(site_folder)


if __name__ == '__main__':
    main()
