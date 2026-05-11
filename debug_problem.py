import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get Best Time problem
problems = requests.get(f"{BASE_URL}/problems/").json()
best_time = next(p for p in problems if "best time" in p["title"].lower())

print("Problem keys:", best_time.keys())
print("\nFull problem data:")
print(json.dumps(best_time, indent=2)[:1000])
