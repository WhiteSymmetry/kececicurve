import json

data = {
    "name": "kececicurve",
    "version": "0.1.7",
    "generated": True
}

with open("project.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
