from filters.filter_1_fetch_issuers import fetch_issuers
from filters.filter_2_check_last_date import get_last_date
from filters.filter_3_fill_missing_data import fill_missing_data
from filters.filter_4_timer import start_timer, stop_timer, log_time
from setup.csv_handler import save_to_csv
from selenium import webdriver

def main():
    start_time = start_timer()

    driver = webdriver.Firefox()
    driver.get("https://www.mse.mk/en/stats/symbolhistory/kmb")

    issuers = fetch_issuers()

    for issuer in issuers:
        last_date = get_last_date(issuer, "data.csv")
        data = fill_missing_data(driver, issuer, last_date)
        save_to_csv(data, "data.csv")

    driver.quit()

    elapsed_time = stop_timer(start_time)
    log_time(elapsed_time)

if __name__ == "__main__":
    main()