import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next((p for p in problems if p["title"].lower() == "two sum"), None)

print("Problem examples:")
for i, ex in enumerate(two_sum.get("examples", []), 1):
    print(f"  Example {i}: input={ex['input'][:30]}... expected={ex['output']}")

print("\n" + "="*80)

# Test Python Two Sum with simple code
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

print(f"\nTesting Python Two Sum:")
resp = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": python_code, "language": "python", "problem_id": two_sum["id"]}
)
result = resp.json()
print(f"  Status: {result.get('status')}")
print(f"  Passed: {result.get('passed_count')}/{result.get('total_count')}")
print(f"  Output details:")
for i, case in enumerate(result.get('test_details', []), 1):
    print(f"    Test {i}: {case}")
