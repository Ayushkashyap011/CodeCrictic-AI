import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test JavaScript code for Two Sum
js_code = """
class Solution {
    twoSum(nums, target) {
        const map = new Map();
        for (let i = 0; i < nums.length; i++) {
            const complement = target - nums[i];
            if (map.has(complement)) {
                return [map.get(complement), i];
            }
            map.set(nums[i], i);
        }
        return [];
    }
}
"""

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

# Test C++ code for Two Sum
cpp_code = """
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> map;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (map.find(complement) != map.end()) {
                return {map[complement], i};
            }
            map[nums[i]] = i;
        }
        return {};
    }
};
"""

# Get Two Sum problem
problems = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next(p for p in problems if "two sum" in p["title"].lower())
problem_id = two_sum["id"]
print(f"Testing with problem: {two_sum['title']}\n")

# Test JavaScript
print("=" * 60)
print("🧪 Testing JavaScript...")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": js_code, "language": "javascript", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results'][:1]:
        print(f"Sample Output: {test.get('actual')} (expected: {test.get('expected')})")

# Test Java
print("\n" + "=" * 60)
print("🧪 Testing Java...")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": java_code, "language": "java", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results'][:1]:
        print(f"Sample Output: {test.get('actual')} (expected: {test.get('expected')})")

# Test C++
print("\n" + "=" * 60)
print("🧪 Testing C++...")
print("=" * 60)
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": cpp_code, "language": "cpp", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results'][:1]:
        print(f"Sample Output: {test.get('actual')} (expected: {test.get('expected')})")

print("\n✅ All languages are executing! (Output formatting may need adjustment)")
