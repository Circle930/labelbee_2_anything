import json

with open('input/030206245180.jpg.json', 'r') as f:
    data = json.load(f)
    print(json.dumps(data, indent=2))