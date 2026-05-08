"""
app/services/code_wrapper.py
Wraps user-submitted Solution class with automatic input parsing and output capture.
Supports all 12 problems. Users only submit the Solution class — no boilerplate needed.
"""
import re


def wrap_solution(code: str, problem_title: str, input_data: str) -> str:
    """
    Main entry point. Detects problem type from title and wraps accordingly.
    Returns complete executable Python code.
    """
    title_lower = problem_title.lower()

    if "two sum" in title_lower:
        return _wrap_two_sum(code, input_data)
    elif "valid parentheses" in title_lower:
        return _wrap_valid_parentheses(code, input_data)
    elif "reverse linked list" in title_lower:
        return _wrap_reverse_linked_list(code, input_data)
    elif "maximum subarray" in title_lower:
        return _wrap_maximum_subarray(code, input_data)
    elif "best time" in title_lower:
        return _wrap_best_time(code, input_data)
    elif "climbing stairs" in title_lower:
        return _wrap_climbing_stairs(code, input_data)
    elif "binary search" in title_lower:
        return _wrap_binary_search(code, input_data)
    elif "longest common prefix" in title_lower:
        return _wrap_longest_common_prefix(code, input_data)
    elif "number of islands" in title_lower:
        return _wrap_number_of_islands(code, input_data)
    elif "merge intervals" in title_lower:
        return _wrap_merge_intervals(code, input_data)
    elif "coin change" in title_lower:
        return _wrap_coin_change(code, input_data)
    elif "word search" in title_lower:
        return _wrap_word_search(code, input_data)
    else:
        return _wrap_generic(code, input_data)


def wrap_python_solution(user_code: str, test_input: str) -> str:
    """Backward-compatible wrapper used by existing execution service calls."""
    if "def twoSum" in user_code:
        return _wrap_two_sum(user_code, test_input)
    elif "def isValid" in user_code:
        return _wrap_valid_parentheses(user_code, test_input)
    elif "def reverseList" in user_code:
        return _wrap_reverse_linked_list(user_code, test_input)
    elif "def maxSubArray" in user_code:
        return _wrap_maximum_subarray(user_code, test_input)
    elif "def maxProfit" in user_code:
        return _wrap_best_time(user_code, test_input)
    elif "def climbStairs" in user_code:
        return _wrap_climbing_stairs(user_code, test_input)
    elif "def search" in user_code:
        return _wrap_binary_search(user_code, test_input)
    elif "def longestCommonPrefix" in user_code:
        return _wrap_longest_common_prefix(user_code, test_input)
    elif "def numIslands" in user_code:
        return _wrap_number_of_islands(user_code, test_input)
    elif "def merge" in user_code:
        return _wrap_merge_intervals(user_code, test_input)
    elif "def coinChange" in user_code:
        return _wrap_coin_change(user_code, test_input)
    elif "def exist" in user_code:
        return _wrap_word_search(user_code, test_input)
    return _wrap_generic(user_code, test_input)


# ── Problem-specific wrappers ─────────────────────────────────────────────────

def _wrap_two_sum(code: str, input_data: str) -> str:
    return code + f'''
import json as _json
_lines = """{input_data}""".strip().split("\\n")
_nums = _json.loads(_lines[0])
_target = int(_lines[1])
print(Solution().twoSum(_nums, _target))
'''

def _wrap_valid_parentheses(code: str, input_data: str) -> str:
    return code + f'''
_s = """{input_data}""".strip()
print(Solution().isValid(_s))
'''

def _wrap_reverse_linked_list(code: str, input_data: str) -> str:
    return code + f'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

_vals = list(map(int, """{input_data}""".strip().split()))
_head = None
for _v in reversed(_vals):
    _head = ListNode(_v, _head)
_result = Solution().reverseList(_head)
_out = []
while _result:
    _out.append(str(_result.val))
    _result = _result.next
print(" ".join(_out))
'''

def _wrap_maximum_subarray(code: str, input_data: str) -> str:
    return code + f'''
_nums = list(map(int, """{input_data}""".strip().split()))
print(Solution().maxSubArray(_nums))
'''

def _wrap_best_time(code: str, input_data: str) -> str:
    return code + f'''
_prices = list(map(int, """{input_data}""".strip().split()))
print(Solution().maxProfit(_prices))
'''

def _wrap_climbing_stairs(code: str, input_data: str) -> str:
    return code + f'''
_n = int("""{input_data}""".strip())
print(Solution().climbStairs(_n))
'''

def _wrap_binary_search(code: str, input_data: str) -> str:
    return code + f'''
_lines = """{input_data}""".strip().split("\\n")
_nums = list(map(int, _lines[0].split()))
_target = int(_lines[1])
print(Solution().search(_nums, _target))
'''

def _wrap_longest_common_prefix(code: str, input_data: str) -> str:
    return code + f'''
_strs = """{input_data}""".strip().split()
print(Solution().longestCommonPrefix(_strs))
'''

def _wrap_number_of_islands(code: str, input_data: str) -> str:
    return code + f'''
_lines = """{input_data}""".strip().split("\\n")
_m, _n = map(int, _lines[0].split())
_grid = [_lines[i+1].split() for i in range(_m)]
print(Solution().numIslands(_grid))
'''

def _wrap_merge_intervals(code: str, input_data: str) -> str:
    return code + f'''
_lines = """{input_data}""".strip().split("\\n")
_count = int(_lines[0])
_intervals = [list(map(int, _lines[i+1].split())) for i in range(_count)]
_result = Solution().merge(_intervals)
for _iv in _result:
    print(" ".join(map(str, _iv)))
'''

def _wrap_coin_change(code: str, input_data: str) -> str:
    return code + f'''
_lines = """{input_data}""".strip().split("\\n")
_coins = list(map(int, _lines[0].split()))
_amount = int(_lines[1])
print(Solution().coinChange(_coins, _amount))
'''

def _wrap_word_search(code: str, input_data: str) -> str:
    return code + f'''
_lines = """{input_data}""".strip().split("\\n")
_m, _n = map(int, _lines[0].split())
_board = [_lines[i+1].split() for i in range(_m)]
_word = _lines[_m+1]
print(Solution().exist(_board, _word))
'''

def _wrap_generic(code: str, input_data: str) -> str:
    """Fallback: just run code with input via stdin."""
    return code + f'''
# Generic execution fallback
'''
