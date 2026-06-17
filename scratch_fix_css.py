dashboard_path = r"d:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py"
with open(dashboard_path, "r", encoding="utf-8") as f:
    content = f.read()

# Repair the missing text from line 1718
missing_text = """                f'margin-bottom:8px; display:flex; align-items:center; gap:6px;">'
                f'💡 Key Insight</div>'
                f'<div style="font-size:0.85rem;color:#1E293B;line-height:1.6;">'
                f'Traditional process mining tracks only cases. '
                f'By tracking <b style="color:#10B981;">{len(_type_n)} object types</b> simultaneously, '
                f'CausalOCPM can discover hidden causal bottlenecks across the entire network.'
                f'</div></div>'"""

broken_text = """                f'margin-bottom:8px; display:flex; align-items:center; gap:6px;">'
                f'💡 Key Insight</div>'
                f'<div style="font-size:0.85rem;color:#1E293B;line-height:1.6;">'
                f'CausalOCPM can discover hidden causal bottlenecks across the entire network.'
                f'</div></div>'"""

if broken_text in content:
    content = content.replace(broken_text, missing_text)

# Update insight_card(..., "info") -> "knowledge" for OCEL Graph Coverage
ocel_card_old = """        insight_card(
            "OCEL Graph Coverage",
            f"{summary.get('total_nodes', 0):,} object instances across "
            f"{len(_type_n) if G and G.number_of_nodes() > 0 else 5} types — "
            f"{summary.get('total_edges', 0):,} co-occurrence edges "
            f"(avg degree {summary.get('avg_degree', 0):.2f}). "
            "CausalOCPM tracks every object type simultaneously, not just cases.",
            "info",
        )"""

ocel_card_new = """        insight_card(
            "OCEL Graph Coverage",
            f"{summary.get('total_nodes', 0):,} object instances across "
            f"{len(_type_n) if G and G.number_of_nodes() > 0 else 5} types — "
            f"{summary.get('total_edges', 0):,} co-occurrence edges "
            f"(avg degree {summary.get('avg_degree', 0):.2f}). "
            "CausalOCPM tracks every object type simultaneously, not just cases.",
            "knowledge",
        )"""

if ocel_card_old in content:
    content = content.replace(ocel_card_old, ocel_card_new)

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixes applied successfully.")
