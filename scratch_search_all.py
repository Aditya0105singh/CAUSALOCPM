import os

search_text = "Built using"
search_text2 = "NetworkX"

for root, dirs, files in os.walk(r"d:\placement\project\Causal OCPM\causal_ocpm"):
    for file in files:
        if file.endswith(".py"):
            try:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    if search_text in content or search_text2 in content:
                        print(f"Found in {file}")
            except Exception as e:
                pass
