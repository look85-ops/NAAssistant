import json, re

raw = open(r"C:\Users\marcenuk\.local\share\opencode\tool-output\tool_08f8c504d0013b4IQn0xL4AcBr", "r", encoding="utf-8").read()

# Extract JSON string from the tool output
m = re.search(r'"(\{.+\})"', raw, re.DOTALL)
data = json.loads(m.group(1))

out = {"MK_M": {"q": "methodolog+obuchenie", "n": data["count"], "total": data["total"], "v": data["results"]}}
with open(r"C:\Users\marcenuk\Desktop\Новый проект\scripts\browser-state\vacancies_m1.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"OK: {data['count']} вакансий, total={data['total']}")