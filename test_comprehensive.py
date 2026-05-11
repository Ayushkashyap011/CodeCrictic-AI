import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()

# Test specific problems
test_cases = {
    "two sum": """
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
    "climbing stairs": """
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
    "valid parentheses": """
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
"""
}

print("Testing Multiple Problems - JavaScript:\n")
for problem_name, code in test_cases.items():
    problem = next((p for p in problems if problem_name in p["title"].lower()), None)
    if problem:
        response = requests.post(
            f"{BASE_URL}/execute/run",
            json={"code": code, "language": "javascript", "problem_id": problem["id"]}
        )
        result = response.json()
        status = result.get('status', 'Unknown')
        passed = result.get('passed_count', '?')
        total = result.get('total_count', '?')
        print(f"  {problem['title']:35} Status={status:12} Passed={passed}/{total}")
