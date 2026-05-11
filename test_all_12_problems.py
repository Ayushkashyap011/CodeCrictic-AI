import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Solution codes for all 12 problems
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
    },
    "Best Time to Buy and Sell Stock": {
        "javascript": "class Solution {\n    maxProfit(prices) {\n        if (!prices || prices.length < 2) return 0;\n        let minBuyPrice = prices[0];\n        let maxProfit = 0;\n        for (let i = 1; i < prices.length; i++) {\n            maxProfit = Math.max(maxProfit, prices[i] - minBuyPrice);\n            minBuyPrice = Math.min(minBuyPrice, prices[i]);\n        }\n        return maxProfit;\n    }\n}",
        "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        if (prices == null || prices.length < 2) return 0;\n        int minBuyPrice = Integer.MAX_VALUE;\n        int maxProfit = 0;\n        for (int price : prices) {\n            maxProfit = Math.max(maxProfit, price - minBuyPrice);\n            minBuyPrice = Math.min(minBuyPrice, price);\n        }\n        return maxProfit;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        if (prices.empty() || prices.size() < 2) return 0;\n        int minBuyPrice = INT_MAX;\n        int maxProfit = 0;\n        for (int price : prices) {\n            maxProfit = max(maxProfit, price - minBuyPrice);\n            minBuyPrice = min(minBuyPrice, price);\n        }\n        return maxProfit;\n    }\n};",
        "python": "class Solution:\n    def maxProfit(self, prices):\n        if not prices or len(prices) < 2:\n            return 0\n        min_buy_price = prices[0]\n        max_profit = 0\n        for price in prices:\n            max_profit = max(max_profit, price - min_buy_price)\n            min_buy_price = min(min_buy_price, price)\n        return max_profit"
    }
}

# Get all problems
print("Fetching problems...")
response = requests.get(f"{BASE_URL}/problems/")
problems = response.json()
problem_map = {p["title"].lower(): p for p in problems}

print(f"Found {len(problems)} problems")
print("=" * 80)
print("TESTING ALL AVAILABLE PROBLEMS")
print("=" * 80)

results = {}
total_pass = 0
total_fail = 0

for problem_name, codes in test_suites.items():
    print(f"\n{problem_name}:")
    problem = problem_map.get(problem_name.lower())
    
    if not problem:
        print(f"  ⚠️  Problem not found in system")
        continue
    
    results[problem_name] = {}
    
    for language, code in codes.items():
        try:
            response = requests.post(
                f"{BASE_URL}/execute/run",
                json={"code": code, "language": language, "problem_id": problem["id"]}
            )
            result = response.json()
            status = result.get("status", "Unknown")
            passed = result.get("passed_count", 0)
            total = result.get("total_count", 0)
            
            if status == "Accepted":
                marker = "✅"
                total_pass += 1
            else:
                marker = "❌"
                total_fail += 1
            
            results[problem_name][language] = status
            print(f"  {marker} {language:12} Status={status:15} Passed={passed}/{total}")
            
        except Exception as e:
            print(f"  ❌ {language:12} ERROR: {str(e)}")
            total_fail += 1

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Pass:  {total_pass}")
print(f"Total Fail:  {total_fail}")

# Show missing problems
tested_problems = [p.lower() for p in test_suites.keys()]
missing = [p["title"] for p in problems if p["title"].lower() not in tested_problems]
if missing:
    print(f"\nProblems not yet tested ({len(missing)}):")
    for p in missing:
        print(f"  - {p}")
