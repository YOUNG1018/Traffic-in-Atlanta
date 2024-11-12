from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

WAIT_TIME = 10  # seconds


def download_with_selenium(site, start_date, end_date, data_type):
    """Automate downloads for traffic data between a start date and an end date."""

    # Configure Chrome options for downloading
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": ".",  # Set your preferred directory
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Parse the start and end dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if data_type == "class":
        current_date = start
        while current_date <= end:
            # Format the current date as a string
            date_str = current_date.strftime("%Y-%m-%d")

            # Generate the URL for the current date range
            url_string = f"https://gdottrafficdata.drakewell.com/tfreport.asp?node=GDOT_CCS&cosit={site.replace('-', '').zfill(12)}&reportdate={date_str}&enddate={date_str}&dimtype=2&dir=%2D4&excel=1"
            # elif data_type == "speed":
            #     url_string = f"https://gdottrafficdata.drakewell.com/tfreport.asp?node=GDOT_CCS&cosit={site.replace('-', '').zfill(12)}&reportdate={date_str}&enddate={date_str}&dimtype=3"

            # Open the URL in the browser
            driver.get(url_string)
            print(f"Opening {url_string}")

            # Wait for the download to complete or for CAPTCHA interaction
            time.sleep(WAIT_TIME)  # Adjust if necessary based on download speed and CAPTCHA needs

            # Move to the next day
            current_date += timedelta(days=1)

    elif data_type == "speed":
        current_date = start
        while current_date <= end:
            # Format the current date as a string
            # Download by week: No matter the current_date, the date_str_end will be the next Saturday of current_date, if it is before the end_date
            date_str_start = current_date.strftime("%Y-%m-%d")
            days_delta = 5 - current_date.weekday() if current_date.weekday() <= 5 else 6
            date_download_end = current_date + timedelta(days=days_delta)
            if date_download_end > end:
                date_download_end = end
            date_str_end = date_download_end.strftime("%Y-%m-%d")

            # Generate the URL for the current date range
            url_string = f"https://gdottrafficdata.drakewell.com/tfweekspeed.asp?node=GDOT_CCS&cosit={site.replace('-', '').zfill(12)}&reportdate={date_str_start}&enddate={date_str_end}&dimtype=3&dir=%2D3&excel=1"

            # Open the URL in the browser
            driver.get(url_string)
            print(f"Opening {url_string}")

            # Wait for the download to complete or for CAPTCHA interaction
            time.sleep(WAIT_TIME)

            # Move to the next week
            current_date = date_download_end + timedelta(days=1)

    # Close the WebDriver after all downloads are complete
    driver.quit()
    print("All downloads completed and browser closed.")


if __name__ == '__main__':
    # data_type = "class"
    data_type = "speed"
    site = "067-2373"
    start_date = "2024-03-10"
    end_date = "2024-03-18"
    download_with_selenium(site, start_date, end_date, data_type)
