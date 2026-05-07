"""
code_wrapper.py
Wraps user solution code to automatically handle input parsing.
Users submit only the Solution class, backend handles I/O and test execution.
"""

def wrap_python_solution(user_code: str, test_input: str) -> str:
    """
    Wraps user's Solution class with input parsing and function calling.
    Embeds test input directly to avoid stdin issues.
    
    Supports multiple problem types:
    - twoSum: JSON lists and integers
    - coinChange: space-separated integers
    - Valid Parentheses: string
    - Other problems: generic parsing
    
    Example:
    - User submits: class Solution: def twoSum(self, nums, target): ...
    - Backend wraps it with: parse input, call method, print result
    """
    
    # Pre-process the test input
    lines = test_input.strip().split('\n')
    
    # Detect which method is being defined in the user code
    method_name = None
    if 'def twoSum' in user_code:
        method_name = 'twoSum'
    elif 'def coinChange' in user_code:
        method_name = 'coinChange'
    elif 'def isValid' in user_code:
        method_name = 'isValid'
    elif 'def merge' in user_code:
        method_name = 'merge'
    elif 'def exist' in user_code:
        method_name = 'exist'
    
    # Build wrapper code based on method type
    if method_name == 'twoSum':
        wrapper_code = f"""import json

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    # Parse input for twoSum: JSON list and integer
    nums = json.loads(test_lines[0])
    target = int(test_lines[1])
    
    # Create solution instance and call method
    solution = Solution()
    result = solution.twoSum(nums, target)
    
    # Print result
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    elif method_name == 'coinChange':
        wrapper_code = f"""import json
from typing import List

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    # Parse input for coinChange: space-separated integers, then amount
    coins = list(map(int, test_lines[0].split()))
    amount = int(test_lines[1])
    
    # Create solution instance and call method
    solution = Solution()
    result = solution.coinChange(coins, amount)
    
    # Print result
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    elif method_name == 'isValid':
        wrapper_code = f"""import json

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    # Parse input for isValid: just a string
    s = test_lines[0]
    
    # Create solution instance and call method
    solution = Solution()
    result = solution.isValid(s)
    
    # Print result
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    elif method_name == 'merge':
        wrapper_code = f"""import json
from typing import List

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    # Parse input for merge: number of intervals, then intervals
    n = int(test_lines[0])
    intervals = [list(map(int, test_lines[i+1].split())) for i in range(n)]
    
    # Create solution instance and call method
    solution = Solution()
    result = solution.merge(intervals)
    
    # Print result
    for interval in result:
        print(' '.join(map(str, interval)))
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    elif method_name == 'exist':
        wrapper_code = f"""import json
from typing import List

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    # Parse input for exist: grid dimensions, then grid rows, then word
    m, n = map(int, test_lines[0].split())
    board = [test_lines[i+1].split() for i in range(m)]
    word = test_lines[m+1]
    
    # Create solution instance and call method
    solution = Solution()
    result = solution.exist(board, word)
    
    # Print result
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    else:
        # Generic fallback
        wrapper_code = f"""import json

{user_code}

# Test input embedded by backend
test_lines = {repr(lines)}

try:
    print("Unknown problem type")
except Exception as e:
    import traceback
    traceback.print_exc()
"""
    
    return wrapper_code
