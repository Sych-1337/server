import json, os
from datetime import datetime

ANALYTICS_FILE = "analytics.json"

def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        return {}
    with open(ANALYTICS_FILE, "r") as f:
        return json.load(f)

def save_analytics(data):
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def store_postback(app_name: str, params: dict):
    data = load_analytics()
    record = dict(params)
    record["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if app_name not in data:
        data[app_name] = []
    data[app_name].append(record)
    save_analytics(data)
