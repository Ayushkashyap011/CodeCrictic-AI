import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
problems = requests.get(f"{BASE_URL}/problems/").json()

# Find Maximum Subarray
max_sub = [p for p in problems if "Maximum" in p.get("title", "")][0]
print(json.dumps(max_sub, indent=2, default=str)[:2000])
