import json
import pandas as pd
import os

INPUT_FILE = "../system_01_synthetic_data/customer_support_tickets_latest.json"
OUTPUT_PREFIX = "customer_support_tickets_structured"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_records(records):
    normalized = []

    for item in records:
        row = {}
        for key, value in item.items():
            row[key] = value
        normalized.append(row)

    return normalized


def save_outputs(data, prefix):
    df = pd.DataFrame(data)

    csv_file = f"{prefix}.csv"
    excel_file = f"{prefix}.xlsx"

    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    print(f"Saved CSV: {csv_file}")
    print(f"Saved Excel: {excel_file}")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print("Input JSON file not found.")
        exit()

    records = load_json(INPUT_FILE)
    structured = normalize_records(records)
    save_outputs(structured, OUTPUT_PREFIX)
