import csv
from datetime import datetime
import os

LOG_FILE = "conversation_logs.csv"

HEADERS = [
    "timestamp",
    "channel",
    "message",
    "action",
    "priority",
    "source"
]

def log_event(channel, message, action, priority, source):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(HEADERS)

        writer.writerow([
            datetime.now().isoformat(),
            channel,
            message,
            action,
            priority,
            source
        ])
