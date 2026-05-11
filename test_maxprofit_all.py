import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get Best Time problem
problems = requests.get(f"{BASE_URL}/problems/").json()
best_time = next(p for p in problems if "best time" in p["title"].lower())
problem_id = best_time["id"]

# Test codes for all languages
js_code = """
class Solution {
    maxProfit(prices) {
        let maxProfit = 0;
        let minPrice = prices[0];
        for (let price of prices) {
            maxProfit = Math.max(maxProfit, price - minPrice);
            minPrice = Math.min(minPrice, price);
        }
        return maxProfit;
    }
}
"""

java_code = """
class Solution {
    public int maxProfit(int[] prices) {
        int maxProfit = 0;
        int minPrice = prices[0];
        for (int price : prices) {
            maxProfit = Math.max(maxProfit, price - minPrice);
            minPrice = Math.min(minPrice, price);
        }
        return maxProfit;
    }
}
"""

cpp_code = """
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxProfit = 0;
        int minPrice = prices[0];
        for (int price : prices) {
            maxProfit = max(maxProfit, price - minPrice);
            minPrice = min(minPrice, price);
        }
        return maxProfit;
    }
};
"""

print(f"Testing: {best_time['title']}\n")

for lang_code, lang_name in [(js_code, "javascript"), (java_code, "java"), (cpp_code, "cpp")]:
    response = requests.post(
        f"{BASE_URL}/execute/run",
        json={"code": lang_code, "language": lang_name, "problem_id": problem_id}
    )
    result = response.json()
    status = result.get('status')
    passed = result.get('passed_count')
    total = result.get('total_count')
    print(f"{lang_name.upper():12} Status={status:12} Passed={passed}/{total}")
