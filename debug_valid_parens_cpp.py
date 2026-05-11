import sys
sys.path.insert(0, 'backend')

from app.services.code_wrapper import _wrap_valid_parentheses

cpp_code = """#include <stack>
using namespace std;
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            if (c == ')' || c == '}' || c == ']') {
                if (st.empty()) return false;
                char open = st.top();
                st.pop();
                if ((c == ')' && open != '(') || (c == '}' && open != '{') || (c == ']' && open != '[')) {
                    return false;
                }
            } else {
                st.push(c);
            }
        }
        return st.empty();
    }
};"""

input_data = ")"

print("Generated C++ Code for Valid Parentheses:")
print("=" * 80)
wrapped = _wrap_valid_parentheses(cpp_code, input_data, "cpp")
print(wrapped)
print("=" * 80)
