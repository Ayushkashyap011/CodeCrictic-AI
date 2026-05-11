"""
app/services/code_wrapper.py
Wraps user-submitted Solution class with automatic input parsing and output capture.
Supports all 12 problems in all 4 languages. Users only submit the Solution class — no boilerplate needed.
"""
import re


def wrap_solution(code: str, problem_title: str, input_data: str, language: str) -> str:
    """
    Main entry point. Detects problem type from title and wraps accordingly.
    Returns complete executable code for the given language.
    """
    title_lower = problem_title.lower()

    if "two sum" in title_lower:
        return _wrap_two_sum(code, input_data, language)
    elif "valid parentheses" in title_lower:
        return _wrap_valid_parentheses(code, input_data, language)
    elif "reverse linked list" in title_lower:
        return _wrap_reverse_linked_list(code, input_data, language)
    elif "maximum subarray" in title_lower:
        return _wrap_maximum_subarray(code, input_data, language)
    elif "best time" in title_lower:
        return _wrap_best_time(code, input_data, language)
    elif "climbing stairs" in title_lower:
        return _wrap_climbing_stairs(code, input_data, language)
    elif "binary search" in title_lower:
        return _wrap_binary_search(code, input_data, language)
    elif "longest common prefix" in title_lower:
        return _wrap_longest_common_prefix(code, input_data, language)
    elif "number of islands" in title_lower:
        return _wrap_number_of_islands(code, input_data, language)
    elif "merge intervals" in title_lower:
        return _wrap_merge_intervals(code, input_data, language)
    elif "coin change" in title_lower:
        return _wrap_coin_change(code, input_data, language)
    elif "word search" in title_lower:
        return _wrap_word_search(code, input_data, language)
    else:
        return code


def wrap_python_solution(user_code: str, test_input: str) -> str:
    """Backward-compatible wrapper used by existing execution service calls."""
    if "def twoSum" in user_code:
        return _wrap_two_sum(user_code, test_input, "python")
    elif "def isValid" in user_code:
        return _wrap_valid_parentheses(user_code, test_input, "python")
    elif "def reverseList" in user_code:
        return _wrap_reverse_linked_list(user_code, test_input, "python")
    elif "def maxSubArray" in user_code:
        return _wrap_maximum_subarray(user_code, test_input, "python")
    elif "def maxProfit" in user_code:
        return _wrap_best_time(user_code, test_input, "python")
    elif "def climbStairs" in user_code:
        return _wrap_climbing_stairs(user_code, test_input, "python")
    elif "def search" in user_code:
        return _wrap_binary_search(user_code, test_input, "python")
    elif "def longestCommonPrefix" in user_code:
        return _wrap_longest_common_prefix(user_code, test_input, "python")
    elif "def numIslands" in user_code:
        return _wrap_number_of_islands(user_code, test_input, "python")
    elif "def merge" in user_code:
        return _wrap_merge_intervals(user_code, test_input, "python")
    elif "def coinChange" in user_code:
        return _wrap_coin_change(user_code, test_input, "python")
    elif "def exist" in user_code:
        return _wrap_word_search(user_code, test_input, "python")
    return user_code


# ── Two Sum ───────────────────────────────────────────────────────────────────

