from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time

def fetch_issuers():
    url = "https://www.mse.mk/en/stats/symbolhistory/kmb"
    driver = webdriver.Firefox(options=Options())
    driver.get(url)

    time.sleep(2)
    dropdown = driver.find_element(By.ID, "Code")
    select = Select(dropdown)

    issuers = []
    for option in select.options:
        issuer_code = option.get_attribute("value")
        if issuer_code.isalpha():
            issuers.append(issuer_code)

    driver.quit()
    return issuers