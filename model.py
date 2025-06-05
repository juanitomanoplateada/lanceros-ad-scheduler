# model.py
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data/ads_data.json"
BACKUP_DIR = "data/backups"


class AdSchedulerModel:

    def __init__(self):
        self.schedule = self.load_ad_data()

    def load_ad_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            start_time = datetime.strptime("5:30AM", "%I:%M%p")
            end_time = datetime.strptime("8:30PM", "%I:%M%p")
            schedule = {}
            current_time = start_time
            while current_time <= end_time:
                label = current_time.strftime("%I:%M%p").lstrip("0")
                schedule[label] = []
                current_time += timedelta(minutes=30)
            return schedule

    def save_ad_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, indent=2)

        os.makedirs(BACKUP_DIR, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        backup_path = os.path.join(BACKUP_DIR, f"{today}_ads_backup.json")
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, indent=2)

    def export_schedule(self, export_path):
        with open(export_path, "w", encoding="utf-8") as f:
            for slot, ads in self.schedule.items():
                f.write(f"{slot}: {', '.join(map(str, sorted(ads)))}\n")
