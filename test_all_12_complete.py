import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Solution codes for ALL 12 problems
test_suites = {
    "Two Sum": {
        "python": "class Solution:\n    def twoSum(self, nums, target):\n        map_dict = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in map_dict:\n                return [map_dict[complement], i]\n            map_dict[num] = i\n        return []",
        "javascript": "class Solution {\n    twoSum(nums, target) {\n        const map = new Map();\n        for (let i = 0; i < nums.length; i++) {\n            const complement = target - nums[i];\n            if (map.has(complement)) {\n                return [map.get(complement), i];\n            }\n            map.set(nums[i], i);\n        }\n        return [];\n    }\n}",
        "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        java.util.Map<Integer, Integer> map = new java.util.HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int complement = target - nums[i];\n            if (map.containsKey(complement)) {\n                return new int[]{map.get(complement), i};\n            }\n            map.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n}",
        "cpp": "#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> map;\n        for (int i = 0; i < nums.size(); i++) {\n            int complement = target - nums[i];\n            if (map.find(complement) != map.end()) {\n                return {map[complement], i};\n            }\n            map[nums[i]] = i;\n        }\n        return {};\n    }\n};"
    },
    "Valid Parentheses": {
        "python": "class Solution:\n    def isValid(self, s):\n        stack = []\n        map_dict = {')': '(', '}': '{', ']': '['}\n        for c in s:\n            if c in map_dict:\n                if not stack or stack.pop() != map_dict[c]:\n                    return False\n            else:\n                stack.append(c)\n        return len(stack) == 0",
        "javascript": "class Solution {\n    isValid(s) {\n        const stack = [];\n        const map = {'(': ')', '{': '}', '[': ']'};\n        for (const char of s) {\n            if (char in map) {\n                stack.push(char);\n            } else {\n                if (stack.length === 0 || map[stack.pop()] !== char) {\n                    return false;\n                }\n            }\n        }\n        return stack.length === 0;\n    }\n}",
        "java": "class Solution {\n    public boolean isValid(String s) {\n        java.util.Stack<Character> stack = new java.util.Stack<>();\n        java.util.Map<Character, Character> map = new java.util.HashMap<>();\n        map.put(')', '('); map.put('}', '{'); map.put(']', '[');\n        for (char c : s.toCharArray()) {\n            if (map.containsKey(c)) {\n                if (stack.isEmpty() || stack.pop() != map.get(c)) return false;\n            } else {\n                stack.push(c);\n            }\n        }\n        return stack.isEmpty();\n    }\n}",
        "cpp": "#include <stack>\nusing namespace std;\nclass Solution {\npublic:\n    bool isValid(string s) {\n        stack<char> st;\n        for (char c : s) {\n            if (c == ')' || c == '}' || c == ']') {\n                if (st.empty()) return false;\n                char open = st.top(); st.pop();\n                if ((c == ')' && open != '(') || (c == '}' && open != '{') || (c == ']' && open != '[')) return false;\n            } else {\n                st.push(c);\n            }\n        }\n        return st.empty();\n    }\n};"
    },
    "Climbing Stairs": {
        "python": "class Solution:\n    def climbStairs(self, n):\n        if n <= 1: return 1\n        a, b = 1, 1\n        for i in range(2, n + 1):\n            a, b = b, a + b\n        return b",
        "javascript": "class Solution {\n    climbStairs(n) {\n        if (n <= 1) return 1;\n        let a = 1, b = 1;\n        for (let i = 2; i <= n; i++) {\n            [a, b] = [b, a + b];\n        }\n        return b;\n    }\n}",
        "java": "class Solution {\n    public int climbStairs(int n) {\n        if (n <= 1) return 1;\n        int a = 1, b = 1;\n        for (int i = 2; i <= n; i++) {\n            int temp = b; b = a + b; a = temp;\n        }\n        return b;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        if (n <= 1) return 1;\n        int a = 1, b = 1;\n        for (int i = 2; i <= n; i++) {\n            int temp = b; b = a + b; a = temp;\n        }\n        return b;\n    }\n};"
    },
    "Best Time to Buy and Sell Stock": {
        "python": "class Solution:\n    def maxProfit(self, prices):\n        if not prices or len(prices) < 2: return 0\n        min_buy_price = prices[0]\n        max_profit = 0\n        for price in prices:\n            max_profit = max(max_profit, price - min_buy_price)\n            min_buy_price = min(min_buy_price, price)\n        return max_profit",
        "javascript": "class Solution {\n    maxProfit(prices) {\n        if (!prices || prices.length < 2) return 0;\n        let minBuyPrice = prices[0], maxProfit = 0;\n        for (let i = 1; i < prices.length; i++) {\n            maxProfit = Math.max(maxProfit, prices[i] - minBuyPrice);\n            minBuyPrice = Math.min(minBuyPrice, prices[i]);\n        }\n        return maxProfit;\n    }\n}",
        "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        if (prices == null || prices.length < 2) return 0;\n        int minBuyPrice = Integer.MAX_VALUE, maxProfit = 0;\n        for (int price : prices) {\n            maxProfit = Math.max(maxProfit, price - minBuyPrice);\n            minBuyPrice = Math.min(minBuyPrice, price);\n        }\n        return maxProfit;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        if (prices.empty() || prices.size() < 2) return 0;\n        int minBuyPrice = INT_MAX, maxProfit = 0;\n        for (int price : prices) {\n            maxProfit = max(maxProfit, price - minBuyPrice);\n            minBuyPrice = min(minBuyPrice, price);\n        }\n        return maxProfit;\n    }\n};"
    },
    "Maximum Subarray": {
        "python": "class Solution:\n    def maxSubArray(self, nums):\n        max_current = max_global = nums[0]\n        for i in range(1, len(nums)):\n            max_current = max(nums[i], max_current + nums[i])\n            max_global = max(max_global, max_current)\n        return max_global",
        "javascript": "class Solution {\n    maxSubArray(nums) {\n        let maxCurrent = maxGlobal = nums[0];\n        for (let i = 1; i < nums.length; i++) {\n            maxCurrent = Math.max(nums[i], maxCurrent + nums[i]);\n            maxGlobal = Math.max(maxGlobal, maxCurrent);\n        }\n        return maxGlobal;\n    }\n}",
        "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        int maxCurrent = maxGlobal = nums[0];\n        for (int i = 1; i < nums.length; i++) {\n            maxCurrent = Math.max(nums[i], maxCurrent + nums[i]);\n            maxGlobal = Math.max(maxGlobal, maxCurrent);\n        }\n        return maxGlobal;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        int maxCurrent = maxGlobal = nums[0];\n        for (int i = 1; i < nums.size(); i++) {\n            maxCurrent = max(nums[i], maxCurrent + nums[i]);\n            maxGlobal = max(maxGlobal, maxCurrent);\n        }\n        return maxGlobal;\n    }\n};"
    },
    "Binary Search": {
        "python": "class Solution:\n    def search(self, nums, target):\n        left, right = 0, len(nums) - 1\n        while left <= right:\n            mid = (left + right) // 2\n            if nums[mid] == target: return mid\n            elif nums[mid] < target: left = mid + 1\n            else: right = mid - 1\n        return -1",
        "javascript": "class Solution {\n    search(nums, target) {\n        let left = 0, right = nums.length - 1;\n        while (left <= right) {\n            let mid = Math.floor((left + right) / 2);\n            if (nums[mid] === target) return mid;\n            else if (nums[mid] < target) left = mid + 1;\n            else right = mid - 1;\n        }\n        return -1;\n    }\n}",
        "java": "class Solution {\n    public int search(int[] nums, int target) {\n        int left = 0, right = nums.length - 1;\n        while (left <= right) {\n            int mid = left + (right - left) / 2;\n            if (nums[mid] == target) return mid;\n            else if (nums[mid] < target) left = mid + 1;\n            else right = mid - 1;\n        }\n        return -1;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        int left = 0, right = nums.size() - 1;\n        while (left <= right) {\n            int mid = left + (right - left) / 2;\n            if (nums[mid] == target) return mid;\n            else if (nums[mid] < target) left = mid + 1;\n            else right = mid - 1;\n        }\n        return -1;\n    }\n};"
    },
    "Longest Common Prefix": {
        "python": "class Solution:\n    def longestCommonPrefix(self, strs):\n        if not strs: return \"\"\n        for i in range(len(strs[0])):\n            for j in range(1, len(strs)):\n                if i >= len(strs[j]) or strs[j][i] != strs[0][i]: return strs[0][:i]\n        return strs[0]",
        "javascript": "class Solution {\n    longestCommonPrefix(strs) {\n        if (!strs.length) return \"\";\n        for (let i = 0; i < strs[0].length; i++) {\n            for (let j = 1; j < strs.length; j++) {\n                if (i >= strs[j].length || strs[j][i] !== strs[0][i]) return strs[0].substring(0, i);\n            }\n        }\n        return strs[0];\n    }\n}",
        "java": "class Solution {\n    public String longestCommonPrefix(String[] strs) {\n        if (strs.length == 0) return \"\";\n        for (int i = 0; i < strs[0].length(); i++) {\n            for (int j = 1; j < strs.length; j++) {\n                if (i >= strs[j].length() || strs[j].charAt(i) != strs[0].charAt(i)) return strs[0].substring(0, i);\n            }\n        }\n        return strs[0];\n    }\n}",
        "cpp": "class Solution {\npublic:\n    string longestCommonPrefix(vector<string>& strs) {\n        if (strs.empty()) return \"\";\n        for (int i = 0; i < strs[0].length(); i++) {\n            for (int j = 1; j < strs.size(); j++) {\n                if (i >= strs[j].length() || strs[j][i] != strs[0][i]) return strs[0].substr(0, i);\n            }\n        }\n        return strs[0];\n    }\n};"
    },
    "Number of Islands": {
        "python": "class Solution:\n    def numIslands(self, grid):\n        if not grid: return 0\n        def dfs(i, j):\n            if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[i]) or grid[i][j] == '0': return\n            grid[i][j] = '0'\n            dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1)\n        count = 0\n        for i in range(len(grid)):\n            for j in range(len(grid[i])):\n                if grid[i][j] == '1':\n                    dfs(i, j); count += 1\n        return count",
        "javascript": "class Solution {\n    numIslands(grid) {\n        if (!grid || !grid.length) return 0;\n        const dfs = (i, j) => {\n            if (i < 0 || i >= grid.length || j < 0 || j >= grid[i].length || grid[i][j] === '0') return;\n            grid[i][j] = '0';\n            dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1);\n        };\n        let count = 0;\n        for (let i = 0; i < grid.length; i++) {\n            for (let j = 0; j < grid[i].length; j++) {\n                if (grid[i][j] === '1') { dfs(i, j); count++; }\n            }\n        }\n        return count;\n    }\n}",
        "java": "class Solution {\n    public int numIslands(char[][] grid) {\n        if (grid == null || grid.length == 0) return 0;\n        int count = 0;\n        for (int i = 0; i < grid.length; i++) {\n            for (int j = 0; j < grid[i].length; j++) {\n                if (grid[i][j] == '1') { dfs(grid, i, j); count++; }\n            }\n        }\n        return count;\n    }\n    private void dfs(char[][] grid, int i, int j) {\n        if (i < 0 || i >= grid.length || j < 0 || j >= grid[i].length || grid[i][j] == '0') return;\n        grid[i][j] = '0';\n        dfs(grid, i+1, j); dfs(grid, i-1, j); dfs(grid, i, j+1); dfs(grid, i, j-1);\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        if (grid.empty()) return 0;\n        int count = 0;\n        for (int i = 0; i < grid.size(); i++) {\n            for (int j = 0; j < grid[i].size(); j++) {\n                if (grid[i][j] == '1') { dfs(grid, i, j); count++; }\n            }\n        }\n        return count;\n    }\nprivate:\n    void dfs(vector<vector<char>>& grid, int i, int j) {\n        if (i < 0 || i >= grid.size() || j < 0 || j >= grid[i].size() || grid[i][j] == '0') return;\n        grid[i][j] = '0';\n        dfs(grid, i+1, j); dfs(grid, i-1, j); dfs(grid, i, j+1); dfs(grid, i, j-1);\n    }\n};"
    },
    "Merge Intervals": {
        "python": "class Solution:\n    def merge(self, intervals):\n        intervals.sort()\n        merged = [intervals[0]]\n        for i in range(1, len(intervals)):\n            if intervals[i][0] <= merged[-1][1]:\n                merged[-1][1] = max(merged[-1][1], intervals[i][1])\n            else: merged.append(intervals[i])\n        return merged",
        "javascript": "class Solution {\n    merge(intervals) {\n        intervals.sort((a, b) => a[0] - b[0]);\n        let merged = [intervals[0]];\n        for (let i = 1; i < intervals.length; i++) {\n            if (intervals[i][0] <= merged[merged.length-1][1]) {\n                merged[merged.length-1][1] = Math.max(merged[merged.length-1][1], intervals[i][1]);\n            } else { merged.push(intervals[i]); }\n        }\n        return merged;\n    }\n}",
        "java": "class Solution {\n    public int[][] merge(int[][] intervals) {\n        java.util.Arrays.sort(intervals, (a, b) -> a[0] - b[0]);\n        java.util.List<int[]> merged = new java.util.ArrayList<>();\n        merged.add(intervals[0]);\n        for (int i = 1; i < intervals.length; i++) {\n            if (intervals[i][0] <= merged.get(merged.size()-1)[1]) {\n                merged.get(merged.size()-1)[1] = Math.max(merged.get(merged.size()-1)[1], intervals[i][1]);\n            } else { merged.add(intervals[i]); }\n        }\n        return merged.toArray(new int[0][]);\n    }\n}",
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> merge(vector<vector<int>>& intervals) {\n        sort(intervals.begin(), intervals.end());\n        vector<vector<int>> merged; merged.push_back(intervals[0]);\n        for (int i = 1; i < intervals.size(); i++) {\n            if (intervals[i][0] <= merged.back()[1]) {\n                merged.back()[1] = max(merged.back()[1], intervals[i][1]);\n            } else { merged.push_back(intervals[i]); }\n        }\n        return merged;\n    }\n};"
    },
    "Coin Change": {
        "python": "class Solution:\n    def coinChange(self, coins, amount):\n        dp = [float('inf')] * (amount + 1)\n        dp[0] = 0\n        for i in range(1, amount + 1):\n            for coin in coins:\n                if coin <= i: dp[i] = min(dp[i], dp[i - coin] + 1)\n        return dp[amount] if dp[amount] != float('inf') else -1",
        "javascript": "class Solution {\n    coinChange(coins, amount) {\n        const dp = Array(amount + 1).fill(Infinity);\n        dp[0] = 0;\n        for (let i = 1; i <= amount; i++) {\n            for (let coin of coins) {\n                if (coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);\n            }\n        }\n        return dp[amount] === Infinity ? -1 : dp[amount];\n    }\n}",
        "java": "class Solution {\n    public int coinChange(int[] coins, int amount) {\n        int[] dp = new int[amount + 1];\n        java.util.Arrays.fill(dp, amount + 1);\n        dp[0] = 0;\n        for (int i = 1; i <= amount; i++) {\n            for (int coin : coins) {\n                if (coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n}",
        "cpp": "class Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        vector<int> dp(amount + 1, amount + 1);\n        dp[0] = 0;\n        for (int i = 1; i <= amount; i++) {\n            for (int coin : coins) {\n                if (coin <= i) dp[i] = min(dp[i], dp[i - coin] + 1);\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n};"
    },
    "Word Search": {
        "python": "class Solution:\n    def exist(self, board, word):\n        def dfs(i, j, k):\n            if k == len(word): return True\n            if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]) or board[i][j] != word[k]: return False\n            board[i][j] = ''\n            res = dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or dfs(i, j+1, k+1) or dfs(i, j-1, k+1)\n            board[i][j] = word[k]\n            return res\n        for i in range(len(board)):\n            for j in range(len(board[i])):\n                if dfs(i, j, 0): return True\n        return False",
        "javascript": "class Solution {\n    exist(board, word) {\n        const dfs = (i, j, k) => {\n            if (k === word.length) return true;\n            if (i < 0 || i >= board.length || j < 0 || j >= board[i].length || board[i][j] !== word[k]) return false;\n            board[i][j] = '';\n            const res = dfs(i+1, j, k+1) || dfs(i-1, j, k+1) || dfs(i, j+1, k+1) || dfs(i, j-1, k+1);\n            board[i][j] = word[k];\n            return res;\n        };\n        for (let i = 0; i < board.length; i++) {\n            for (let j = 0; j < board[i].length; j++) {\n                if (dfs(i, j, 0)) return true;\n            }\n        }\n        return false;\n    }\n}",
        "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        for (int i = 0; i < board.length; i++) {\n            for (int j = 0; j < board[i].length; j++) {\n                if (dfs(board, word, i, j, 0)) return true;\n            }\n        }\n        return false;\n    }\n    private boolean dfs(char[][] board, String word, int i, int j, int k) {\n        if (k == word.length()) return true;\n        if (i < 0 || i >= board.length || j < 0 || j >= board[i].length || board[i][j] != word.charAt(k)) return false;\n        board[i][j] = '\\0';\n        boolean res = dfs(board, word, i+1, j, k+1) || dfs(board, word, i-1, j, k+1) || dfs(board, word, i, j+1, k+1) || dfs(board, word, i, j-1, k+1);\n        board[i][j] = word.charAt(k);\n        return res;\n    }\n}",
        "cpp": "class Solution {\npublic:\n    bool exist(vector<vector<char>>& board, string word) {\n        for (int i = 0; i < board.size(); i++) {\n            for (int j = 0; j < board[i].size(); j++) {\n                if (dfs(board, word, i, j, 0)) return true;\n            }\n        }\n        return false;\n    }\nprivate:\n    bool dfs(vector<vector<char>>& board, string& word, int i, int j, int k) {\n        if (k == word.length()) return true;\n        if (i < 0 || i >= board.size() || j < 0 || j >= board[i].size() || board[i][j] != word[k]) return false;\n        board[i][j] = '\\0';\n        bool res = dfs(board, word, i+1, j, k+1) || dfs(board, word, i-1, j, k+1) || dfs(board, word, i, j+1, k+1) || dfs(board, word, i, j-1, k+1);\n        board[i][j] = word[k];\n        return res;\n    }\n};"
    }
}

