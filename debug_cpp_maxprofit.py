import subprocess
import re
import tempfile
import os

# Test C++ maxProfit wrapper generation
problem_title = "Best Time to Buy and Sell Stock"

code_cpp = """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if (prices.empty() || prices.size() < 2) return 0;
        int minBuyPrice = INT_MAX;
        int maxProfit = 0;
        for (int price : prices) {
            maxProfit = max(maxProfit, price - minBuyPrice);
            minBuyPrice = min(minBuyPrice, price);
        }
        return maxProfit;
    }
};"""

# Import the wrapper
import sys
sys.path.insert(0, r'c:\Users\kashy\OneDrive\Desktop\code\CodeCrictic-AI\backend\app')
from services.code_wrapper import wrap_solution

# Generate wrapped code - signature: wrap_solution(code, problem_title, input_data, language)
test_input = "7 1 5 3 6 4"  # First test case
wrapped_code = wrap_solution(code_cpp, problem_title, test_input, "cpp")
print("Generated C++ Code:")
print("=" * 80)
print(wrapped_code)
print("=" * 80)

# Try to compile
with tempfile.TemporaryDirectory() as tmpdir:
    cpp_file = os.path.join(tmpdir, "Main.cpp")
    exe_file = os.path.join(tmpdir, "Main.exe")
    
    with open(cpp_file, 'w') as f:
        f.write(wrapped_code)
    
    # Compile
    result = subprocess.run(
        f'cd {tmpdir} && g++ -o Main.exe Main.cpp 2>&1',
        shell=True,
        capture_output=True,
        text=True
    )
    
    print("\nCompilation output:")
    if result.returncode == 0:
        print("✅ Compilation successful!")
        
        # Try to run
        run_result = subprocess.run(
            f'{exe_file}',
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        print("\nExecution output:")
        print(run_result.stdout)
        if run_result.stderr:
            print("Errors:", run_result.stderr)
    else:
        print("❌ Compilation failed:")
        print(result.stdout)
        print(result.stderr)
