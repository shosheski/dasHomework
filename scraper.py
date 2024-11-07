from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

url = "https://www.mse.mk/en/stats/symbolhistory/kmb"
csv_file_path = "data.csv"

def setup_driver():
    driver_path = "C://Users/goraz/Desktop/geckodriver.exe"
    firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    options = Options()
    options.binary_location = firefox_binary_path
    service = Service(executable_path=driver_path)

    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    return driver

def fetch_issuer_codes(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Code")))
    driver.find_element(By.CSS_SELECTOR, "input[onclick='return btnClick();']").click()

    dropdown = driver.find_element(By.ID, "Code")
    select = Select(dropdown)

    codes = [option.get_attribute("value") for option in select.options if option.get_attribute("value").isalpha()]
    return codes

def fetch_issuer_data(driver, issuer_code):
    data_rows = []
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=365 * 10)
    current_start_date = start_date
    seen_dates = set()

    select = Select(driver.find_element(By.ID, "Code"))
    select.select_by_value(issuer_code)

    driver.find_element(By.CSS_SELECTOR, "input[onclick='return btnClick();']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultsTable")))

    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=364), end_date)

        from_date_input = driver.find_element(By.ID, "FromDate")
        to_date_input = driver.find_element(By.ID, "ToDate")

        from_date_input.clear()
        from_date_input.send_keys(current_start_date.strftime("%m/%d/%Y"))
        to_date_input.clear()
        to_date_input.send_keys(current_end_date.strftime("%m/%d/%Y"))

        driver.find_element(By.CSS_SELECTOR, "input[onclick='return btnClick();']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultsTable")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", {"id": "resultsTable"})

        if table:
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")

                if cells and len(cells) >= 9:
                    def clean_text(cell):
                        return cell.text.strip() if cell.text.strip() else "/"

                    date = clean_text(cells[0])
                    if date not in seen_dates:
                        seen_dates.add(date)
                        data_rows.append({
                            "issuer_code": issuer_code,
                            "date": date,
                            "last_transaction_price": clean_text(cells[1]),
                            "max_price": clean_text(cells[2]),
                            "min_price": clean_text(cells[3]),
                            "average_price": clean_text(cells[4]),
                            "percent_change": clean_text(cells[5]),
                            "quantity": clean_text(cells[6]),
                            "best_trading_volume": clean_text(cells[7]),
                            "total_turnover": clean_text(cells[8])
                        })

        current_start_date += timedelta(days=365)
        time.sleep(1)

    data_rows.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y") if x["date"] != "/" else datetime.min)
    return data_rows

def save_to_csv(data, file_path):
    file_exists = False
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "issuer_code", "date", "last_transaction_price", "max_price",
            "min_price", "average_price", "percent_change", "quantity",
            "best_trading_volume", "total_turnover"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def main():
    driver = setup_driver()
    issuer_codes = fetch_issuer_codes(driver)
    for code in issuer_codes:
        print(f"Fetching data for issuer code: {code}")
        data = fetch_issuer_data(driver, code)
        save_to_csv(data, csv_file_path)
        print(f"Data for issuer {code} saved.")
    driver.quit()

main()