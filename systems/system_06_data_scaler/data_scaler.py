import json
import random
import copy

INPUT_FILES = [
    "../system_04_conversation_generator/synthetic_conversations.json",
    "../system_05_email_ticket_generator/synthetic_emails_tickets.json"
]

OUTPUT_FILE = "scaled_synthetic_data.json"

def load_data():
    all_records = []
    for path in INPUT_FILES:
        with open(path, "r", encoding="utf-8") as f:
            all_records.extend(json.load(f))
    return all_records

def vary_record(record):
    new_record = copy.deepcopy(record)

    if "urgency" in new_record:
        new_record["urgency"] = random.choice(["low", "medium", "high"])

    if "outcome" in new_record:
        new_record["outcome"] = random.choice(["resolved", "escalated"])

    new_record["variant_id"] = random.randint(1000, 9999)
    return new_record

def scale_data(records, factor=5):
    scaled = []
    for r in records:
        scaled.append(r)
        for _ in range(factor - 1):
            scaled.append(vary_record(r))
    return scaled

if __name__ == "__main__":
    records = load_data()
    scaled_records = scale_data(records, factor=5)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(scaled_records, f, indent=2)

    print(f"Scaled dataset created with {len(scaled_records)} records.")
