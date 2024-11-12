from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

WAIT_TIME = 10  # seconds


def configure_driver(download_directory="."):
    """Configure and return a Chrome WebDriver instance with download options."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def generate_url(site, date_str_start, date_str_end, data_type):
    """Generate the appropriate URL based on data type and date range."""
    base_url = "https://gdottrafficdata.drakewell.com/"
    site_id = site.replace('-', '').zfill(12)

    if data_type == "class":
        url = f"{base_url}tfreport.asp?node=GDOT_CCS&cosit={site_id}&reportdate={date_str_start}&enddate={date_str_end}&dimtype=2&dir=%2D4&excel=1"
    elif data_type == "speed":
        url = f"{base_url}tfweekspeed.asp?node=GDOT_CCS&cosit={site_id}&reportdate={date_str_start}&enddate={date_str_end}&dimtype=3&dir=%2D3&excel=1"
    else:
        raise ValueError("Invalid data type specified. Choose 'class' or 'speed'.")
    return url


def download_data(driver, site, start_date, end_date, data_type):
    """Automate downloads for traffic data between a start date and an end date."""
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end:
        date_str_start = current_date.strftime("%Y-%m-%d")

        if data_type == "class":
            date_str_end = date_str_start
            current_date += timedelta(days=1)
        elif data_type == "speed":
            # The download end date should be the next Saturday
            days_delta = 5 - current_date.weekday() if current_date.weekday() <= 5 else 6
            date_download_end = min(current_date + timedelta(days=days_delta), end)
            date_str_end = date_download_end.strftime("%Y-%m-%d")
            current_date = date_download_end + timedelta(days=1)
        else:
            raise ValueError("Invalid data type specified. Choose 'class' or 'speed'.")

        url = generate_url(site, date_str_start, date_str_end, data_type)
        driver.get(url)
        print(f"Opening {url}")
        time.sleep(WAIT_TIME)


def download_with_selenium(site, start_date, end_date, data_type):
    """Main function to download data using Selenium with the specified parameters."""
    driver = configure_driver()
    try:
        download_data(driver, site, start_date, end_date, data_type)
        print("All downloads completed.")
    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == '__main__':
    # Define download parameters
    site = "067-2373"
    start_date = "2024-03-10"
    end_date = "2024-03-18"
    data_type = "speed"  # "class" or "speed"

    download_with_selenium(site, start_date, end_date, data_type)
