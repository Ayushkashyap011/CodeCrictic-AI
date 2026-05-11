import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
best_time = next(p for p in problems if "best time" in p["title"].lower())
problem_id = best_time["id"]

print(f"Problem: {best_time['title']}")
print(f"Problem ID: {problem_id}\n")

# Test JavaScript
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

print("Testing JavaScript with maxProfit:")
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": js_code, "language": "javascript", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")

if result.get('test_results'):
    for test in result['test_results']:
        print(f"\nTest {test['test_number']}:")
        print(f"  Input: {test.get('input')}")
        print(f"  Expected: {test.get('expected')}")
        print(f"  Actual: {test.get('actual')}")
        if test.get('error'):
            print(f"  Error: {test.get('error')}")
