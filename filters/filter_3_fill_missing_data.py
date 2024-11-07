from datetime import timedelta
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

def fill_missing_data(driver, issuer_code, last_date):
    end_date = datetime.now() - timedelta(days=1)
    current_start_date = last_date + timedelta(days=1) if last_date else end_date - timedelta(days=365 * 10)

    data_rows = []
    select = Select(driver.find_element(By.ID, "Code"))
    select.select_by_value(issuer_code)

    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=364), end_date)
        from_date_input = driver.find_element(By.ID, "FromDate")
        to_date_input = driver.find_element(By.ID, "ToDate")

        from_date_input.clear()
        from_date_input.send_keys(current_start_date.strftime("%m/%d/%Y"))
        to_date_input.clear()
        to_date_input.send_keys(current_end_date.strftime("%m/%d/%Y"))

        driver.find_element(By.CSS_SELECTOR, "input[onclick='return btnClick();']").click()

        try:
            # Wait for the results table to appear, but give up after 10 seconds
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultsTable")))
        except TimeoutException:
            print(f"Timeout waiting for table for issuer {issuer_code}. Skipping.")
            current_start_date += timedelta(days=365)
            time.sleep(1)
            continue  # Skip this iteration if no table is found

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", {"id": "resultsTable"})

        if table:
            rows = table.find_all("tr")[1:]
            if rows:
                for row in rows:
                    cells = row.find_all("td")
                    if cells and len(cells) >= 9:
                        date = cells[0].text.strip()
                        data_rows.append({
                            "issuer_code": issuer_code,
                            "date": date,
                            "last_transaction_price": cells[1].text.strip(),
                            "max_price": cells[2].text.strip(),
                            "min_price": cells[3].text.strip(),
                            "average_price": cells[4].text.strip(),
                            "percent_change": cells[5].text.strip(),
                            "quantity": cells[6].text.strip(),
                            "best_trading_volume": cells[7].text.strip(),
                            "total_turnover": cells[8].text.strip()
                        })
            else:
                print(f"No data found for issuer {issuer_code} in the table.")
        else:
            print(f"No table found for issuer {issuer_code}.")

        current_start_date += timedelta(days=365)
        time.sleep(1)

    return data_rows