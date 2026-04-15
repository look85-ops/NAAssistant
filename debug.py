import os
import json

folder = r"C:\Users\marcenuk\Desktop\Новый проект"
result = {
    "folder": folder,
    "exists": os.path.exists(folder),
    "files": []
}

if os.path.exists(folder):
    for f in os.listdir(folder):
        result["files"].append(f)

with open(r"C:\Users\marcenuk\Desktop\Новый проект\debug_result.json", "w", encoding="utf-8") as out:
    json.dump(result, out, ensure_ascii=False, indent=2)
