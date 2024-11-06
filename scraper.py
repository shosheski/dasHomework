import requests
from bs4 import BeautifulSoup

URL = "https://www.mse.mk/mk/stats/symbolhistory/kmb"

response = requests.get(URL)
html = response.content
soup = BeautifulSoup(html, "html.parser")


