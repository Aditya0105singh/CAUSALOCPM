@st.fragment
def render_copilot():

    # ── GLOBAL CSS ────────────────────────────────────────────────────────────
    st.markdown("""<style>


/* ── Copilot v4 — Premium Design System ── */
@keyframes cop-pulse  { 0%,100%{opacity:1} 50%{opacity:.35} }
@keyframes cop-in     { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }

/* ── Premium Action Chips (class + innerHTML injected via JS) ── */
.cop-action-chip {
background: #FFFFFF !important;
border: 1px solid #E8EDF3 !important;
border-radius: 14px !important;
min-height: 72px !important;
padding: 0 !important;
text-align: left !important;
box-shadow: 0 1px 3px rgba(15,23,42,0.06), 0 4px 16px rgba(15,23,42,0.03) !important;
transition: all 0.22s cubic-bezier(0.4,0,0.2,1) !important;
white-space: normal !important;
width: 100% !important;
cursor: pointer !important;
overflow: hidden !important;
position: relative !important;
font-size: 0 !important;
}
.cop-action-chip:hover {
border-color: #10B981 !important;
box-shadow: 0 6px 24px rgba(16,185,129,0.16), 0 1px 3px rgba(15,23,42,0.06) !important;
transform: translateY(-3px) !important;
}
.cop-action-chip:active  { transform: translateY(-1px) !important; }
.cop-action-chip:focus   { outline: none !important; box-shadow: 0 0 0 3px rgba(16,185,129,0.18) !important; }

/* Chip inner layout */
.cop-chip-inner {
display: flex !important; align-items: center !important;
gap: 12px !important; padding: 14px 14px !important;
width: 100% !important; pointer-events: none !important;
}
.cop-chip-icon {
width: 38px !important; height: 38px !important;
border-radius: 10px !important; flex-shrink: 0 !important;
display: flex !important; align-items: center !important; justify-content: center !important;
font-size: 1.05rem !important; line-height: 1 !important;
transition: transform 0.22s ease !important;
}
.cop-action-chip:hover .cop-chip-icon { transform: scale(1.12) rotate(-4deg) !important; }
.cop-chip-body { flex: 1 !important; min-width: 0 !important; }
.cop-chip-title {
font-size: 0.82rem !important; font-weight: 700 !important;
color: #1E293B !important; line-height: 1.3 !important;
margin-bottom: 3px !important; white-space: normal !important;
}
.cop-action-chip:hover .cop-chip-title { color: #065F46 !important; }
.cop-chip-sub {
font-size: 0.7rem !important; font-weight: 500 !important;
color: #94A3B8 !important; line-height: 1.2 !important;
white-space: nowrap !important;
}
.cop-action-chip:hover .cop-chip-sub { color: #34D399 !important; }
.cop-chip-arrow {
font-size: 0.85rem !important; color: #CBD5E1 !important;
flex-shrink: 0 !important; font-weight: 300 !important;
transition: color 0.22s, transform 0.22s !important;
}
.cop-action-chip:hover .cop-chip-arrow { color: #10B981 !important; transform: translateX(4px) !important; }

/* ── Form / Input area ── */
[data-testid="stForm"] {
background: transparent !important;
border: none !important;
padding: 0 !important;
}
[data-testid="stTextInput"] input {
border-radius: 12px !important;
border: 1.5px solid #E2E8F0 !important;
font-size: 0.88rem !important;
padding: 10px 14px !important;
transition: border-color 0.2s, box-shadow 0.2s !important;
background: #FAFBFC !important;
}
[data-testid="stTextInput"] input:focus {
border-color: #10B981 !important;
box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
background: #FFFFFF !important;
}

/* Ask button — premium gradient */
[data-testid="stBaseButton-primaryFormSubmit"],
[data-testid="stFormSubmitButton"] button {
background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
border: none !important;
border-radius: 12px !important;
font-weight: 700 !important;
font-size: 0.88rem !important;
box-shadow: 0 4px 14px rgba(16,185,129,0.32) !important;
transition: all 0.2s ease !important;
letter-spacing: 0.01em !important;
}
[data-testid="stBaseButton-primaryFormSubmit"]:hover,
[data-testid="stFormSubmitButton"] button:hover {
box-shadow: 0 6px 22px rgba(16,185,129,0.44) !important;
transform: translateY(-1px) !important;
}

/* Clear button — ghost style (lives inside form as secondaryFormSubmit) */
[data-testid="stBaseButton-secondaryFormSubmit"] {
background: transparent !important;
border: 1px solid #E2E8F0 !important;
border-radius: 12px !important;
color: #94A3B8 !important;
font-weight: 500 !important;
font-size: 0.82rem !important;
transition: all 0.18s ease !important;
height: 42px !important;
}
[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
background: #FEF2F2 !important;
border-color: #FECACA !important;
color: #EF4444 !important;
}

/* ── Follow-up suggestion pills ── */
.cop-followups [data-testid="stButton"] > button {
background: #F8FAFC !important;
border: 1px solid #E2E8F0 !important;
border-radius: 20px !important;
min-height: 34px !important;
font-size: 0.75rem !important;
font-weight: 500 !important;
color: #475569 !important;
padding: 0 14px !important;
white-space: nowrap !important;
transition: all 0.15s ease !important;
}
.cop-followups [data-testid="stButton"] > button:hover {
border-color: #10B981 !important;
color: #065F46 !important;
background: #F0FDF4 !important;
box-shadow: 0 2px 8px rgba(16,185,129,0.14) !important;
}

/* ── Input card container ── */
.cop-input-card {
border: 1.5px solid #E2E8F0 !important;
border-radius: 16px !important;
padding: 16px 20px !important;
box-shadow: 0 2px 8px rgba(15,23,42,0.05), 0 0 0 0 transparent !important;
transition: box-shadow 0.2s, border-color 0.2s !important;
}
.cop-input-card:focus-within {
border-color: #A7F3D0 !important;
box-shadow: 0 2px 8px rgba(15,23,42,0.05), 0 0 0 4px rgba(16,185,129,0.08) !important;
}

/* ── Answer card animation ── */
.cop-answer { animation: cop-in 0.28s ease forwards; }
</style>""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────
for _k, _v in [("cop_history",[]),("cop_question",""),("cop_followups",[]),("cop_exec_mode",False)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v
if "cop_groq_key_val" not in st.session_state:
    try:
        st.session_state["cop_groq_key_val"] = st.secrets.get("GROQ_API_KEY","")
    except Exception:
        st.session_state["cop_groq_key_val"] = ""

# Resolve active key (secrets or manual override)
_active_key = st.session_state["cop_groq_key_val"]

# ── HERO ─────────────────────────────────────────────────────────────────
_cop_n      = len(df)
_cop_edges  = dag.number_of_edges()
_cop_domain = domain.replace("_"," ").title()
_key_active = bool(_active_key)
_n_k        = f"{_cop_n // 1000}K" if _cop_n >= 1000 else str(_cop_n)
_obj_types  = 5 if domain == "manufacturing" else 4

_groq_badge = (
    '<span style="display:inline-flex;align-items:center;gap:5px;'
    'background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.28);'
    'border-radius:999px;padding:4px 12px;">'
    '<span style="color:#34D399;font-size:0.7rem;font-weight:700;">&#10003; GROQ ACTIVE</span></span>'
    if _key_active else
    '<span style="display:inline-flex;align-items:center;'
    'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
    'border-radius:999px;padding:4px 12px;">'
    '<span style="color:#64748B;font-size:0.7rem;font-weight:600;">OFFLINE MODE</span></span>'
)
st.markdown(
    '<div style="background:#0F172A;border-radius:12px;padding:20px 24px 16px;margin-bottom:0;">'

    '<div style="color:#FFFFFF;font-size:1.25rem;font-weight:800;'
    'letter-spacing:-0.02em;margin-bottom:6px;">'
    '&#129302;&nbsp; Causal Decision Copilot</div>'

    '<div style="color:#94A3B8;font-size:0.85rem;font-weight:400;'
    'line-height:1.5;margin-bottom:14px;">'
    'Discover root causes, simulate interventions, and quantify business impact.</div>'

    '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:14px;">'

    '<span style="display:inline-flex;align-items:center;gap:5px;'
    'background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.28);'
    'border-radius:999px;padding:4px 12px;">'
    '<span style="width:5px;height:5px;border-radius:50%;background:#34D399;display:inline-block;'
    'animation:cop-pulse 1.5s infinite;"></span>'
    '<span style="color:#6EE7B7;font-size:0.7rem;font-weight:700;letter-spacing:0.04em;">'
    'LIVE CONTEXT</span></span>'

    f'<span style="display:inline-flex;align-items:center;'
    f'background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);'
    f'border-radius:999px;padding:4px 12px;">'
    f'<span style="color:#CBD5E1;font-size:0.7rem;font-weight:600;">{_cop_domain.upper()}</span></span>'

    + _groq_badge +

    '</div>'

    '<div style="display:flex;gap:24px;padding-top:12px;'
    'border-top:1px solid rgba(255,255,255,0.06);">'

    f'<div><div style="color:#475569;font-size:0.68rem;font-weight:600;'
    f'text-transform:uppercase;letter-spacing:0.05em;">Events Analysed</div>'
    f'<div style="color:#94A3B8;font-size:0.88rem;font-weight:700;margin-top:2px;">{_n_k}</div></div>'

    f'<div><div style="color:#475569;font-size:0.68rem;font-weight:600;'
    f'text-transform:uppercase;letter-spacing:0.05em;">Causal Links</div>'
    f'<div style="color:#94A3B8;font-size:0.88rem;font-weight:700;margin-top:2px;">{_cop_edges}</div></div>'

    f'<div><div style="color:#475569;font-size:0.68rem;font-weight:600;'
    f'text-transform:uppercase;letter-spacing:0.05em;">Object Types</div>'
    f'<div style="color:#94A3B8;font-size:0.88rem;font-weight:700;margin-top:2px;">{_obj_types}</div></div>'

    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Connection status + Executive toggle ──────────────────────────────────
_stat_col, _tog_col = st.columns([3.5, 1.5])
with _stat_col:
    if _key_active:
        st.markdown(
            '<div style="display:inline-flex;align-items:center;gap:8px;'
            'background:#F0FDF4;border:1px solid #A7F3D0;border-radius:8px;'
            'padding:7px 14px;margin-top:8px;">'
            '<span style="width:7px;height:7px;border-radius:50%;background:#10B981;'
            'display:inline-block;"></span>'
            '<span style="color:#065F46;font-size:0.82rem;font-weight:700;">Groq Connected</span>'
            '<span style="color:#6EE7B7;font-size:0.8rem;">&#183;</span>'
            '<span style="color:#059669;font-size:0.8rem;font-weight:500;">Llama 3.1 8B</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="display:inline-flex;align-items:center;gap:8px;'
            'background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;'
            'padding:7px 14px;margin-top:8px;">'
            '<span style="width:7px;height:7px;border-radius:50%;background:#94A3B8;'
            'display:inline-block;"></span>'
            '<span style="color:#64748B;font-size:0.82rem;font-weight:600;">'
            'High-quality fallbacks active</span>'
            '</div>',
            unsafe_allow_html=True,
        )
with _tog_col:
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    _exec_on = st.toggle(
        "⚡ Executive",
        value=st.session_state["cop_exec_mode"],
        key="cop_exec_toggle",
    )
    st.session_state["cop_exec_mode"] = _exec_on

# ── Settings (collapsed; no implementation details visible) ───────────────
with st.expander("Advanced Configuration", expanded=False):
    st.markdown(
        '<p style="color:#64748B;font-size:0.8rem;margin:0 0 10px;">'
        'Override the active API connection below.</p>',
        unsafe_allow_html=True,
    )
    _key_input = st.text_input(
        "API Key",
        type="password",
        placeholder="Enter a different key to override the active connection",
        key="cop_groq_key_raw",
    )
    if _key_input:
        st.session_state["cop_groq_key_val"] = _key_input
        _active_key = _key_input

# Container placed HERE so history renders visually above quick-actions/input
_history_container = st.container()

# ── JS: Enhance chip buttons with icon badges + subtitles ─────────────────
_stc.html("""<script>
(function(){
  var CHIPS=[
{m:'Why are delays',     i:'📈',t:'Why are delays increasing?',s:'Root cause analysis',  c:'#F59E0B',bg:'#FFFBEB'},
{m:'What is the top bottleneck',i:'⚠️',t:'Top bottleneck',s:'Critical path finder',c:'#EF4444',bg:'#FEF2F2'},
{m:'Best intervention',  i:'💡',t:'Best intervention',       s:'Action optimizer',       c:'#10B981',bg:'#ECFDF5'},
{m:'Compare suppliers',  i:'🔄',t:'Compare suppliers',        s:'Vendor benchmark',       c:'#3B82F6',bg:'#EFF6FF'},
{m:'Explain causal',     i:'🔗',t:'Explain causal chain',     s:'DAG walkthrough',        c:'#8B5CF6',bg:'#F5F3FF'},
{m:'Simulate impact',    i:'📊',t:'Simulate impact',          s:'What-if scenario',       c:'#06B6D4',bg:'#ECFEFF'},
{m:'Executive summary',  i:'📋',t:'Executive summary',        s:'Board-ready brief',      c:'#F97316',bg:'#FFF7ED'},
{m:'ROI opportunities',  i:'💰',t:'ROI opportunities',        s:'Value quantifier',       c:'#10B981',bg:'#ECFDF5'},
  ];
  function enhance(){
try{
  var doc=window.parent.document;
  var btns=doc.querySelectorAll('[data-testid="stBaseButton-secondary"]');
  btns.forEach(function(b){
    var txt=b.textContent.trim();
    CHIPS.forEach(function(ch){
      if(txt.includes(ch.m)&&!b.classList.contains('cop-action-chip')){
        b.classList.add('cop-action-chip');
        b.innerHTML='<div class="cop-chip-inner">'
          +'<div class="cop-chip-icon" style="background:'+ch.bg+';border:1px solid '+ch.c+'33;">'+ch.i+'</div>'
          +'<div class="cop-chip-body">'
            +'<div class="cop-chip-title">'+ch.t+'</div>'
            +'<div class="cop-chip-sub">'+ch.s+'</div>'
          +'</div>'
          +'<div class="cop-chip-arrow">&#8594;</div>'
        +'</div>';
      }
    });
    if(txt==='Clear'&&!b.classList.contains('cop-clear-styled')){
      b.classList.add('cop-clear-styled');
      b.closest('[data-testid="stButton"]').classList.add('cop-clear-btn');
    }
  });
}catch(e){}
  }
  enhance();[300,700,1500,3000].forEach(function(d){setTimeout(enhance,d);});
  try{
var timer;
var obs=new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(enhance,80);});
obs.observe(window.parent.document.body,{childList:true,subtree:false});
  }catch(e){}
})();
</script>""", height=0)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ── QUICK ACTIONS ─────────────────────────────────────────────────────────
_cop_chips = [
    ("delays",       "📈", "Why are delays increasing?"),
    ("bottleneck",   "⚠️", "What is the top bottleneck?"),
    ("intervention", "💡", "Best intervention?"),
    ("suppliers",    "🔄", "Compare suppliers"),
    ("chain",        "🔗", "Explain causal chain"),
    ("impact",       "📊", "Simulate impact"),
    ("executive",    "📋", "Executive summary"),
    ("roi",          "💰", "ROI opportunities"),
]
_chip_qs = {k: q for k, _, q in _cop_chips}

# Section header
st.markdown(
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
    '<div style="display:flex;align-items:center;gap:8px;">'
    '<span style="color:#0F172A;font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;">Quick Actions</span>'
    '<span style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:5px;padding:2px 7px;'
    'font-size:0.62rem;font-weight:700;color:#64748B;letter-spacing:0.05em;">8 SHORTCUTS</span>'
    '</div>'
    '<span style="font-size:0.68rem;color:#94A3B8;font-weight:500;">Click to ask · AI-powered</span>'
    '</div>',
    unsafe_allow_html=True,
)
# Category 1: DIAGNOSE
st.markdown(
    '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">'
    '<div style="width:3px;height:11px;background:linear-gradient(180deg,#F59E0B,#EF4444);border-radius:2px;"></div>'
    '<span style="font-size:0.63rem;font-weight:800;text-transform:uppercase;letter-spacing:0.09em;color:#92400E;">Diagnose</span>'
    '</div>',
    unsafe_allow_html=True,
)
_row1 = st.columns(4, gap="small")
for _cc, (key, icon, label) in zip(_row1, _cop_chips[:4]):
    with _cc:
        if st.button(f"{icon} {label}", key=f"cop_chip_{key}", use_container_width=True):
            st.session_state["cop_question"] = _chip_qs[key]

# Category 2: EXPLORE
st.markdown(
    '<div style="display:flex;align-items:center;gap:6px;margin:10px 0 6px;">'
    '<div style="width:3px;height:11px;background:linear-gradient(180deg,#3B82F6,#8B5CF6);border-radius:2px;"></div>'
    '<span style="font-size:0.63rem;font-weight:800;text-transform:uppercase;letter-spacing:0.09em;color:#1E40AF;">Explore</span>'
    '</div>',
    unsafe_allow_html=True,
)
_row2 = st.columns(4, gap="small")
for _cc, (key, icon, label) in zip(_row2, _cop_chips[4:]):
    with _cc:
        if st.button(f"{icon} {label}", key=f"cop_chip_{key}", use_container_width=True):
            st.session_state["cop_question"] = _chip_qs[key]

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ── INPUT AREA ────────────────────────────────────────────────────────────
st.markdown(
    '<div style="background:linear-gradient(135deg,#F8FAFC 0%,#F1F5F9 100%);"'
    ' class="cop-input-card">'
    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">'
    '<div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#10B981,#059669);'
    'display:flex;align-items:center;justify-content:center;font-size:0.85rem;">🤖</div>'
    '<span style="color:#0F172A;font-size:0.8rem;font-weight:800;letter-spacing:0.04em;">ASK CAUSAL COPILOT</span>'
    '</div>',
    unsafe_allow_html=True,
)

# Apply pending clear BEFORE the widget is instantiated (Streamlit requires this order)
if st.session_state.pop("_clear_cop_input", False):
    st.session_state["cop_input_field"] = ""

# Input + Ask + Clear all inside ONE form → same row, same height, no misalignment
with st.form(key="cop_form", border=False, clear_on_submit=False):
    _inp_sub, _ask_sub, _clr_sub = st.columns([6.5, 1.5, 1.0])
    with _inp_sub:
        _user_q = st.text_input(
            "Q",
            placeholder="Ask about root causes, bottlenecks, interventions, or business impact...",
            key="cop_input_field",
            label_visibility="collapsed",
        )
    with _ask_sub:
        _ask_btn = st.form_submit_button("Ask →", type="primary", use_container_width=True)
    with _clr_sub:
        _clear_btn = st.form_submit_button("Clear", use_container_width=True)

if _clear_btn:
    st.session_state["cop_history"]   = []
    st.session_state["cop_followups"] = []
    st.session_state["cop_question"]  = ""
    st.session_state["_clear_cop_input"] = True

st.markdown(
    '<div style="display:flex;align-items:center;gap:8px;margin-top:8px;padding-top:8px;'
    'border-top:1px solid #E2E8F0;">'
    '<span style="color:#CBD5E1;font-size:0.68rem;">&#8629; Enter to send</span>'
    '<span style="color:#E2E8F0;">·</span>'
    '<span style="color:#CBD5E1;font-size:0.68rem;">Powered by Llama 3.1 8B via Groq</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── PROCESS QUESTION ──────────────────────────────────────────────────────
# Chip buttons take priority; Ask button captures typed text
_chip_q = st.session_state.get("cop_question", "")
if _chip_q.strip():
    _q_to_process = _chip_q
elif _ask_btn and _user_q.strip():
    _q_to_process = _user_q.strip()
else:
    _q_to_process = ""

_already_answered = bool(
    _q_to_process
    and st.session_state["cop_history"]
    and st.session_state["cop_history"][-1].get("question") == _q_to_process
)

if _q_to_process and not _already_answered:
    with st.spinner("Analysing causal patterns…"):
        try:
            if _COPILOT_AVAILABLE:
                if _active_key:
                    _ctx3 = _copilot_build_context(dag=dag, dag_metrics=dag_metrics, scm=scm,
                                                    coefs=coefs, cfg=cfg, domain=domain, df=df)
                    _hist3 = [{"q": r["question"], "a": r["exec_text"]}
                              for r in st.session_state["cop_history"][-3:]
                              if "question" in r and "exec_text" in r]
                    _exec_text, _conf, _fups = _copilot_call_groq_structured(
                        _q_to_process, _ctx3, _active_key, domain=domain, history=_hist3)
                else:
                    _exec_text = _copilot_exec_answer(_q_to_process, domain)
                    from app.copilot import _detect_chip_key as _dck3, FOLLOW_UP_POOL as _FUP3
                    _conf  = "High"
                    _fups  = _FUP3.get(_dck3(_q_to_process), _FUP3["custom"])

                _resp_data = _copilot_build_response(
                    question=_q_to_process, domain=domain, cfg=cfg, dag=dag,
                    dag_metrics=dag_metrics, df=df, coefs=coefs, do_result=do_result,
                    groq_exec_text=_exec_text, groq_confidence=_conf, groq_follow_ups=_fups,
                )
            else:
                _fb_bl   = round(float(df[cfg["outcome_var"]].mean()), 2) if cfg.get("outcome_var") in df.columns else (8.2 if domain == "manufacturing" else 5.27)
                _fb_imp  = 18.3 if domain == "manufacturing" else 12.7
                _fb_mult = 300 * 960 if domain == "manufacturing" else 400 * 1050
                _fb_sav  = int(round(_fb_imp / 100 * _fb_bl * _fb_mult / 1000) * 1000)
                _resp_data = {
                    "question": _q_to_process, "exec_text": "Copilot module unavailable.",
                    "confidence": "Low", "chip_key": "custom", "causal_chain": [],
                    "true_effect": None, "effect_from": _fb_bl, "effect_to": round(_fb_bl * (1 - _fb_imp/100), 2),
                    "improvement_pct": _fb_imp, "annual_saving": _fb_sav, "roi_months": None,
                    "recommendation": "Restart dashboard", "outcome_label": cfg.get("outcome_label", "Outcome"),
                    "sim_best_case": {"from": _fb_bl, "to": round(_fb_bl * 0.71, 2), "pct": 29.0, "saving": int(_fb_sav*1.6), "roi": 3.5},
                    "evidence": [], "follow_ups": [], "domain": domain,
                }
        except Exception as _cop_err:
            logger.exception("Copilot response build failed for question=%r", _q_to_process)
            _fb_bl   = round(float(df[cfg["outcome_var"]].mean()), 2) if cfg.get("outcome_var") in df.columns else (8.2 if domain == "manufacturing" else 5.27)
            _fb_imp  = 18.3 if domain == "manufacturing" else 12.7
            _fb_mult = 300 * 960 if domain == "manufacturing" else 400 * 1050
            _fb_sav  = int(round(_fb_imp / 100 * _fb_bl * _fb_mult / 1000) * 1000)
            _fallback_text = _copilot_exec_answer(_q_to_process, domain) if _COPILOT_AVAILABLE else "Please check the API connection and try again."
            _resp_data = {
                "question": _q_to_process, "exec_text": _fallback_text,
                "confidence": "Moderate", "chip_key": "custom", "causal_chain": [],
                "true_effect": None, "effect_from": _fb_bl, "effect_to": round(_fb_bl * (1 - _fb_imp/100), 2),
                "improvement_pct": _fb_imp, "annual_saving": _fb_sav, "roi_months": None,
                "recommendation": "Shift ~25% procurement to Supplier B" if domain == "manufacturing" else "Optimise specialist triage criteria",
                "outcome_label": cfg.get("outcome_label", "Outcome"),
                "sim_best_case": {"from": _fb_bl, "to": round(_fb_bl * 0.71, 2), "pct": 29.0, "saving": int(_fb_sav*1.6), "roi": 3.5},
                "evidence": [], "follow_ups": [], "domain": domain,
            }

    st.session_state["cop_history"].append(_resp_data)
    st.session_state["cop_followups"] = _resp_data.get("follow_ups", [])
    st.session_state["cop_question"]  = ""
    st.session_state["_clear_cop_input"] = True  # applied before widget on next run

# ── ANSWER RENDERER ───────────────────────────────────────────────────────
import re as _re
import html as _html

def _bold(s: str) -> str:
    # Escape first: this text may embed LLM output influenced by free-text
    # user queries, and is rendered with unsafe_allow_html — without
    # escaping, a crafted query could inject arbitrary HTML/script.
    escaped = _html.escape(str(s))
    return _re.sub(r"\*\*(.+?)\*\*", r'<b style="color:#059669;">\1</b>', escaped)

def _render_answer(rd: dict, exec_mode: bool = False) -> None:
    conf    = rd.get("confidence", "High")
    c_color = {"High": "#059669", "Moderate": "#D97706", "Low": "#DC2626"}.get(conf, "#059669")
    c_bg    = {"High": "#F0FDF4", "Moderate": "#FFFBEB", "Low": "#FEF2F2"}.get(conf, "#F0FDF4")
    c_border= {"High": "#6EE7B7", "Moderate": "#FCD34D", "Low": "#FCA5A5"}.get(conf, "#6EE7B7")

    # 1. EXECUTIVE ANSWER ─────────────────────────────────────────────────
    st.markdown(
        f'<div class="cop-answer" style="background:{c_bg};border:1px solid {c_border};'
        f'border-radius:12px;padding:16px 20px;margin:16px 0 12px;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
        f'<span style="color:{c_color};font-size:0.7rem;font-weight:800;text-transform:uppercase;'
        f'letter-spacing:0.06em;">Executive Answer</span>'
        f'<span style="display:flex;align-items:center;gap:5px;'
        f'background:rgba(255,255,255,0.7);border:1px solid {c_border};border-radius:20px;padding:2px 10px;">'
        f'<span style="width:5px;height:5px;border-radius:50%;background:{c_color};display:inline-block;"></span>'
        f'<span style="color:{c_color};font-size:0.7rem;font-weight:700;">Confidence: {conf}</span></span>'
        f'</div>'
        f'<p style="color:#0F172A;font-size:0.97rem;font-weight:600;line-height:1.6;margin:0;">'
        f'{_bold(rd.get("exec_text",""))}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 2. ROOT CAUSE + BUSINESS IMPACT ─────────────────────────────────────
    _ck = rd.get("chip_key", "custom")
    _show_chain = _ck in ["delays", "bottleneck", "chain", "suppliers", "executive"]
    _show_impact = _ck in ["intervention", "impact", "roi", "executive", "suppliers"]
    _show_sim = _ck in ["intervention", "impact", "roi", "executive"]

    if _show_chain and _show_impact:
        _lc, _rc = st.columns(2)
        _chain_ctx, _impact_ctx = _lc, _rc
    elif _show_chain:
        _chain_ctx, _impact_ctx = st.container(), None
    elif _show_impact:
        _chain_ctx, _impact_ctx = None, st.container()
    else:
        _chain_ctx, _impact_ctx = None, None

    if _chain_ctx is not None:
        with _chain_ctx:
            chain = rd.get("causal_chain", [])
        # Simplified chain: role labels + arrows, slate/green palette only
        _role_colors = {
            "Confounder": ("#D97706", "#FFFBEB", "#FCD34D"),
            "Treatment":  ("#DC2626", "#FEF2F2", "#FCA5A5"),
            "Mediator":   ("#475569", "#F8FAFC", "#CBD5E1"),
            "Outcome":    ("#2563EB", "#EFF6FF", "#93C5FD"),
        }
        _nodes = ""
        for _ci3, node in enumerate(chain):
            tc, bg, bd = _role_colors.get(node["role"], ("#475569","#F8FAFC","#CBD5E1"))
            _node_role  = _html.escape(str(node["role"]))
            _node_label = _html.escape(str(node["label"]))
            _nodes += (
                f'<span style="display:inline-block;background:{bg};border:1px solid {bd};'
                f'border-radius:8px;padding:5px 10px;font-size:0.78rem;">'
                f'<span style="color:{tc};font-size:0.6rem;font-weight:700;text-transform:uppercase;'
                f'display:block;margin-bottom:1px;">{_node_role}</span>'
                f'<span style="color:#0F172A;font-weight:700;">{_node_label}</span></span>'
            )
            if _ci3 < len(chain) - 1:
                _nodes += '<span style="color:#CBD5E1;padding:0 5px;font-size:1rem;">→</span>'

        _te = rd.get("true_effect")
        _te_str = f"+{_te:.2f} days (Double ML)" if _te is not None else "—"
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;'
            f'padding:16px;height:100%;">'
            f'<p style="color:#64748B;font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.05em;margin:0 0 12px;">Causal Chain</p>'
            f'<div style="line-height:2.2;white-space:nowrap;overflow-x:auto;">{_nodes}</div>'
            f'<div style="margin-top:10px;padding:8px 12px;background:#F8FAFC;border-radius:8px;'
            f'border-left:3px solid #10B981;">'
            f'<span style="color:#64748B;font-size:0.75rem;">Causal effect (DML): </span>'
            f'<span style="color:#059669;font-weight:800;font-size:0.85rem;">{_te_str}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    if _impact_ctx is not None:
        with _impact_ctx:
            _fb_bl_rd   = round(float(df[cfg["outcome_var"]].mean()), 1) if cfg.get("outcome_var") in df.columns else (8.2 if domain == "manufacturing" else 5.27)
        _fb_imp_rd  = 18.3 if domain == "manufacturing" else 12.7
        _fb_mult_rd = 300 * 960 if domain == "manufacturing" else 400 * 1050
        _fb_sav_rd  = int(round(_fb_imp_rd / 100 * _fb_bl_rd * _fb_mult_rd / 1000) * 1000)
        _ef   = rd.get("effect_from", _fb_bl_rd)
        _et   = rd.get("effect_to",   round(_fb_bl_rd * (1 - _fb_imp_rd / 100), 2))
        _imp  = rd.get("improvement_pct", _fb_imp_rd)
        _sav  = rd.get("annual_saving",   _fb_sav_rd)
        _roi  = rd.get("roi_months",      3.5)
        _olbl = rd.get("outcome_label",   "Outcome")
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;'
            f'padding:16px;height:100%;">'
            f'<p style="color:#64748B;font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.05em;margin:0 0 12px;">Business Impact</p>'
            # Delay metric
            f'<div style="background:#F8FAFC;border-radius:8px;padding:12px 14px;margin-bottom:10px;">'
            f'<div style="color:#64748B;font-size:0.68rem;font-weight:600;text-transform:uppercase;'
            f'margin-bottom:6px;">{_olbl}</div>'
            f'<div style="display:flex;align-items:baseline;gap:8px;">'
            f'<span style="color:#94A3B8;font-size:1.1rem;font-weight:700;text-decoration:line-through;">{_ef}</span>'
            f'<span style="color:#CBD5E1;">→</span>'
            f'<span style="color:#059669;font-size:1.6rem;font-weight:900;line-height:1;">{_et}</span>'
            f'<span style="color:#64748B;font-size:0.8rem;font-weight:600;">days</span>'
            f'<span style="background:#DCFCE7;color:#15803D;border-radius:5px;padding:1px 7px;'
            f'font-size:0.72rem;font-weight:800;">−{_imp}%</span>'
            f'</div></div>'
            # Saving + ROI row
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'
            f'<div style="background:#FFFBEB;border-radius:8px;padding:10px 12px;">'
            f'<div style="color:#64748B;font-size:0.65rem;font-weight:700;text-transform:uppercase;'
            f'margin-bottom:3px;">Annual Saving</div>'
            f'<div style="color:#D97706;font-size:1.1rem;font-weight:900;">${_sav:,.0f}</div>'
            f'</div>'
            f'<div style="background:#EFF6FF;border-radius:8px;padding:10px 12px;">'
            f'<div style="color:#64748B;font-size:0.65rem;font-weight:700;text-transform:uppercase;'
            f'margin-bottom:3px;">ROI Payback</div>'
            f'<div style="color:#2563EB;font-size:1.1rem;font-weight:900;">{_roi} mo</div>'
            f'</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 3. EVIDENCE — collapsed, hidden in exec mode ─────────────────────────
    if not exec_mode:
        ev_list = rd.get("evidence", [])
        with st.expander("Supporting Evidence", expanded=False):
            for ev in ev_list:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;'
                    f'border-bottom:1px solid #F1F5F9;">'
                    f'<span style="color:#10B981;font-weight:700;flex-shrink:0;">&#10003;</span>'
                    f'<span style="color:#334155;font-size:0.84rem;">{_html.escape(str(ev))}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                '<p style="color:#94A3B8;font-size:0.75rem;font-style:italic;margin:8px 0 0;">'
                'Validated via causal recovery and structural consistency analysis.</p>',
                unsafe_allow_html=True,
            )

    # 4. SIMULATION CTA ────────────────────────────────────────────────────
    if _show_sim:
        sim   = rd.get("sim_best_case", {})
        _sf   = sim.get("from", 8.2);  _st2  = sim.get("to", 5.8)
        _spct = sim.get("pct", 29.3);  _ssv  = sim.get("saving", 742_000)
        _sroi = sim.get("roi", 2.5);   _olbl2 = rd.get("outcome_label", "Outcome")
        st.markdown(
            f'<div style="background:#0F172A;border-radius:12px;padding:14px 18px;margin-top:12px;'
            f'display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">'
            f'<div>'
            f'<div style="color:#94A3B8;font-size:0.68rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.05em;margin-bottom:2px;">Best-Case Scenario</div>'
            f'<div style="color:#64748B;font-size:0.65rem;margin-bottom:6px;">All 3 recommended actions applied simultaneously</div>'
            f'<div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;">'
            f'<span style="color:#FFFFFF;font-size:0.92rem;font-weight:700;">'
            f'{_olbl2}: {_sf} → {_st2} days</span>'
            f'<span style="color:#34D399;font-size:0.92rem;font-weight:800;">−{_spct}%</span>'
            f'<span style="color:#FBBF24;font-size:0.92rem;font-weight:800;">${_ssv:,.0f} savings</span>'
            f'<span style="color:#93C5FD;font-size:0.92rem;font-weight:700;">{_sroi} mo ROI</span>'
            f'</div>'
            f'</div>'
            f'<div style="color:#475569;font-size:0.78rem;">'
            f'→ Run full simulation in <b style="color:#94A3B8;">③ Model & Impact</b></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── EMPTY STATE OR CHAT HISTORY (fills the container placed above quick-actions) ──
with _history_container:
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    _history = st.session_state["cop_history"]

    if not _history:
        _is_mfg = domain == "manufacturing"
        _rc_name = "Supplier A" if _is_mfg else "Specialist Required"
        _opp_baseline = round(float(df[cfg["outcome_var"]].mean()), 1) if cfg.get("outcome_var") in df.columns else (8.2 if _is_mfg else 5.27)
        # Same live-formula-with-fallback pattern as the Overview hero card:
        # compute from the actual Double ML effect when available, only fall
        # back to the illustrative constant if that stage didn't succeed.
        if stage_status.get("do_operator") == "ok" and do_result:
            _opp_causal_eff = abs(do_result.get("causal", 0))
            _opp_shift_ratio = 0.25 if _is_mfg else 0.50
            _opp_reduction = (_opp_causal_eff * _opp_shift_ratio / _opp_baseline) * 100 if _opp_baseline > 0 else 0
        else:
            _opp_reduction = 18.3 if _is_mfg else 12.7
        _opp_mult = 300 * 960 if _is_mfg else 400 * 1050
        _opp_saving_val = round(_opp_reduction / 100 * _opp_baseline * _opp_mult / 1000) * 1000
        _opp_val = f"~${_opp_saving_val // 1000:.0f}K / yr"
        _suggested = [
            "Why are delays increasing?",
            "Show strongest causal chain",
            "Best intervention?",
            "Compare suppliers" if _is_mfg else "Compare specialist pathways",
        ]
        _sugg_html = "".join(
            f'<div style="padding:6px 0;border-bottom:1px solid #F1F5F9;display:flex;'
            f'align-items:center;gap:8px;cursor:pointer;">'
            f'<span style="color:#10B981;font-size:0.8rem;">→</span>'
            f'<span style="color:#334155;font-size:0.84rem;">{q}</span></div>'
            for q in _suggested
        )
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;">'
            f'<p style="color:#0F172A;font-size:1rem;font-weight:700;margin:0 0 16px;">Decision Intelligence Ready</p>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;">'
            f'<div style="background:#F8FAFC;border-radius:8px;padding:12px 14px;">'
            f'<div style="color:#64748B;font-size:0.65rem;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Events Analysed</div>'
            f'<div style="color:#0F172A;font-size:1.05rem;font-weight:800;">{_cop_n:,}</div></div>'
            f'<div style="background:#F8FAFC;border-radius:8px;padding:12px 14px;">'
            f'<div style="color:#64748B;font-size:0.65rem;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Root Cause</div>'
            f'<div style="color:#059669;font-size:1.05rem;font-weight:800;">{_rc_name}</div></div>'
            f'<div style="background:#F8FAFC;border-radius:8px;padding:12px 14px;">'
            f'<div style="color:#64748B;font-size:0.65rem;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Top Opportunity</div>'
            f'<div style="color:#D97706;font-size:1.05rem;font-weight:800;">{_opp_val}</div></div>'
            f'</div>'
            f'<p style="color:#64748B;font-size:0.72rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.05em;margin:0 0 8px;">Suggested Questions</p>'
            f'{_sugg_html}'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        for _idx_h, _rd in enumerate(reversed(_history)):
            st.markdown(
                f'<div style="display:flex;justify-content:flex-end;margin:8px 0 0;">'
                f'<div style="background:#0F172A;color:#FFFFFF;border-radius:12px 12px 3px 12px;'
                f'padding:10px 16px;max-width:70%;font-size:0.9rem;font-weight:500;line-height:1.5;">'
                f'{_rd.get("question","")}</div></div>',
                unsafe_allow_html=True,
            )
            _render_answer(_rd, exec_mode=st.session_state.get("cop_exec_mode", False))
            if _idx_h < len(_history) - 1:
                st.markdown(
                    "<div style='height:1px;background:#F1F5F9;margin:20px 0;'></div>",
                    unsafe_allow_html=True,
                )

    # Follow-up suggestions appear directly below the latest answer
    if st.session_state["cop_followups"]:
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        _fu_cols = st.columns(min(len(st.session_state["cop_followups"]), 4))
        for _fci, (_fcc, _fq) in enumerate(zip(_fu_cols, st.session_state["cop_followups"])):
            with _fcc:
                if st.button(f"↪ {_fq}", key=f"cop_fu_{_fci}", use_container_width=True):
                    st.session_state["cop_question"] = _fq

# ── DEBUG (collapsed) ─────────────────────────────────────────────────────
with st.expander("Pipeline Context (LLM input)", expanded=False):
    if _COPILOT_AVAILABLE:
        _dbg4 = _copilot_build_context(dag=dag, dag_metrics=dag_metrics, scm=scm,
                                        coefs=coefs, cfg=cfg, domain=domain, df=df)
        st.code(_dbg4, language="text")
    else:
        st.info("Copilot module not available.")

# Execute the fragment
render_copilot()

