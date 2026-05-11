import requests
import json

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
    "Valid Parentheses": {
        "javascript": """
class Solution {
    isValid(s) {
        const stack = [];
        const map = {'(': ')', '{': '}', '[': ']'};
        for (const char of s) {
            if (char in map) {
                stack.push(char);
            } else {
                if (stack.length === 0 || map[stack.pop()] !== char) {
                    return false;
                }
            }
        }
        return stack.length === 0;
    }
}
""",
        "java": """
class Solution {
    public boolean isValid(String s) {
        java.util.Stack<Character> stack = new java.util.Stack<>();
        java.util.Map<Character, Character> map = new java.util.HashMap<>();
        map.put(')', '(');
        map.put('}', '{');
        map.put(']', '[');
        for (char c : s.toCharArray()) {
            if (map.containsKey(c)) {
                if (stack.isEmpty() || stack.pop() != map.get(c)) {
                    return false;
                }
            } else {
                stack.push(c);
            }
        }
        return stack.isEmpty();
    }
}
""",
        "cpp": """
#include <stack>
#include <unordered_map>
using namespace std;
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char, char> map;
        map[')'] = '(';
        map['}'] = '{';
        map[']'] = '[';
        for (char c : s) {
            if (map.find(c) != map.end()) {
                if (st.empty() || st.top() != map[c]) {
                    return false;
                }
                st.pop();
            } else {
                st.push(c);
            }
        }
        return st.empty();
    }
};
""",
        "python": """
class Solution:
    def isValid(self, s):
        stack = []
        map_dict = {')': '(', '}': '{', ']': '['}
        for c in s:
            if c in map_dict:
                if not stack or stack.pop() != map_dict[c]:
                    return False
            else:
                stack.append(c)
        return len(stack) == 0
"""
    },
    "Climbing Stairs": {
        "javascript": """
class Solution {
    climbStairs(n) {
        if (n <= 1) return 1;
        let a = 1, b = 1;
        for (let i = 2; i <= n; i++) {
            [a, b] = [b, a + b];
        }
        return b;
    }
}
""",
        "java": """
class Solution {
    public int climbStairs(int n) {
        if (n <= 1) return 1;
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int temp = b;
            b = a + b;
            a = temp;
        }
        return b;
    }
}
""",
        "cpp": """
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 1) return 1;
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int temp = b;
            b = a + b;
            a = temp;
        }
        return b;
    }
};
""",
        "python": """
class Solution:
    def climbStairs(self, n):
        if n <= 1:
            return 1
        a, b = 1, 1
        for i in range(2, n + 1):
            a, b = b, a + b
        return b
"""
    }
}

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
problem_map = {p["title"].lower(): p for p in problems}

print("=" * 80)
print("COMPREHENSIVE MULTI-LANGUAGE TEST")
print("=" * 80)

results = {}
for problem_name, codes in test_suites.items():
    print(f"\n{problem_name}:")
    results[problem_name] = {}
    
    problem = problem_map.get(problem_name.lower())
    if not problem:
        print(f"  ⚠️  Problem not found in database")
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
        
        results[problem_name][language] = {
            "status": status,
            "passed": passed,
            "total": total
        }
        
        checkmark = "✅" if status == "Accepted" else "❌"
        print(f"  {checkmark} {language:12} Status={status:12} Passed={passed}/{total}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

all_passed = True
for problem_name, langs in results.items():
    for lang, data in langs.items():
        if data["status"] != "Accepted" or data["passed"] != data["total"]:
            all_passed = False
            
if all_passed:
    print("✅ ALL TESTS PASSED! All languages working correctly.")
else:
    print("⚠️  Some tests failed. Review above for details.")
