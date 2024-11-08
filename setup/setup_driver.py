from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os

def setup_driver(url, driver_path=None, firefox_binary_path=None):
    if driver_path is None:
        driver_path = os.getenv("GECKODRIVER_PATH", "geckodriver")
    if firefox_binary_path is None:
        firefox_binary_path = os.getenv("FIREFOX_BINARY_PATH", "firefox")

    options = Options()
    options.binary_location = firefox_binary_path
    service = Service(executable_path=driver_path)

    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    return driver