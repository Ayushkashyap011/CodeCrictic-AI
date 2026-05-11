from app.services.code_wrapper import wrap_solution

cpp_code = """
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

input_data = "[2,7,11,15]\n9"

wrapped = wrap_solution(cpp_code, "Two Sum", input_data, "cpp")
print("="*60)
print("Generated C++ Code:")
print("="*60)
print(wrapped)