def _wrap_two_sum(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    nums_json = lines[0]
    target = int(lines[1])
    
    if language == "python":
        return code + f'''
import json as _json
_nums = _json.loads("""{nums_json}""")
_target = {target}
print(Solution().twoSum(_nums, _target))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[] nums = {{{", ".join(nums_json.strip("[]").split(","))}}};
        int target = {target};
        int[] result = new Solution().twoSum(nums, target);
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < result.length; i++) {{
            if (i > 0) sb.append(",");
            sb.append(result[i]);
        }}
        sb.append("]");
        System.out.println(sb.toString());
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const nums = {nums_json};
const target = {target};
const result = new Solution().twoSum(nums, target);
console.log("[" + result.join(",") + "]");
'''
    elif language == "cpp":
        nums_list = ", ".join(nums_json.strip("[]").split(","))
        # Add necessary includes if not already present
        if "#include" not in code:
            code = "#include <vector>\n#include <unordered_map>\n#include <iostream>\nusing namespace std;\n\n" + code
        return code + f'''

int main() {{
    vector<int> nums = {{{nums_list}}};
    int target = {target};
    vector<int> result = Solution().twoSum(nums, target);
    cout << "[";
    for (int i = 0; i < result.size(); i++) {{
        if (i > 0) cout << ",";
        cout << result[i];
    }}
    cout << "]" << endl;
    return 0;
}}
'''
    return code


# ── Valid Parentheses ─────────────────────────────────────────────────────────

def _wrap_valid_parentheses(code: str, input_data: str, language: str) -> str:
    s = input_data.strip()
    
    if language == "python":
        return code + f'''
_s = """{s}"""
print(Solution().isValid(_s))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        String s = "{s}";
        System.out.println(new Solution().isValid(s));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const s = "{s}";
console.log(new Solution().isValid(s));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    string s = "{s}";
    cout << (new Solution()->isValid(s) ? "true" : "false") << endl;
    delete new Solution();
    return 0;
}}
'''
    return code


# ── Reverse Linked List ───────────────────────────────────────────────────────

def _wrap_reverse_linked_list(code: str, input_data: str, language: str) -> str:
    vals = list(map(int, input_data.strip().split()))
    
    if language == "python":
        return code + f'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

_vals = {vals}
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
    elif language == "java":
        return code + f'''

class ListNode {{
    int val;
    ListNode next;
    ListNode() {{}}
    ListNode(int val) {{ this.val = val; }}
}}

public class Main {{
    public static void main(String[] args) {{
        int[] vals = {{{", ".join(map(str, vals))}}};
        ListNode head = null;
        for (int i = vals.length - 1; i >= 0; i--) {{
            ListNode node = new ListNode(vals[i]);
            node.next = head;
            head = node;
        }}
        ListNode result = new Solution().reverseList(head);
        StringBuilder sb = new StringBuilder();
        while (result != null) {{
            if (sb.length() > 0) sb.append(" ");
            sb.append(result.val);
            result = result.next;
        }}
        System.out.println(sb.toString());
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

class ListNode {{
    constructor(val = 0, next = null) {{
        this.val = val;
        this.next = next;
    }}
}}

const vals = {vals};
let head = null;
for (let i = vals.length - 1; i >= 0; i--) {{
    const node = new ListNode(vals[i]);
    node.next = head;
    head = node;
}}
let result = new Solution().reverseList(head);
const output = [];
while (result) {{
    output.push(result.val);
    result = result.next;
}}
console.log(output.join(" "));
'''
    elif language == "cpp":
        return code + f'''

struct ListNode {{
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {{}}
}};

int main() {{
    vector<int> vals = {{{", ".join(map(str, vals))}}};
    ListNode *head = NULL;
    for (int i = vals.size() - 1; i >= 0; i--) {{
        ListNode *node = new ListNode(vals[i]);
        node->next = head;
        head = node;
    }}
    ListNode *result = Solution().reverseList(head);
    bool first = true;
    while (result) {{
        if (!first) cout << " ";
        cout << result->val;
        result = result->next;
        first = false;
    }}
    cout << endl;
    return 0;
}}
'''
    return code


# ── Maximum Subarray ──────────────────────────────────────────────────────────

def _wrap_maximum_subarray(code: str, input_data: str, language: str) -> str:
    nums = list(map(int, input_data.strip().split()))
    
    if language == "python":
        return code + f'''
_nums = {nums}
print(Solution().maxSubArray(_nums))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[] nums = {{{", ".join(map(str, nums))}}};
        System.out.println(new Solution().maxSubArray(nums));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const nums = {nums};
console.log(new Solution().maxSubArray(nums));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<int> nums = {{{", ".join(map(str, nums))}}};
    cout << Solution().maxSubArray(nums) << endl;
    return 0;
}}
'''
    return code


# ── Best Time to Buy and Sell Stock ───────────────────────────────────────────

def _wrap_best_time(code: str, input_data: str, language: str) -> str:
    prices = list(map(int, input_data.strip().split()))
    
    if language == "python":
        return code + f'''
_prices = {prices}
print(Solution().maxProfit(_prices))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[] prices = {{{", ".join(map(str, prices))}}};
        System.out.println(new Solution().maxProfit(prices));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const prices = {prices};
console.log(new Solution().maxProfit(prices));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<int> prices = {{{", ".join(map(str, prices))}}};
    cout << Solution().maxProfit(prices) << endl;
    return 0;
}}
'''
    return code


# ── Climbing Stairs ──────────────────────────────────────────────────────────

def _wrap_climbing_stairs(code: str, input_data: str, language: str) -> str:
    n = int(input_data.strip())
    
    if language == "python":
        return code + f'''
_n = {n}
print(Solution().climbStairs(_n))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int n = {n};
        System.out.println(new Solution().climbStairs(n));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const n = {n};
console.log(new Solution().climbStairs(n));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    int n = {n};
    cout << Solution().climbStairs(n) << endl;
    return 0;
}}
'''
    return code


# ── Binary Search ────────────────────────────────────────────────────────────

def _wrap_binary_search(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    
    if language == "python":
        return code + f'''
_nums = {nums}
_target = {target}
print(Solution().search(_nums, _target))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[] nums = {{{", ".join(map(str, nums))}}};
        int target = {target};
        System.out.println(new Solution().search(nums, target));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const nums = {nums};
const target = {target};
console.log(new Solution().search(nums, target));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<int> nums = {{{", ".join(map(str, nums))}}};
    int target = {target};
    cout << Solution().search(nums, target) << endl;
    return 0;
}}
'''
    return code


# ── Longest Common Prefix ────────────────────────────────────────────────────

def _wrap_longest_common_prefix(code: str, input_data: str, language: str) -> str:
    strs = input_data.strip().split()
    
    if language == "python":
        return code + f'''
_strs = {strs}
print(Solution().longestCommonPrefix(_strs))
'''
    elif language == "java":
        strs_java = ", ".join([f'"{s}"' for s in strs])
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        String[] strs = {{{strs_java}}};
        System.out.println(new Solution().longestCommonPrefix(strs));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const strs = {strs};
console.log(new Solution().longestCommonPrefix(strs));
'''
    elif language == "cpp":
        strs_cpp = ", ".join([f'"{s}"' for s in strs])
        return code + f'''

int main() {{
    vector<string> strs = {{{strs_cpp}}};
    cout << Solution().longestCommonPrefix(strs) << endl;
    return 0;
}}
'''
    return code


# ── Number of Islands ───────────────────────────────────────────────────────

def _wrap_number_of_islands(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    m, n = map(int, lines[0].split())
    grid = [lines[i+1].split() for i in range(m)]
    
    if language == "python":
        return code + f'''
_grid = {grid}
print(Solution().numIslands(_grid))
'''
    elif language == "java":
        grid_java = ", ".join([f'{{"{s}"}}' for row in grid for s in row])
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        char[][] grid = new char[][] {{
            {', '.join(["{" + ", ".join(f"'{c}'" for c in row) + "}" for row in grid])}
        }};
        System.out.println(new Solution().numIslands(grid));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const grid = {grid};
console.log(new Solution().numIslands(grid));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<vector<char>> grid = {{{{{", ".join(["{" + ", ".join(f"'{c}'" for c in row) + "}" for row in grid])}}}}};
    cout << Solution().numIslands(grid) << endl;
    return 0;
}}
'''
    return code


# ── Merge Intervals ────────────────────────────────────────────────────────

def _wrap_merge_intervals(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    count = int(lines[0])
    intervals = [list(map(int, lines[i+1].split())) for i in range(count)]
    
    if language == "python":
        return code + f'''
_intervals = {intervals}
_result = Solution().merge(_intervals)
for _iv in _result:
    print(" ".join(map(str, _iv)))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[][] intervals = new int[][] {{
            {', '.join(["{" + ", ".join(map(str, iv)) + "}" for iv in intervals])}
        }};
        int[][] result = new Solution().merge(intervals);
        for (int[] iv : result) {{
            System.out.println(iv[0] + " " + iv[1]);
        }}
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const intervals = {intervals};
const result = new Solution().merge(intervals);
for (let iv of result) {{
    console.log(iv[0] + " " + iv[1]);
}}
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<vector<int>> intervals = {{{{{", ".join(["{" + ", ".join(map(str, iv)) + "}" for iv in intervals])}}}}};
    vector<vector<int>> result = Solution().merge(intervals);
    for (auto& iv : result) {{
        cout << iv[0] << " " << iv[1] << endl;
    }}
    return 0;
}}
'''
    return code


# ── Coin Change ────────────────────────────────────────────────────────────

def _wrap_coin_change(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    coins = list(map(int, lines[0].split()))
    amount = int(lines[1])
    
    if language == "python":
        return code + f'''
_coins = {coins}
_amount = {amount}
print(Solution().coinChange(_coins, _amount))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        int[] coins = {{{", ".join(map(str, coins))}}};
        int amount = {amount};
        System.out.println(new Solution().coinChange(coins, amount));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const coins = {coins};
const amount = {amount};
console.log(new Solution().coinChange(coins, amount));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<int> coins = {{{", ".join(map(str, coins))}}};
    int amount = {amount};
    cout << Solution().coinChange(coins, amount) << endl;
    return 0;
}}
'''
    return code


# ── Word Search ────────────────────────────────────────────────────────────

def _wrap_word_search(code: str, input_data: str, language: str) -> str:
    lines = input_data.strip().split("\n")
    m, n = map(int, lines[0].split())
    board = [lines[i+1].split() for i in range(m)]
    word = lines[m+1]
    
    if language == "python":
        return code + f'''
_board = {board}
_word = "{word}"
print(Solution().exist(_board, _word))
'''
    elif language == "java":
        return code + f'''

public class Main {{
    public static void main(String[] args) {{
        char[][] board = new char[][] {{
            {', '.join(["{" + ", ".join(f"'{c}'" for c in row) + "}" for row in board])}
        }};
        String word = "{word}";
        System.out.println(new Solution().exist(board, word));
    }}
}}
'''
    elif language == "javascript":
        return code + f'''

const board = {board};
const word = "{word}";
console.log(new Solution().exist(board, word));
'''
    elif language == "cpp":
        return code + f'''

int main() {{
    vector<vector<char>> board = {{{{{", ".join(["{" + ", ".join(f"'{c}'" for c in row) + "}" for row in board])}}}}};
    string word = "{word}";
    cout << (Solution().exist(board, word) ? "true" : "false") << endl;
    return 0;
}}
'''
    return code