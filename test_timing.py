import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems_resp = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next((p for p in problems_resp if p["title"].lower() == "two sum"), None)

python_code = """
class Solution:
    def twoSum(self, nums, target):
        map_dict = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in map_dict:
                return [map_dict[complement], i]
            map_dict[num] = i
        return []
"""

print("First test (should fail due to timing):")
resp = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": python_code, "language": "python", "problem_id": two_sum["id"]}
)
result = resp.json()
print(f"  Status: {result.get('status')}, Passed: {result.get('passed_count')}/{result.get('total_count')}")

print("\nWaiting 2 seconds...")
time.sleep(2)

print("Second test (should pass after timing out):")
resp = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": python_code, "language": "python", "problem_id": two_sum["id"]}
)
result = resp.json()
print(f"  Status: {result.get('status')}, Passed: {result.get('passed_count')}/{result.get('total_count')}")
