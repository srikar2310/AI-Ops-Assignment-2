import time
import requests

API_URL = "http://localhost:8000/predict"
TEST_TEXT = "WIN a FREE iPhone now! Click here: bit.ly/xyz123"

def send_request():
    start = time.perf_counter()
    response = requests.post(API_URL, json={"text": TEST_TEXT})
    elapsed_ms = (time.perf_counter() - start) * 1000
    data = response.json()
    return data, elapsed_ms

print("Sending 1st request (Cache MISS)...")
res1, time1 = send_request()
print(f"Response: {res1} | Time: {time1:.3f} ms\n")

print("Sending 2nd request (Cache HIT)...")
res2, time2 = send_request()
print(f"Response: {res2} | Time: {time2:.3f} ms\n")

speedup = time1 / time2 if time2 > 0 else 0
print(f"Speedup Factor: {speedup:.2f}x faster on Cache HIT")