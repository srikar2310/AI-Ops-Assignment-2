import csv
import random

def generate_dataset(filename="dataset.csv", num_samples=1000):
    random.seed(42)
    spam_keywords = ["WINNER", "FREE", "URGENT", "CLAIM NOW", "PRIZE", "CASH", "CLICK HERE"]
    ham_keywords = ["meeting", "project", "schedule", "report", "dinner", "thanks", "update"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        for _ in range(num_samples):
            if random.random() < 0.5:
                text = f"Congratulations! You are a {random.choice(spam_keywords)}! Claim your ${random.randint(100, 5000)} now!"
                label = "spam"
            else:
                text = f"Hi, let's discuss the {random.choice(ham_keywords)} for tomorrow. Thanks!"
                label = "ham"
            writer.writerow([text, label])

if __name__ == "__main__":
    generate_dataset()
    print("dataset.csv generated successfully.")