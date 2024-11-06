import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.mse.mk/en/stats/symbolhistory/kmb"

def fetch_issuer_codes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    codes = []
    dropdown = soup.find("select", {"id": "Code"})

    code_pattern = re.compile(r'^[A-Za-z]+$')

    for option in dropdown.find_all("option"):
        code = option.get("value")
        if code and code_pattern.match(code):
            codes.append(code)

    return codes


