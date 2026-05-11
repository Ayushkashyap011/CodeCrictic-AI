import requests
import subprocess

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get problems
problems = requests.get(f"{BASE_URL}/problems/").json()
two_sum = next((p for p in problems if p["title"].lower() == "two sum"), None)

# C++ Two Sum  
cpp_code = """
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
"""

# Add required includes and main
full_cpp_code = cpp_code + """

int main() {
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;
    vector<int> result = Solution().twoSum(nums, target);
    cout << "[";
    for (int i = 0; i < result.size(); i++) {
        if (i > 0) cout << ",";
        cout << result[i];
    }
    cout << "]" << endl;
    return 0;
}
"""

# Print what will be tested
print("C++ code that will be sent:")
print("="*60)
print(full_cpp_code)
print("="*60)

# Try to compile it locally
print("\nTesting local compilation with g++:")
try:
    result = subprocess.run(
        ["g++", "-x", "c++", "-o", "test_cpp", "-"],
        input=full_cpp_code,
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print("SUCCESS: Code compiled locally!")
    else:
        print(f"COMPILATION ERROR:\n{result.stderr}")
except Exception as e:
    print(f"Error: {e}")

# Now test via API
print("\n\nTesting via API:")
resp = requests.post(
    f"{BASE_URL}/execute/run",
    json={"code": cpp_code, "language": "cpp", "problem_id": two_sum["id"]}
)
result = resp.json()
print(f"Status: {result.get('status')}")
print(f"Passed: {result.get('passed_count')}/{result.get('total_count')}")
if result.get('compile_output'):
    print(f"Compile Error: {result.get('compile_output')[:200]}")
