# -*- coding: utf-8 -*-
"""
Patch dashboard.py:
1. Add dark/light theme toggle (session_state-driven, conditional BRAND_COLORS / PLOTLY_LAYOUT)
2. Add sidebar "Appearance" toggle widget
3. Fix Sankey "undefined" label bug (Tab4 causal pathway — newline in node label)
4. Fix Tab2 DAG canvas iframe height (510 -> 460, matching the 440px wrap) + html overflow
5. Fix Tab5 waterfall chart margins/height + spacer before Attribution Summary card
"""
PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

replacements = []

# 1. Theme state — inserted right after CSS load, before BRAND_COLORS
replacements.append((
'''# ── LOAD EXTERNAL CSS (Sven-Bo pattern: separate file, not inline) ─────────────
_css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(_css_path, encoding="utf-8") as _f:
    st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)
''',
'''# ── LOAD EXTERNAL CSS (Sven-Bo pattern: separate file, not inline) ─────────────
_css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(_css_path, encoding="utf-8") as _f:
    st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)


# ── THEME STATE (decided before BRAND_COLORS so every color below adapts) ─────
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
IS_LIGHT: bool = st.session_state["theme"] == "light"

if IS_LIGHT:
    st.markdown("""<style>
.stApp, .main .block-container { background-color: #FFFFFF !important; }
html, body, [class*="css"] { color: #1E293B !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8F9FB 0%, #FFFFFF 100%) !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] hr, hr { border-color: #E2E8F0 !important; }
::-webkit-scrollbar-track { background: #FFFFFF !important; }
::-webkit-scrollbar-thumb { background: #CBD5E1 !important; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8 !important; }
[data-testid="stTabs"] > div:first-child {
    background: #F1F2F6 !important; scrollbar-color: #CBD5E1 #FFFFFF !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] { color: #64748B !important; }
[data-testid="stTabs"] [data-baseweb="tab"]:hover { background: rgba(108,99,255,0.10) !important; color: #1E293B !important; }
[data-testid="stTabs"] [aria-selected="true"] { background: #6C63FF !important; color: #ffffff !important; }
[data-testid="stMetric"] { background: #F8F9FB !important; border: 1px solid #E2E8F0 !important; border-left: 3px solid #6C63FF !important; }
[data-testid="stMetricLabel"] { color: #64748B !important; }
[data-testid="stMetricValue"] { color: #1E293B !important; }
.content-card, .insight-box { background: #F8F9FB !important; border-color: #E2E8F0 !important; }
.hero-section { background: linear-gradient(135deg, #FFFFFF 0%, #F1F2F6 100%) !important; border-color: #E2E8F0 !important; }
.hero-sub { color: #1E293B !important; }
ul[data-baseweb="menu"], [data-baseweb="list"] { background: #FFFFFF !important; border: 1px solid #E2E8F0 !important; }
li[role="option"] { color: #1E293B !important; }
li[role="option"]:hover { background: rgba(108,99,255,0.08) !important; color: #1E293B !important; }
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div:first-child {
    background: #FFFFFF !important; border: 1px solid #E2E8F0 !important; color: #1E293B !important;
}
[data-testid="stNumberInput"] input { background: #FFFFFF !important; border: 1px solid #E2E8F0 !important; color: #1E293B !important; }
[data-testid="stExpander"] { background: #F8F9FB !important; border: 1px solid #E2E8F0 !important; }
[data-testid="stExpander"] summary { color: #334155 !important; }
[data-testid="stExpander"] summary:hover { color: #1E293B !important; }
[data-testid="stRadio"] label { color: #334155 !important; }
[data-testid="stDataFrame"] { border: 1px solid #E2E8F0 !important; }
table.ctbl th { background: #F1F2F6 !important; color: #64748B !important; border-bottom: 1px solid #E2E8F0 !important; }
table.ctbl td { color: #334155 !important; border-top: 1px solid #F1F2F6 !important; }
.ctbl tr:hover td { background: #F8F9FB !important; }
.sb-label { color: #64748B !important; }
.version-pill { background: #F1F2F6 !important; border-color: #E2E8F0 !important; color: #64748B !important; }
</style>""", unsafe_allow_html=True)
''',
))

