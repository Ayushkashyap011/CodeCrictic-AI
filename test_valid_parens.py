import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test Valid Parentheses (boolean output, no array formatting)
js_code = """
class Solution {
    isValid(s) {
        const stack = [];
        const map = {'(': ')', '{': '}', '[': ']'};
        for (const char of s) {
            if (char in map) {
                stack.push(char);
            } else {
                if (stack.length === 0 || map[stack.pop()] !== char) {
                    return false;
                }
            }
        }
        return stack.length === 0;
    }
}
"""

java_code = """
class Solution {
    public boolean isValid(String s) {
        java.util.Stack<Character> stack = new java.util.Stack<>();
        java.util.Map<Character, Character> map = new java.util.HashMap<>();
        map.put('(', ')');
        map.put('{', '}');
        map.put('[', ']');
        
        for (char c : s.toCharArray()) {
            if (map.containsKey(c)) {
                stack.push(c);
            } else {
                if (stack.isEmpty() || map.get(stack.pop()) != c) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }
}
"""

cpp_code = """
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char, char> map;
        map['('] = ')';
        map['{'] = '}';
        map['['] = ']';
        
        for (char c : s) {
            if (map.count(c) && !map[c]) {
                st.push(c);
            } else {
                if (st.empty() || map[st.top()] != c) {
                    return false;
                }
                st.pop();
            }
        }
        return st.empty();
    }
};
"""

# Get Valid Parentheses problem
problems = requests.get(f"{BASE_URL}/problems/").json()
valid_parens = next(p for p in problems if "valid parentheses" in p["title"].lower())
problem_id = valid_parens["id"]
print(f"Testing: {valid_parens['title']}\n")

for lang_code, lang_name in [(js_code, "JavaScript"), (java_code, "Java"), (cpp_code, "C++")]:
    response = requests.post(
        f"{BASE_URL}/execute/run",
        json={"code": lang_code, "language": lang_name.lower(), "problem_id": problem_id}
    )
    result = response.json()
    print(f"{lang_name}: Status={result.get('status')}, Passed={result.get('passed_count')}/{result.get('total_count')}")
