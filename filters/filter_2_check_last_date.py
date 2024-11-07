import csv
from datetime import datetime

def get_last_date(issuer_code, csv_file_path):
    last_date = None
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['issuer_code'] == issuer_code:
                    date = datetime.strptime(row['date'], "%m/%d/%Y")
                    if last_date is None or date > last_date:
                        last_date = date
    except FileNotFoundError:
        pass
    return last_date