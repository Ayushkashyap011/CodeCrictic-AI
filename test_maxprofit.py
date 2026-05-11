import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test Best Time to Buy and Sell Stock with JavaScript
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

# Get Best Time problem
problems = requests.get(f"{BASE_URL}/problems/").json()
best_time = next(p for p in problems if "best time" in p["title"].lower())
problem_id = best_time["id"]
print(f"Testing: {best_time['title']}\n")
print(f"Problem ID: {problem_id}\n")

# Test examples
print("Examples from problem.json:")
for i, ex in enumerate(best_time['examples'], 1):
    print(f"  Example {i}: {ex['input']} => {ex['output']}")

print("\n" + "="*60)
print("Testing JavaScript...")
print("="*60)
response = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": js_code, "language": "javascript", "problem_id": problem_id}
)
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('test_results'):
    for test in result['test_results']:
        print(f"  Test {test['test_number']}: actual={test.get('actual')} expected={test.get('expected')} error={test.get('error')}")
