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

# Get first problem ID
problems = requests.get(f"{BASE_URL}/problems/").json()
problem_id = problems[0]["id"]
print(f"Testing with problem: {problems[0]['title']}")

# Test JavaScript
print("\n🧪 Testing JavaScript...")
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": js_code, "language": "javascript", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results']:
        print(f"  Test {test['test_number']}: {test.get('actual')} (expected: {test.get('expected')})")

# Test Java
print("\n🧪 Testing Java...")
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": java_code, "language": "java", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results']:
        print(f"  Test {test['test_number']}: {test.get('actual')} (expected: {test.get('expected')})")

# Test C++
print("\n🧪 Testing C++...")
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": cpp_code, "language": "cpp", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results']:
        print(f"  Test {test['test_number']}: {test.get('actual')} (expected: {test.get('expected')})")
