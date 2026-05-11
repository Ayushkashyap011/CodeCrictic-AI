import json

data = json.load(open(r'c:\Users\kashy\OneDrive\Desktop\code\CodeCrictic-AI\backend\data\problems.json'))
for i, p in enumerate(data, 1):
    print(f"{i}. {p['title']}")
