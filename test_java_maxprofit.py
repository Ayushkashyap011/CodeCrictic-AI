import requests
import time
import json

time.sleep(2)
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test maxProfit with Java
java_code = """public class Solution {
    public int maxProfit(int[] prices) {
        if (prices == null || prices.length < 2) return 0;
        int minBuyPrice = Integer.MAX_VALUE, maxProfit = 0;
        for (int price : prices) {
            maxProfit = Math.max(maxProfit, price - minBuyPrice);
            minBuyPrice = Math.min(minBuyPrice, price);
        }
        return maxProfit;
    }
}"""

try:
    problems = requests.get(f"{BASE_URL}/problems/").json()
    prob = [p for p in problems if "Best Time" in p.get("title", "")][0]
    
    result = requests.post(f"{BASE_URL}/execute/run", json={"code": java_code, "language": "java", "problem_id": prob["id"]}).json()
    print(f"Status: {result.get('status')}")
    print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
    for test in result.get("test_results", []):
        print(f"  Test {test['test_number']}: {test.get('error') or 'OK - ' + str(test.get('actual'))}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
