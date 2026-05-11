import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get all problems
resp = requests.get(f"{BASE_URL}/problems/")
problems = resp.json()

# Find maxProfit problem
max_profit_problem = None
for p in problems:
    print(f"  {p['title']}")
    if "best time" in p["title"].lower() or "max profit" in p["title"].lower():
        max_profit_problem = p
        break

if not max_profit_problem:
    print("\nERROR: Best Time to Buy and Sell Stock problem not found!")
    print(f"Available problems: {[p['title'] for p in problems]}")
    exit(1)

print(f"\nFound problem: {max_profit_problem['title']}")
print(f"Problem ID: {max_profit_problem['id']}")

# Test code
java_code = """
public class Solution {
    public int maxProfit(int[] prices) {
        if (prices == null || prices.length < 2) {
            return 0;
        }
        int minBuyPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        for (int currentPrice : prices) {
            if (currentPrice < minBuyPrice) {
                minBuyPrice = currentPrice;
            } else {
                int potentialProfit = currentPrice - minBuyPrice;
                if (potentialProfit > maxProfit) {
                    maxProfit = potentialProfit;
                }
            }
        }
        return maxProfit;
    }
}
"""

print("\nTesting maxProfit with Java...")
resp = requests.post(
    f"{BASE_URL}/execute/run",
    json={
        "code": java_code,
        "language": "java",
        "problem_id": max_profit_problem["id"]
    }
)

result = resp.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
print(f"Full response: {result}")
