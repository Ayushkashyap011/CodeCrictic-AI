import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Get all problems
problems = requests.get(f"{BASE_URL}/problems/").json()
problem_map = {p["title"].lower(): p for p in problems}

# Check specific problems
failing_problems = ["Maximum Subarray", "Merge Intervals", "Word Search", "Reverse Linked List"]

for prob_name in failing_problems:
    prob = problem_map.get(prob_name.lower())
    if not prob:
        print(f"Problem {prob_name} not found")
        continue
    
    print(f"\n{'='*60}")
    print(f"Problem: {prob_name}")
    print(f"{'='*60}")
    print(f"Examples:")
    for i, ex in enumerate(prob['examples']):
        print(f"  Test {i+1}:")
        print(f"    Input:    {repr(ex['input'])}")
        print(f"    Expected: {repr(ex['output'])}")
