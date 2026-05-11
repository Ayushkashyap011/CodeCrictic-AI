import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next((p for p in problems if p["title"].lower() == "two sum"), None)

# Python Two Sum
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

# C++ Two Sum  
cpp_code = """
#include <unordered_map>
using namespace std;
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

if two_sum:
    print("Testing Python Two Sum:")
    resp = requests.post(
        f"{BASE_URL}/execute/run",
        json={"code": python_code, "language": "python", "problem_id": two_sum["id"]}
    )
    result = resp.json()
    print(f"  Status: {result.get('status')}")
    print(f"  Passed: {result.get('passed_count')}/{result.get('total_count')}")
    print(f"  Output: {result.get('output')}")
    
    print("\nTesting C++ Two Sum:")
    resp = requests.post(
        f"{BASE_URL}/execute/run",
        json={"code": cpp_code, "language": "cpp", "problem_id": two_sum["id"]}
    )
    result = resp.json()
    print(f"  Status: {result.get('status')}")
    print(f"  Passed: {result.get('passed_count')}/{result.get('total_count')}")
    print(f"  Output: {result.get('output')}")
