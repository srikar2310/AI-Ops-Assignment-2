import csv
import os
import random

NUM_SHARDS = 8
ROWS_PER_SHARD = 100
OUTPUT_DIR = "shards"

os.makedirs(OUTPUT_DIR, exist_ok=True)

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ian", "Julia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
DOMAINS = ["example.com", "test.org", "mail.net", "service.co"]

def generate_valid_row(user_id):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}"
    signup_date = f"2026-0{random.randint(1, 9)}-{random.randint(10, 28)}"
    return [user_id, name, email, signup_date]

def generate_invalid_row(user_id):
    row = generate_valid_row(user_id)
    error_type = random.choice(["malformed_email", "missing_email", "missing_name"])
    
    if error_type == "malformed_email":
        row[2] = row[2].replace("@", "_at_")
    elif error_type == "missing_email":
        row[2] = ""
    elif error_type == "missing_name":
        row[1] = ""
        
    return row

print("--- Generating Synthetic CSV Shards ---")
for shard_idx in range(NUM_SHARDS):
    random.seed(42 + shard_idx)
    invalid_target = random.randint(5, 25)
    invalid_indices = set(random.sample(range(ROWS_PER_SHARD), invalid_target))
    
    file_path = os.path.join(OUTPUT_DIR, f"shard_{shard_idx}.csv")
    invalid_count = 0
    
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "name", "email", "signup_date"])
        
        for row_idx in range(ROWS_PER_SHARD):
            user_id = shard_idx * 1000 + row_idx + 1
            if row_idx in invalid_indices:
                row = generate_invalid_row(user_id)
                invalid_count += 1
            else:
                row = generate_valid_row(user_id)
            writer.writerow(row)
            
    print(f"Created {file_path} | Total Rows: {ROWS_PER_SHARD} | Seeded Invalid Rows: {invalid_count}")