# Get all problems
print("Fetching problems...")
response = requests.get(f"{BASE_URL}/problems/")
problems = response.json()
problem_map = {p["title"].lower(): p for p in problems}

print(f"Found {len(problems)} problems")
print("=" * 80)
print("TESTING ALL 12 PROBLEMS ACROSS 4 LANGUAGES (48 TOTAL TESTS)")
print("=" * 80)

results = {}
total_pass = 0
total_fail = 0
problem_order = ["Two Sum", "Valid Parentheses", "Reverse Linked List", "Maximum Subarray", 
                 "Best Time to Buy and Sell Stock", "Climbing Stairs", "Binary Search", 
                 "Longest Common Prefix", "Number of Islands", "Merge Intervals", "Coin Change", "Word Search"]

for problem_name in problem_order:
    if problem_name not in test_suites:
        continue
    
    codes = test_suites[problem_name]
    print(f"\n{problem_name}:")
    problem = problem_map.get(problem_name.lower())
    
    if not problem:
        print(f"  ⚠️  Problem not found in system")
        continue
    
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
            
            print(f"  {marker} {language:12} Status={status:15} Passed={passed}/{total}")
            
        except Exception as e:
            print(f"  ❌ {language:12} ERROR: {str(e)[:50]}")
            total_fail += 1

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"✅ Passed: {total_pass}/48")
print(f"❌ Failed: {total_fail}/48")
print(f"Success Rate: {100*total_pass/48:.1f}%")
