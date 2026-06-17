dashboard_path = r"d:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py"
with open(dashboard_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# We need to remove from line 1005 to 1029 approximately.
# Find exact start and end for block 1:
block1_start = -1
block1_end = -1
for i, line in enumerate(lines):
    if line.startswith("# Pipeline Rendering (Redesigned Milestone Checklist)"):
        block1_start = i
    if line.startswith("_stage_ph.markdown(f\"<div>{_ph_html}</div>\", unsafe_allow_html=True)") and block1_start != -1 and block1_end == -1:
        block1_end = i

# Find exact start and end for block 2:
block2_start = -1
block2_end = -1
for i, line in enumerate(lines):
    if line.startswith("# ── Sidebar pipeline status"):
        block2_start = i
    if line.startswith("_stage_ph.markdown(f\"<div>{_ph_html}</div>\", unsafe_allow_html=True)") and i > block1_end:
        block2_end = i

new_block2 = """# ── Sidebar pipeline status ────────────────────────────────────────────────────
_stage_labels = [
    ("data", "Event Log Processed", "✅"), 
    ("graph", "Object Relationships Mapped", "🕸"),
    ("dag", "Causal Structure Recovered", "🌿"), 
    ("scm", "Structural Model Estimated", "⚙"),
    ("done", "Decision Intelligence Ready", "🧠")
]
_ph_html = f'<div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:12px 16px; border-radius:8px; margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.02);">'
for _sk, _sl, _emoji in _stage_labels:
    _status = stage_status.get(_sk, "ok" if _sk == "done" and stage_status.get("scm") == "ok" else stage_status.get(_sk, "na"))
    
    if _status == "ok":
        _icon = f'<span style="color:#10B981; font-weight:bold; margin-right:8px; font-size:1.1rem;">{_emoji}</span>'
        _color = "#0F172A"
    elif _status == "err":
        _icon = '<span style="color:#EF4444; font-weight:bold; margin-right:8px; font-size:1.1rem;">✗</span>'
        _color = "#EF4444"
    else:
        _icon = '<span style="color:#CBD5E1; font-weight:bold; margin-right:8px; font-size:1.1rem;">○</span>'
        _color = "#94A3B8"
        
    _ph_html += f'<div style="color:{_color}; font-size:0.85rem; font-weight:600; margin-bottom:10px; display:flex; align-items:center;">{_icon} {_sl}</div>'
_ph_html += '</div>'
_stage_ph.markdown(f"<div>{_ph_html}</div>", unsafe_allow_html=True)
"""

if block1_start != -1 and block1_end != -1 and block2_start != -1 and block2_end != -1:
    new_lines = lines[:block1_start] + lines[block1_end+1:block2_start] + [new_block2 + "\n"] + lines[block2_end+1:]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Fixed stage_status bug.")
else:
    print(f"Failed to find blocks. {block1_start}, {block1_end}, {block2_start}, {block2_end}")
