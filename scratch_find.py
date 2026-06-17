import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app/dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

sidebar_start = -1
hero_ph = -1

for i, line in enumerate(lines):
    if line.startswith("with st.sidebar:"):
        sidebar_start = i
    if "hero_ph = st.empty()" in line and sidebar_start != -1 and hero_ph == -1:
        hero_ph = i

print(f"Sidebar starts at: {sidebar_start}")
print(f"hero_ph at: {hero_ph}")

if sidebar_start != -1 and hero_ph != -1:
    print("Found bounds successfully!")
