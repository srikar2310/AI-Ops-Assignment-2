import time
import json
import urllib.request

url = "http://localhost:8000/predict"
payload = json.dumps({"text": "CONGRATULATIONS! You won a $1000 Walmart gift card. Claim now!"}).encode("utf-8")
headers = {"Content-Type": "application/json"}

def send_request():
    req = urllib.request.Request(url, data=payload, headers=headers)
    start = time.perf_counter()
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed = (time.perf_counter() - start) * 1000
    return data, elapsed

if __name__ == "__main__":
    print("Sending 1st request (Cache MISS)...")
    res1, t1 = send_request()
    print(f"Response: {res1} | Time: {t1:.3f} ms\n")

    print("Sending 2nd request (Cache HIT)...")
    res2, t2 = send_request()
    print(f"Response: {res2} | Time: {t2:.3f} ms\n")

    print(f"Speedup Factor: {t1/t2:.2f}x faster on Cache HIT")