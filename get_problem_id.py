import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

problems = requests.get(f"{BASE_URL}/problems/").json()
best_time = [p for p in problems if "Best Time" in p.get("title", "")][0]
print(f"Problem ID: {best_time['id']}")
print(f"Title: {best_time['title']}")
