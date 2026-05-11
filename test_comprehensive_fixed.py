import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test codes for multiple problems
test_suites = {
    "Two Sum": {
        "javascript": "class Solution {\n    twoSum(nums, target) {\n        const map = new Map();\n        for (let i = 0; i < nums.length; i++) {\n            const complement = target - nums[i];\n            if (map.has(complement)) {\n                return [map.get(complement), i];\n            }\n            map.set(nums[i], i);\n        }\n        return [];\n    }\n}",
        "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        java.util.Map<Integer, Integer> map = new java.util.HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int complement = target - nums[i];\n            if (map.containsKey(complement)) {\n                return new int[]{map.get(complement), i};\n            }\n            map.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n}",
        "cpp": "#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> map;\n        for (int i = 0; i < nums.size(); i++) {\n            int complement = target - nums[i];\n            if (map.find(complement) != map.end()) {\n                return {map[complement], i};\n            }\n            map[nums[i]] = i;\n        }\n        return {};\n    }\n};",
        "python": "class Solution:\n    def twoSum(self, nums, target):\n        map_dict = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in map_dict:\n                return [map_dict[complement], i]\n            map_dict[num] = i\n        return []"
    },
    "Valid Parentheses": {
        "javascript": "class Solution {\n    isValid(s) {\n        const stack = [];\n        const map = {'(': ')', '{': '}', '[': ']'};\n        for (const char of s) {\n            if (char in map) {\n                stack.push(char);\n            } else {\n                if (stack.length === 0 || map[stack.pop()] !== char) {\n                    return false;\n                }\n            }\n        }\n        return stack.length === 0;\n    }\n}",
        "java": "class Solution {\n    public boolean isValid(String s) {\n        java.util.Stack<Character> stack = new java.util.Stack<>();\n        java.util.Map<Character, Character> map = new java.util.HashMap<>();\n        map.put(')', '(');\n        map.put('}', '{');\n        map.put(']', '[');\n        for (char c : s.toCharArray()) {\n            if (map.containsKey(c)) {\n                if (stack.isEmpty() || stack.pop() != map.get(c)) {\n                    return false;\n                }\n            } else {\n                stack.push(c);\n            }\n        }\n        return stack.isEmpty();\n    }\n}",
        "cpp": "#include <stack>\nusing namespace std;\nclass Solution {\npublic:\n    bool isValid(string s) {\n        stack<char> st;\n        for (char c : s) {\n            if (c == ')' || c == '}' || c == ']') {\n                if (st.empty()) return false;\n                char open = st.top();\n                st.pop();\n                if ((c == ')' && open != '(') || (c == '}' && open != '{') || (c == ']' && open != '[')) {\n                    return false;\n                }\n            } else {\n                st.push(c);\n            }\n        }\n        return st.empty();\n    }\n};",
        "python": "class Solution:\n    def isValid(self, s):\n        stack = []\n        map_dict = {')': '(', '}': '{', ']': '['}\n        for c in s:\n            if c in map_dict:\n                if not stack or stack.pop() != map_dict[c]:\n                    return False\n            else:\n                stack.append(c)\n        return len(stack) == 0"
    },
    "Climbing Stairs": {
        "javascript": "class Solution {\n    climbStairs(n) {\n        if (n <= 1) return 1;\n        let a = 1, b = 1;\n        for (let i = 2; i <= n; i++) {\n            [a, b] = [b, a + b];\n        }\n        return b;\n    }\n}",
        "java": "class Solution {\n    public int climbStairs(int n) {\n        if (n <= 1) return 1;\n        int a = 1, b = 1;\n        for (int i = 2; i <= n; i++) {\n            int temp = b;\n            b = a + b;\n            a = temp;\n        }\n        return b;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        if (n <= 1) return 1;\n        int a = 1, b = 1;\n        for (int i = 2; i <= n; i++) {\n            int temp = b;\n            b = a + b;\n            a = temp;\n        }\n        return b;\n    }\n};",
        "python": "class Solution:\n    def climbStairs(self, n):\n        if n <= 1:\n            return 1\n        a, b = 1, 1\n        for i in range(2, n + 1):\n            a, b = b, a + b\n        return b"
    }
}

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
problem_map = {p["title"].lower(): p for p in problems}

print("=" * 80)
print("COMPREHENSIVE MULTI-PROBLEM, MULTI-LANGUAGE TEST")
print("=" * 80)

all_pass = True
for problem_name, codes in test_suites.items():
    print(f"\n{problem_name}:")
    
    problem = problem_map.get(problem_name.lower())
    if not problem:
        print(f"  WARNING: Problem not found")
        continue
    
    problem_pass = True
    for language, code in codes.items():
        response = requests.post(
            f"{BASE_URL}/execute/run",
            json={"code": code, "language": language, "problem_id": problem["id"]}
        )
        result = response.json()
        status = result.get('status', 'Unknown')
        passed = result.get('passed_count', 0)
        total = result.get('total_count', 0)
        
        is_pass = status == "Accepted" and passed == total
        problem_pass = problem_pass and is_pass
        all_pass = all_pass and is_pass
        
        mark = "OK" if is_pass else "FAIL"
        print(f"  [{mark}] {language:12} Status={status:12} Passed={passed}/{total}")

print("\n" + "=" * 80)
if all_pass:
    print("SUCCESS: All problems passed for all languages!")
else:
    print("FAILURE: Some tests failed. See details above.")
print("=" * 80)
