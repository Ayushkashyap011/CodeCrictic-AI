import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test Java code for Two Sum
java_code = """
class Solution {
    public int[] twoSum(int[] nums, int target) {
        java.util.Map<Integer, Integer> map = new java.util.HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}
"""

# Get Two Sum problem
problems = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next(p for p in problems if "two sum" in p["title"].lower())
problem_id = two_sum["id"]
print(f"Testing with problem: {two_sum['title']}")

# Test Java with detailed error output
print("\n🧪 Testing Java...")
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": java_code, "language": "java", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
if result.get('test_results'):
    for test in result['test_results']:
        print(f"\nTest {test['test_number']}:")
        print(f"  Input: {test.get('input')}")
        print(f"  Expected: {test.get('expected')}")
        print(f"  Actual: {test.get('actual')}")
        if test.get('error'):
            print(f"  Error: {test.get('error')[:500]}")
