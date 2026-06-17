dashboard_path = r"d:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py"
with open(dashboard_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

end_idx = -1
for i, line in enumerate(lines):
    if "FOOTER" in line and "st.divider()" in lines[i+1]:
        end_idx = i
        break

if end_idx != -1:
    lines = lines[:end_idx]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Removed footer.")
else:
    print("Footer not found.")
