# -*- coding: utf-8 -*-
"""
Patch dashboard.py — DAG animation v4 (Professional).
Removes: sparks, glow animations, bouncy easing, blinking dot, big F1 counter.
Keeps: sequential edge draw, dashed confounding, clean completion banner.
"""
import sys, re

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

m_start = re.search(r'    # Animated Causal Discovery', src)
m_end   = re.search(r'    # 2\. Ablation Study', src)
if not m_start or not m_end:
    print("ERROR: markers not found"); sys.exit(1)

si, ei = m_start.start(), m_end.start()
print(f"Replacing lines {src[:si].count(chr(10))+1}–{src[:ei].count(chr(10))}")

NEW_BLOCK = r'''    # Animated Causal Discovery v4 (Professional) ────────────────────────────
    if dag.number_of_nodes() > 0:
        import math as _math
        import json as _json
        import streamlit.components.v1 as _stc

        _f1   = dag_metrics.get("f1_score",  0.0)
        _prec = dag_metrics.get("precision", 0.0)
        _rec  = dag_metrics.get("recall",    0.0)

        # ── Classify nodes ───────────────────────────────────────────────
        _node_role: Dict[str, str] = {}
        for _n in dag.nodes():
            if _n == outcome_var:      _node_role[_n] = "outcome"
            elif _n == treatment_var:  _node_role[_n] = "treatment"
            elif _n in confounder_set: _node_role[_n] = "confounder"
            else:                      _node_role[_n] = "mediator"

        # Flat professional palette — no gradients
        _ROLE_COLOR  = {"outcome":"#DC2626","treatment":"#059669",
                        "confounder":"#D97706","mediator":"#4F46E5"}
        _ROLE_RADIUS = {"outcome":46,"treatment":38,"confounder":40,"mediator":33}

        # ── Layout ──────────────────────────────────────────────────────
        _CW, _CH = 760, 440
        _bkt: Dict[str, list] = {k:[] for k in ("confounder","treatment","mediator","outcome")}
        for _n, _r in _node_role.items():
            _bkt[_r].append(_n)

        def _vcenter(nodes, cy=220, gap=120):
            n = len(nodes)
            return [int(cy + (i-(n-1)/2)*gap) for i in range(n)]

        _pos: Dict[str, Dict] = {}
        for _i, _nd in enumerate(_bkt["confounder"]):
            _pos[_nd] = {"x": 90,  "y": _vcenter(_bkt["confounder"])[_i]}
        for _i, _nd in enumerate(_bkt["treatment"]):
            _pos[_nd] = {"x": 245, "y": _vcenter(_bkt["treatment"])[_i]}
        for _i, _nd in enumerate(_bkt["outcome"]):
            _pos[_nd] = {"x": 680, "y": _vcenter(_bkt["outcome"])[_i]}

        _meds    = _bkt["mediator"]
        _len_med = len(_meds) + 1
        _row_h   = min(120, max(80, (_CH-120) // max(_len_med//2, 1)))
        for _i, _nd in enumerate(_meds):
            _pos[_nd] = {
                "x": 415 + (_i % 2) * 95,
                "y": max(70, min(_CH-60, 80 + (_i//2) * _row_h)),
            }

        # ── Node label (balanced 2-line) ─────────────────────────────────
        def _nlabel(name):
            words = name.replace("_", " ").title().split()
            if len(words) == 1: return words[0]
            mid = len(words) // 2
            return " ".join(words[:mid]) + "<br>" + " ".join(words[mid:])

        # ── SVG edge paths (Python-computed, no JS coord math) ───────────
        def _edge_path(sn, dn):
            p1, p2 = _pos[sn], _pos[dn]
            r1 = _ROLE_RADIUS[_node_role[sn]]
            r2 = _ROLE_RADIUS[_node_role[dn]]
            dx, dy = p2["x"]-p1["x"], p2["y"]-p1["y"]
            d = _math.hypot(dx, dy)
            if d < 1: return None
            nx_, ny_ = dx/d, dy/d
            sx = p1["x"] + nx_*(r1+3);  sy = p1["y"] + ny_*(r1+3)
            ex = p2["x"] - nx_*(r2+8);  ey = p2["y"] - ny_*(r2+8)
            return f"M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f}"

        # Normal edges first, confounding last
        _sorted_edges = sorted(dag.edges(), key=lambda e: (e[0], e[1]) in confound_path_edges)

        _svg_paths, _edge_meta, _pi = [], [], 0
        for _s, _d in _sorted_edges:
            _cf  = (_s, _d) in confound_path_edges
            _pth = _edge_path(_s, _d)
            if _pth is None: continue
            _col    = "#DC2626" if _cf else "#6366F1"
            _marker = "am-c" if _cf else "am-n"
            if _cf:
                # Confounding: dashed line, fade in via opacity
                _svg_paths.append(
                    f'<path id="e{_pi}" d="{_pth}" stroke="{_col}" stroke-width="1.5" '
                    f'fill="none" stroke-dasharray="6 4" '
                    f'marker-end="url(#{_marker})" class="ec" opacity="0"/>'
                )
            else:
                # Causal: solid line, draw via stroke-dashoffset
                _svg_paths.append(
                    f'<path id="e{_pi}" d="{_pth}" stroke="{_col}" stroke-width="1.5" '
                    f'fill="none" stroke-dasharray="2000" stroke-dashoffset="2000" '
                    f'marker-end="url(#{_marker})" class="en" opacity="0"/>'
                )
            _edge_meta.append({"c": _cf, "col": _col})
            _pi += 1

        _n_norm  = sum(1 for e in _edge_meta if not e["c"])
        _n_total = len(_edge_meta)

        # ── Node divs ────────────────────────────────────────────────────
        _node_divs = ""
        for _nd in dag.nodes():
            _r = _ROLE_RADIUS[_node_role[_nd]]
            _c = _ROLE_COLOR[_node_role[_nd]]
            _node_divs += (
                f'<div class="dn" id="nd-{_nd}" data-role="{_node_role[_nd]}" '
                f'style="left:{_pos[_nd]["x"]}px;top:{_pos[_nd]["y"]}px;'
                f'width:{_r*2}px;height:{_r*2}px;background:{_c};">'
                f'<div class="nl">{_nlabel(_nd)}</div></div>\n'
            )

        _svg_body   = "\n".join(_svg_paths)
        _emeta_json = _json.dumps(_edge_meta)
        _nids_json  = _json.dumps([str(n) for n in dag.nodes()])

        _stc.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0A0E17;font-family:-apple-system,'Inter',sans-serif;overflow:hidden;}}
.wrap{{
  position:relative;width:760px;height:440px;margin:0 auto;
  background:#0A0E17;border:1px solid #1A1F2E;border-radius:12px;overflow:hidden;
}}
svg{{position:absolute;top:0;left:0;z-index:1;overflow:visible;}}
#nh{{position:absolute;inset:0;z-index:10;}}

/* Nodes */
.dn{{
  position:absolute;border-radius:50%;
  display:flex;align-items:center;justify-content:center;flex-direction:column;
  cursor:grab;user-select:none;
  border:1.5px solid rgba(255,255,255,0.12);
  box-shadow:0 2px 12px rgba(0,0,0,0.4);
  transform:translate(-50%,-50%) scale(0.85);opacity:0;
  transition:opacity 0.4s cubic-bezier(0.4,0,0.2,1),
             transform 0.4s cubic-bezier(0.4,0,0.2,1),
             box-shadow 0.3s ease;
}}
.dn.vis{{transform:translate(-50%,-50%) scale(1);opacity:1;}}
.dn:hover{{
  box-shadow:0 0 0 3px rgba(255,255,255,0.08),0 2px 12px rgba(0,0,0,0.4)!important;
  transform:translate(-50%,-50%) scale(1.05)!important;z-index:99;
}}
.dn:active{{cursor:grabbing;}}
/* Confounding: subtle static ring, no animation */
.dn.cring{{box-shadow:0 0 0 2px rgba(220,38,38,0.4),0 2px 12px rgba(0,0,0,0.4);}}
.nl{{
  font-size:11.5px;font-weight:600;color:#fff;text-align:center;
  line-height:1.35;padding:0 6px;pointer-events:none;
  text-shadow:0 1px 3px rgba(0,0,0,0.8);
}}

/* Edge transitions — material easing, no glow */
.en{{transition:stroke-dashoffset 0.5s cubic-bezier(0.4,0,0.2,1),
              opacity 0.35s cubic-bezier(0.4,0,0.2,1);}}
.ec{{transition:opacity 0.5s cubic-bezier(0.4,0,0.2,1);}}

/* Status bar */
.sbar{{
  position:absolute;top:10px;left:10px;right:10px;
  display:flex;align-items:center;justify-content:space-between;
  z-index:40;pointer-events:none;
}}
.abadge{{
  display:flex;align-items:center;gap:8px;
  background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);
  border-radius:6px;padding:6px 14px;
}}
.adot{{width:5px;height:5px;border-radius:50%;background:#818CF8;flex-shrink:0;}}
.adot.ok{{background:#10B981;}}
.atxt{{font-size:11px;font-weight:600;color:#818CF8;letter-spacing:0.04em;}}
.ectr{{
  background:rgba(10,14,23,0.9);border:1px solid #1A1F2E;
  border-radius:6px;padding:4px 12px;font-size:11px;color:#4B5563;
}}
.ectr b{{color:#6366F1;font-weight:700;}}

/* Completion banner — slides down, no big numbers */
.banner{{
  position:absolute;top:0;left:50%;
  transform:translateX(-50%) translateY(-50px);opacity:0;
  background:rgba(6,78,59,0.10);border:1px solid rgba(16,185,129,0.22);
  border-radius:8px;padding:8px 18px;
  transition:transform 0.4s cubic-bezier(0.4,0,0.2,1),opacity 0.4s ease;
  z-index:50;pointer-events:none;white-space:nowrap;
}}
.banner.show{{transform:translateX(-50%) translateY(8px);opacity:1;pointer-events:all;}}
.brow{{display:flex;align-items:center;gap:12px;}}
.bchk{{font-size:13px;color:#10B981;}}
.btxt{{font-size:12px;font-weight:600;color:#10B981;}}
.bmeta{{font-size:11px;color:#4B5563;}}
.bmeta b{{color:#6B7280;font-weight:600;}}
.rbtn{{
  background:transparent;border:1px solid rgba(99,102,241,0.3);
  border-radius:5px;padding:3px 10px;color:#818CF8;
  font-size:10px;font-weight:600;cursor:pointer;
  transition:background 0.2s;letter-spacing:0.04em;
}}
.rbtn:hover{{background:rgba(99,102,241,0.1);}}

/* Legend */
.leg{{
  position:absolute;bottom:10px;left:10px;
  display:flex;gap:14px;z-index:30;
  pointer-events:none;opacity:0;transition:opacity 0.5s;
}}
.leg.show{{opacity:1;}}
.li{{display:flex;align-items:center;gap:5px;font-size:9.5px;color:#4B5563;font-weight:600;}}
.lc{{width:8px;height:8px;border-radius:50%;flex-shrink:0;}}
.ll{{width:18px;height:1.5px;flex-shrink:0;}}

/* Tooltip */
.tt{{
  position:absolute;background:#111827;border:1px solid #1F2937;
  border-radius:6px;padding:7px 11px;font-size:10px;color:#D1D5DB;
  pointer-events:none;z-index:100;opacity:0;transition:opacity 0.15s;
  max-width:180px;line-height:1.5;
}}
.tt.show{{opacity:1;}}
</style></head><body>
<div class="wrap">

  <!-- Status bar -->
  <div class="sbar">
    <div class="abadge">
      <div class="adot" id="adot"></div>
      <div class="atxt" id="atxt">Initializing PC algorithm</div>
    </div>
    <div class="ectr">Edges: <b id="ec">0</b>/{_n_total}</div>
  </div>

  <!-- SVG layer: pre-computed paths, no sparks group -->
  <svg id="dag-svg" width="760" height="440">
    <defs>
      <marker id="am-n" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" fill="#6366F1" fill-opacity="0.8"/>
      </marker>
      <marker id="am-c" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" fill="#DC2626" fill-opacity="0.85"/>
      </marker>
    </defs>
    <g id="edges-g">
{_svg_body}
    </g>
  </svg>

  <!-- Node host -->
  <div id="nh">
{_node_divs}  </div>

  <!-- Completion banner -->
  <div class="banner" id="banner">
    <div class="brow">
      <span class="bchk">&#10003;</span>
      <span class="btxt">Causal structure recovered</span>
      <span class="bmeta">F1&nbsp;<b>{_f1:.3f}</b>&nbsp;&middot;&nbsp;Precision&nbsp;<b>{_prec:.3f}</b>&nbsp;&middot;&nbsp;Recall&nbsp;<b>{_rec:.3f}</b></span>
      <button class="rbtn" onclick="replay()">&#8635; Replay</button>
    </div>
  </div>

  <!-- Legend -->
  <div class="leg" id="leg">
    <div class="li"><div class="ll" style="background:#6366F1;"></div>Causal edge</div>
    <div class="li">
      <svg width="18" height="4" style="flex-shrink:0">
        <line x1="0" y1="2" x2="18" y2="2" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="5,3"/>
      </svg>
      Confounding
    </div>
    <div class="li"><div class="lc" style="background:#D97706;"></div>Confounder</div>
    <div class="li"><div class="lc" style="background:#059669;"></div>Treatment</div>
    <div class="li"><div class="lc" style="background:#4F46E5;"></div>Mediator</div>
    <div class="li"><div class="lc" style="background:#DC2626;"></div>Outcome</div>
  </div>

  <div class="tt" id="tt"></div>
</div>

<script>
const EDGE_META = {_emeta_json};
const NODE_IDS  = {_nids_json};
const N_NORMAL  = {_n_norm};
const N_TOTAL   = {_n_total};

function setText(id, txt) {{ const el=document.getElementById(id); if(el) el.textContent=txt; }}
function cls(el, ...c)   {{ if(el) c.forEach(x=>el.classList.add(x)); }}
function uncls(el, ...c) {{ if(el) c.forEach(x=>el.classList.remove(x)); }}
function $id(id)         {{ return document.getElementById(id); }}
function $$cls(c)        {{ return document.querySelectorAll('.'+c); }}

// ── Edge reveal (no sparks, no flash) ─────────────────────────────────────────
let ecnt = 0;
function revealEdge(i) {{
  const el   = $id('e'+i);
  const meta = EDGE_META[i];
  if(!el || !meta) return;
  el.style.opacity = '1';
  if(!meta.c) el.style.strokeDashoffset = '0';
  ecnt++;
  setText('ec', ecnt);
  // Confounding: mark all nodes with a subtle static ring
  if(meta.c) $$cls('dn').forEach(n => n.classList.add('cring'));
}}

// ── Animation sequence ────────────────────────────────────────────────────────
let timers = [], done = false;
function clearTimers() {{ timers.forEach(clearTimeout); timers = []; }}

function startAnim() {{
  clearTimers();
  done = false;
  ecnt = 0;

  // Reset edges
  EDGE_META.forEach((m, i) => {{
    const el = $id('e'+i);
    if(!el) return;
    el.style.opacity = '0';
    if(!m.c) el.style.strokeDashoffset = '2000';
  }});

  // Reset nodes
  NODE_IDS.forEach(id => {{
    const el = $id('nd-'+id);
    if(el) uncls(el, 'vis', 'cring');
  }});

  uncls($id('banner'), 'show');
  uncls($id('leg'), 'show');
  setText('ec', '0');

  const dot = $id('adot');
  if(dot) {{ dot.classList.remove('ok'); dot.style.background = '#818CF8'; }}
  setText('atxt', 'Initializing PC algorithm');

  // Phase 1 — nodes appear staggered (200ms apart, smooth ease)
  NODE_IDS.forEach((id, i) => {{
    timers.push(setTimeout(() => {{
      const el = $id('nd-'+id);
      if(el) cls(el, 'vis');
    }}, 200 + i * 200));
  }});

  // Phase 2 — independence test label
  const p2 = 200 + NODE_IDS.length * 200 + 250;
  timers.push(setTimeout(() => setText('atxt', 'Testing conditional independence'), p2));

  // Phase 3 — edges draw one by one
  const p3 = p2 + 1100, step = 480;
  for(let i = 0; i < N_TOTAL; i++) {{
    timers.push(setTimeout(() => {{
      if(i === 0)        setText('atxt', 'Orienting causal edges');
      if(i === N_NORMAL) setText('atxt', 'Identifying backdoor paths');
      revealEdge(i);
    }}, p3 + i * step));
  }}

  // Phase 4 — backdoor criterion note
  const p4 = p3 + N_TOTAL * step + 300;
  timers.push(setTimeout(() => setText('atxt', 'Backdoor criterion applied'), p4));

  // Phase 5 — completion banner slides down
  const p5 = p4 + 700;
  timers.push(setTimeout(() => {{
    cls($id('banner'), 'show');
    cls($id('leg'),    'show');
    const dot = $id('adot');
    if(dot) {{ dot.style.background = '#10B981'; dot.classList.add('ok'); }}
    setText('atxt', 'Discovery complete');
    done = true;
  }}, p5));
}}

function replay() {{
  uncls($id('banner'), 'show');
  setTimeout(startAnim, 300);
}}

// ── Drag (post-animation only, for exploration) ───────────────────────────────
let isDrag = false, dragId = null, dox = 0, doy = 0;
const wrap = document.querySelector('.wrap');

wrap.addEventListener('mousedown', e => {{
  if(!done) return;
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX - wR.left, my = e.clientY - wR.top;
  for(const id of NODE_IDS) {{
    const el = $id('nd-'+id);
    if(!el) continue;
    const eR = el.getBoundingClientRect();
    const cx = eR.left - wR.left + eR.width/2;
    const cy = eR.top  - wR.top  + eR.height/2;
    if(Math.hypot(mx-cx, my-cy) < eR.width/2 + 6) {{
      isDrag = true; dragId = id; dox = mx-cx; doy = my-cy;
      el.style.cursor = 'grabbing';
      break;
    }}
  }}
}});

window.addEventListener('mousemove', e => {{
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX - wR.left, my = e.clientY - wR.top;
  if(isDrag && dragId) {{
    const el = $id('nd-'+dragId);
    if(el) {{ el.style.left = (mx-dox)+'px'; el.style.top = (my-doy)+'px'; }}
  }}
  // Tooltip on hover
  if(!isDrag && done) {{
    let found = false;
    for(const id of NODE_IDS) {{
      const el = $id('nd-'+id);
      if(!el) continue;
      const eR = el.getBoundingClientRect();
      const cx = eR.left - wR.left + eR.width/2;
      const cy = eR.top  - wR.top  + eR.height/2;
      if(Math.hypot(mx-cx, my-cy) < eR.width/2 + 4) {{
        const tt = $id('tt');
        if(tt) {{
          tt.innerHTML = '<b style="color:#818CF8">' + el.dataset.role + '</b>';
          tt.style.left = (cx + eR.width/2 + 8) + 'px';
          tt.style.top  = (cy - 18) + 'px';
          cls(tt, 'show');
        }}
        found = true;
        break;
      }}
    }}
    if(!found) uncls($id('tt'), 'show');
  }}
}});

window.addEventListener('mouseup', () => {{
  if(dragId) {{ const el = $id('nd-'+dragId); if(el) el.style.cursor = 'grab'; }}
  isDrag = false; dragId = null;
}});

setTimeout(startAnim, 300);
</script></body></html>""", height=510)

        # Static legend strip below the animation
        _dag_legend_items = [
            (SUCCESS, "Treatment"),
            (ERROR,   "Outcome"),
            (WARNING, "Confounder"),
            (PRIMARY, "Mediator / Other"),
            (ERROR,   "Confounding edge (red dashed)"),
        ]
        st.markdown(
            f'<div style="margin-top:6px;padding:8px 16px;background:{CARD};'
            f'border:1px solid {BORDER};border-radius:8px;display:flex;flex-wrap:wrap;">'
            + "".join(
                f'<span style="display:inline-flex;align-items:center;gap:5px;margin:0 14px 6px 0;">'
                f'<span style="width:10px;height:10px;border-radius:50%;'
                f'background:{_c};display:inline-block;"></span>'
                f'<span style="font-size:0.78rem;color:{MUTED};">{_lbl}</span></span>'
                for _c, _lbl in _dag_legend_items
            )
            + "</div>",
            unsafe_allow_html=True,
        )

'''

out = src[:si] + NEW_BLOCK + src[ei:]

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Done — file is now {len(out):,} chars.")
