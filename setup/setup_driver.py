from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def setup_driver(url):
    driver_path = "C://Users/goraz/Desktop/geckodriver.exe"
    firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    options = Options()
    options.binary_location = firefox_binary_path
    service = Service(executable_path=driver_path)

    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)

    driver.implicitly_wait(5)
    return driver