# 2. Conditional BRAND_COLORS
replacements.append((
'''BRAND_COLORS: Dict[str, str] = {
    "primary":   "#6C63FF",   # violet — main accent (DoWhy-inspired)
    "secondary": "#A78BFA",   # light purple
    "success":   "#10B981",   # emerald — ok / causal estimate
    "warning":   "#F59E0B",   # amber — planted truth / warning
    "error":     "#EF4444",   # red — confounding / danger
    "info":      "#3B82F6",   # blue — informational
    "orange":    "#F97316",   # orange
    "bg":        "#0E1117",   # page background
    "card":      "#161B27",   # card / sidebar background
    "border":    "#2D3748",   # borders
    "muted":     "#94A3B8",   # muted text
    "text":      "#E2E8F0",   # main text
    "subtle":    "#64748B",   # subtle / axis labels
}''',
'''BRAND_COLORS: Dict[str, str] = ({
    "primary":   "#6C63FF",
    "secondary": "#7C3AED",
    "success":   "#059669",
    "warning":   "#D97706",
    "error":     "#DC2626",
    "info":      "#2563EB",
    "orange":    "#EA580C",
    "bg":        "#FFFFFF",
    "card":      "#F8F9FB",
    "border":    "#E2E8F0",
    "muted":     "#64748B",
    "text":      "#1E293B",
    "subtle":    "#94A3B8",
} if IS_LIGHT else {
    "primary":   "#6C63FF",   # violet — main accent (DoWhy-inspired)
    "secondary": "#A78BFA",   # light purple
    "success":   "#10B981",   # emerald — ok / causal estimate
    "warning":   "#F59E0B",   # amber — planted truth / warning
    "error":     "#EF4444",   # red — confounding / danger
    "info":      "#3B82F6",   # blue — informational
    "orange":    "#F97316",   # orange
    "bg":        "#0E1117",   # page background
    "card":      "#161B27",   # card / sidebar background
    "border":    "#2D3748",   # borders
    "muted":     "#94A3B8",   # muted text
    "text":      "#E2E8F0",   # main text
    "subtle":    "#64748B",   # subtle / axis labels
})''',
))

# 3. Theme-aware Plotly template
replacements.append((
'''PLOTLY_LAYOUT: Dict[str, Any] = dict(
    template="plotly_dark",''',
'''PLOTLY_LAYOUT: Dict[str, Any] = dict(
    template="plotly_white" if IS_LIGHT else "plotly_dark",''',
))

# 4. Sidebar — Appearance toggle, right after the branding block
replacements.append((
'''        f'<span class="version-pill" style="float:right;margin-top:2px;">v1.0</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── MIDDLE: Domain + Parameters ───────────────────────────────────────────''',
'''        f'<span class="version-pill" style="float:right;margin-top:2px;">v1.0</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── APPEARANCE ─────────────────────────────────────────────────────────────
    st.markdown('<p class="sb-label">🎨 &nbsp;Appearance</p>', unsafe_allow_html=True)
    _light_toggle = st.toggle("Light mode", value=IS_LIGHT, key="theme_toggle_widget")
    if _light_toggle != IS_LIGHT:
        st.session_state["theme"] = "light" if _light_toggle else "dark"
        st.rerun()

    # ── MIDDLE: Domain + Parameters ───────────────────────────────────────────''',
))

# 5. Sankey "undefined" bug — newline inside node label breaks Plotly's Sankey text layout
replacements.append((
'                    f"Outcome\\n({outcome_label})",',
'                    f"Outcome ({outcome_label})",',
))

# 6. DAG canvas — tighten iframe height to match the 440px wrap, clip html too
replacements.append((
"body{{background:#0A0E17;font-family:-apple-system,'Inter',sans-serif;overflow:hidden;}}",
"html,body{{background:#0A0E17;font-family:-apple-system,'Inter',sans-serif;overflow:hidden;max-width:100%;}}",
))
replacements.append((
'</script></body></html>""", height=510)',
'</script></body></html>""", height=460)',
))

# 7. Tab5 waterfall — more breathing room for outside text labels + spacer before summary card
replacements.append((
'''        _wfl = dict(**PLOTLY_LAYOUT)
        _wfl.update(dict(
            title=f"Outcome Attribution — {selected_case}",
            yaxis={**PLOTLY_LAYOUT.get("yaxis", {}), "title": outcome_label},
            xaxis={**PLOTLY_LAYOUT.get("xaxis", {}), "title": "Feature"},
            height=430,
        ))''',
'''        _wfl = dict(**PLOTLY_LAYOUT)
        _wfl.update(dict(
            title=f"Outcome Attribution — {selected_case}",
            yaxis={**PLOTLY_LAYOUT.get("yaxis", {}), "title": outcome_label},
            xaxis={**PLOTLY_LAYOUT.get("xaxis", {}), "title": "Feature"},
            height=460,
            margin=dict(l=20, r=20, t=60, b=70),
        ))''',
))
replacements.append((
'''        insight_card(
            "Attribution Summary",
            f"Baseline: {baseline:.2f} days. Controllable: {attrib_summary['actionable_total']:+.2f}; "
            f"structural: {attrib_summary['structural_total']:+.2f}. "
            f"Predicted {predicted:.2f} vs actual {actual:.2f} days.",
            "info",
        )''',
'''        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        insight_card(
            "Attribution Summary",
            f"Baseline: {baseline:.2f} days. Controllable: {attrib_summary['actionable_total']:+.2f}; "
            f"structural: {attrib_summary['structural_total']:+.2f}. "
            f"Predicted {predicted:.2f} vs actual {actual:.2f} days.",
            "info",
        )''',
))

changed = 0
for old, new in replacements:
    count = src.count(old)
    if count == 1:
        src = src.replace(old, new, 1)
        changed += 1
        print(f"  OK: {old[:70].strip()!r}")
    elif count == 0:
        print(f"  MISS (0 occurrences): {old[:70].strip()!r}")
    else:
        print(f"  AMBIGUOUS ({count} occurrences, skipped): {old[:70].strip()!r}")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\nDone — {changed}/{len(replacements)} replacements applied.")
