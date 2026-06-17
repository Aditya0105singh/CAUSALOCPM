new_func = """def insight_card(
    title: str,
    body: str,
    card_type: str = "info",
) -> None:
    \"\"\"Render a bordered insight card with a bolded title and descriptive body text.\"\"\"
    if card_type == "executive":
        st.markdown(
            f'<div style="background:#ECFDF5; border-left: 5px solid #10B981; padding: 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">'
            f'<p style="color:#10B981; font-weight:800; font-size:1.05rem; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.05em;">{title}</p>'
            f'<p style="color:#064E3B; font-size:0.95rem; margin:0; line-height:1.5;">{body}</p></div>',
            unsafe_allow_html=True,
        )
    elif card_type == "knowledge":
        st.markdown(
            f'<div style="background:#F8FAFC; border-left: 4px solid #14B8A6; padding: 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">'
            f'<p style="color:#0D9488; font-weight:800; font-size:1.05rem; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.05em;">{title}</p>'
            f'<p style="color:#334155; font-size:0.95rem; margin:0; line-height:1.5;">{body}</p></div>',
            unsafe_allow_html=True,
        )
    else:
        _colors = {
            "info":    PRIMARY,
            "success": SUCCESS,
            "warning": WARNING,
            "error":   ERROR,
        }
        color = _colors.get(card_type, PRIMARY)
        st.markdown(
            f'<div class="insight-box" style="border-left-color:{color};">'
            f'<p class="insight-title" style="color:{color};">{title}</p>'
            f'<p class="insight-body">{body}</p></div>',
            unsafe_allow_html=True,
        )
"""

dashboard_path = r"d:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py"
with open(dashboard_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def insight_card("):
        start_idx = i
    if "def metric_card(" in line and start_idx != -1 and end_idx == -1:
        end_idx = i

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [new_func + "\n"] + lines[end_idx:]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Replaced insight_card successfully. Start={start_idx}, End={end_idx}")
else:
    print("Could not find bounds.")
