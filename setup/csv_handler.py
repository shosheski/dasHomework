import csv
from datetime import datetime

def save_to_csv(data, file_path):
    data.sort(key=lambda x: (x["issuer_code"],
        datetime.strptime(x["date"], "%m/%d/%Y") if x["date"] and x["date"] != "/" else datetime.min))

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