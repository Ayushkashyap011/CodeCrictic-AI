import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test codes for all languages
test_suites = {
    "Two Sum": {
        "javascript": """
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
""",
        "java": """
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
""",
        "cpp": """
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
""",
        "python": """
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
    },
}

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
problem_map = {p["title"].lower(): p for p in problems}

print("=" * 80)
print("MULTI-LANGUAGE TEST")
print("=" * 80)

for problem_name, codes in test_suites.items():
    print(f"\n{problem_name}:")
    
    problem = problem_map.get(problem_name.lower())
    if not problem:
        print(f"  WARNING: Problem not found")
        continue
    
    for language, code in codes.items():
        response = requests.post(
            f"{BASE_URL}/execute/run",
            json={"code": code, "language": language, "problem_id": problem["id"]}
        )
        result = response.json()
        status = result.get('status', 'Unknown')
        passed = result.get('passed_count', 0)
        total = result.get('total_count', 0)
        
        mark = "PASS" if status == "Accepted" else "FAIL"
        print(f"  {mark} {language:12} Status={status:12} Passed={passed}/{total}")
