from bs4 import BeautifulSoup
from datetime import datetime


def clean_text(text):
    if not text:
        return ''
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=' ', strip=True)


def extract_date_only(date_str):
    if not date_str:
        return ''
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    if len(date_str) >= 10 and date_str[:4].isdigit():
        return date_str[:10]
    return ''


def get_earliest_date(dates):
    dates = [d for d in dates if d]
    if not dates:
        return ''
    date_only_list = [extract_date_only(d) for d in dates if extract_date_only(d)]
    return min(date_only_list) if date_only_list else ''
