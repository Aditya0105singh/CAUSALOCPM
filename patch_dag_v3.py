# -*- coding: utf-8 -*-
"""
Patch dashboard.py — DAG animation v3.
KEY CHANGE: edges are pre-drawn as SVG <path> elements with coordinates
computed in Python. JS just toggles visibility in sequence.
No canvas, no getBoundingClientRect, no coordinate mismatch possible.
"""
import sys, re

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

# Find the animated DAG block
m_start = re.search(r'    # Animated Causal Discovery', src)
m_end   = re.search(r'    # 2\. Ablation Study', src)
if not m_start or not m_end:
    print("ERROR: markers not found"); sys.exit(1)

si, ei = m_start.start(), m_end.start()
print(f"Replacing lines {src[:si].count(chr(10))+1}–{src[:ei].count(chr(10))}")

NEW_BLOCK = r'''    # Animated Causal Discovery v3 (SVG edges) ────────────────────────────────
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

        _ROLE_COLOR  = {"outcome":"#EF4444","treatment":"#10B981",
                        "confounder":"#F59E0B","mediator":"#6C63FF"}
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

        # mediators: 2-column 415/510
        _meds = _bkt["mediator"]
        _nrows = (_len_meds := len(_meds) + 1) // 2
        _row_h = min(120, max(80, (_CH-120) // max((_len_meds)//2, 1)))
        for _i, _nd in enumerate(_meds):
            _pos[_nd] = {
                "x": 415 + (_i % 2) * 95,
                "y": max(70, min(_CH-60, 80 + (_i//2) * _row_h)),
            }

        # ── Node label (balanced 2-line split) ──────────────────────────
        def _nlabel(name):
            words = name.replace("_"," ").title().split()
            if len(words) == 1: return words[0]
            mid = len(words) // 2
            return " ".join(words[:mid]) + "<br>" + " ".join(words[mid:])

        # ── Build SVG edge paths from Python (no JS coord math needed) ──
        def _edge_path(src_n, dst_n):
            p1, p2 = _pos[src_n], _pos[dst_n]
            r1 = _ROLE_RADIUS[_node_role[src_n]]
            r2 = _ROLE_RADIUS[_node_role[dst_n]]
            dx, dy = p2["x"]-p1["x"], p2["y"]-p1["y"]
            d = _math.hypot(dx, dy)
            if d < 1: return None, None, None
            nx_, ny_ = dx/d, dy/d
            sx = p1["x"] + nx_*(r1+3)
            sy = p1["y"] + ny_*(r1+3)
            ex = p2["x"] - nx_*(r2+8)
            ey = p2["y"] - ny_*(r2+8)
            return f"M {sx:.0f} {sy:.0f} L {ex:.0f} {ey:.0f}", ex, ey

        # Sort: normal edges first, confounding last
        _sorted_edges = sorted(dag.edges(), key=lambda e: (e[0],e[1] ) in confound_path_edges)

        _svg_paths    = []   # SVG <path> HTML strings
        _edge_meta    = []   # [{confound, color, ex, ey}]
        for _i, (_s, _d) in enumerate(_sorted_edges):
            _cf = (_s, _d) in confound_path_edges
            _pth, _ex, _ey = _edge_path(_s, _d)
            if _pth is None: continue
            _col    = "#EF4444" if _cf else "#6C63FF"
            _marker = "am-c" if _cf else "am-n"
            _svg_paths.append(
                f'<path id="e{_i}" d="{_pth}" stroke="{_col}" '
                f'stroke-width="{"2.5" if _cf else "2"}" fill="none" '
                f'marker-end="url(#{_marker})" class="edge{"c" if _cf else ""}" '
                f'stroke-dasharray="2000" stroke-dashoffset="2000" opacity="0"/>'
            )
            _edge_meta.append({"confound": _cf, "color": _col,
                                "ex": round(_ex), "ey": round(_ey)})

        _n_norm   = sum(1 for e in _edge_meta if not e["confound"])
        _n_total  = len(_edge_meta)

        # ── Node divs ────────────────────────────────────────────────────
        _node_divs = ""
        for _nd in dag.nodes():
            _r = _ROLE_RADIUS[_node_role[_nd]]
            _c = _ROLE_COLOR[_node_role[_nd]]
            _node_divs += (
                f'<div class="dn" id="nd-{_nd}" '
                f'data-role="{_node_role[_nd]}" '
                f'style="left:{_pos[_nd]["x"]}px;top:{_pos[_nd]["y"]}px;'
                f'width:{_r*2}px;height:{_r*2}px;'
                f'background:radial-gradient(circle at 35% 35%,'
                f'{_c}EE,{_c},{_c}AA);">'
                f'<div class="nl">{_nlabel(_nd)}</div></div>\n'
            )

        # ── SVG markup ───────────────────────────────────────────────────
        _svg_body = "\n".join(_svg_paths)

        # ── Edge meta as JS JSON ─────────────────────────────────────────
        _emeta_json = _json.dumps(_edge_meta)
        _nids_json  = _json.dumps([str(n) for n in dag.nodes()])

        _stc.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0D1117;font-family:-apple-system,'Inter',sans-serif;overflow:hidden;}}
.wrap{{position:relative;width:760px;height:440px;margin:0 auto;}}
/* SVG layer — z-index 1, below nodes */
svg{{position:absolute;top:0;left:0;z-index:1;overflow:visible;}}
/* Nodes host */
#nh{{position:absolute;inset:0;z-index:10;}}
.dn{{
  position:absolute;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  cursor:grab;user-select:none;flex-direction:column;
  border:2.5px solid rgba(255,255,255,0.18);
  box-shadow:0 4px 24px rgba(0,0,0,0.7);
  transform:translate(-50%,-50%) scale(0);opacity:0;
  transition:transform 0.45s cubic-bezier(0.34,1.56,0.64,1),opacity 0.3s ease;
}}
.dn.vis{{transform:translate(-50%,-50%) scale(1);opacity:1;}}
.dn:hover{{transform:translate(-50%,-50%) scale(1.1)!important;z-index:99;}}
.dn:active{{cursor:grabbing;}}
.dn.ana{{animation:ana 0.8s ease-in-out infinite;}}
@keyframes ana{{
  0%,100%{{box-shadow:0 4px 24px rgba(0,0,0,0.7),0 0 0 0 rgba(255,255,255,0.2);}}
  50%{{box-shadow:0 4px 24px rgba(0,0,0,0.7),0 0 0 16px rgba(255,255,255,0);}}
}}
.dn.cglow{{animation:cg 1.1s ease-in-out infinite!important;}}
@keyframes cg{{
  0%,100%{{box-shadow:0 4px 24px rgba(0,0,0,0.7),0 0 10px 3px rgba(239,68,68,0.4);}}
  50%{{box-shadow:0 4px 24px rgba(0,0,0,0.7),0 0 30px 12px rgba(239,68,68,0.8);}}
}}
.nl{{font-size:11.5px;font-weight:700;color:#fff;text-align:center;
     line-height:1.35;padding:0 6px;pointer-events:none;
     text-shadow:0 1px 4px rgba(0,0,0,0.95);}}
/* Edges — path drawing via stroke-dashoffset transition */
.edge{{transition:stroke-dashoffset 0.55s ease,opacity 0.15s ease;}}
.edge.flash{{filter:drop-shadow(0 0 6px #6C63FF);}}
.edgec{{transition:stroke-dashoffset 0.55s ease,opacity 0.15s ease;}}
.edgec.flash{{filter:drop-shadow(0 0 8px #EF4444);}}
.confglow{{animation:confpulse 1.2s ease-in-out infinite;}}
@keyframes confpulse{{
  0%,100%{{filter:drop-shadow(0 0 3px rgba(239,68,68,0.5));}}
  50%{{filter:drop-shadow(0 0 14px rgba(239,68,68,0.9));}}
}}
/* Status bar */
.sbar{{position:absolute;top:8px;left:8px;right:8px;display:flex;
  align-items:center;justify-content:space-between;z-index:40;pointer-events:none;}}
.abadge{{display:flex;align-items:center;gap:7px;
  background:rgba(108,99,255,0.13);border:1px solid rgba(108,99,255,0.3);
  border-radius:20px;padding:5px 12px;}}
.adot{{width:6px;height:6px;border-radius:50%;background:#6C63FF;animation:blink 0.9s infinite;}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:0.1;}}}}
.atxt{{font-size:10px;font-weight:700;color:#A78BFA;letter-spacing:0.08em;text-transform:uppercase;}}
.ectr{{background:rgba(13,17,23,0.9);border:1px solid #1E2433;
  border-radius:8px;padding:4px 12px;font-size:11px;color:#6B7280;}}
.ectr b{{color:#6C63FF;font-weight:700;}}
/* Completion banner — slides down from top */
.banner{{
  position:absolute;top:0;left:50%;
  transform:translateX(-50%) translateY(-80px);
  background:rgba(2,14,6,0.97);border:1.5px solid #10B981;
  border-radius:0 0 14px 14px;padding:10px 24px;z-index:50;
  transition:transform 0.55s cubic-bezier(0.34,1.56,0.64,1);
  pointer-events:none;white-space:nowrap;
  box-shadow:0 4px 20px rgba(16,185,129,0.25);
}}
.banner.show{{transform:translateX(-50%) translateY(0);pointer-events:all;}}
.brow{{display:flex;align-items:center;gap:14px;}}
.bcheck{{font-size:18px;color:#10B981;}}
.btitle{{font-size:11px;font-weight:700;color:#10B981;
  letter-spacing:0.12em;text-transform:uppercase;}}
.bf1{{font-size:24px;font-weight:800;color:#10B981;letter-spacing:-0.03em;}}
.bmeta{{font-size:11px;color:#6B7280;}}
.bmeta b{{color:#9CA3AF;}}
.rbtn{{background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);
  border-radius:7px;padding:5px 12px;color:#10B981;font-size:10px;font-weight:700;
  cursor:pointer;letter-spacing:0.08em;text-transform:uppercase;}}
.rbtn:hover{{background:rgba(16,185,129,0.3);}}
/* Legend */
.leg{{position:absolute;bottom:8px;left:8px;display:flex;gap:12px;
  z-index:30;pointer-events:none;opacity:0;transition:opacity 0.6s;}}
.leg.show{{opacity:1;}}
.li{{display:flex;align-items:center;gap:5px;font-size:9.5px;color:#6B7280;font-weight:600;}}
.lc{{width:9px;height:9px;border-radius:50%;flex-shrink:0;}}
.ll{{width:20px;height:2px;border-radius:1px;flex-shrink:0;}}
/* Tooltip */
.tt{{position:absolute;background:#161B27;border:1px solid #2D3748;border-radius:8px;
  padding:8px 12px;font-size:10px;color:#E2E8F0;pointer-events:none;z-index:100;
  opacity:0;transition:opacity 0.15s;max-width:200px;line-height:1.5;}}
.tt.show{{opacity:1;}}
/* Spark circles in SVG */
@keyframes sparkfly{{
  0%  {{opacity:0.9;r:3;}}
  100%{{opacity:0;r:1;}}
}}
</style></head><body>
<div class="wrap">
  <!-- Status bar -->
  <div class="sbar">
    <div class="abadge">
      <div class="adot" id="adot"></div>
      <div class="atxt" id="atxt">PC Algorithm — Initialising</div>
    </div>
    <div class="ectr">Edges: <b id="ec">0</b>/{_n_total}</div>
  </div>

  <!-- SVG layer: pre-computed edges + sparks -->
  <svg id="dag-svg" width="760" height="440">
    <defs>
      <marker id="am-n" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
        <polygon points="0 0, 9 3.5, 0 7" fill="#6C63FF" fill-opacity="0.85"/>
      </marker>
      <marker id="am-c" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
        <polygon points="0 0, 9 3.5, 0 7" fill="#EF4444"/>
      </marker>
    </defs>
    <g id="edges-g">
{_svg_body}
    </g>
    <g id="sparks-g"></g>
  </svg>

  <!-- Node host -->
  <div id="nh">
{_node_divs}  </div>

  <!-- Completion banner -->
  <div class="banner" id="banner">
    <div class="brow">
      <span class="bcheck">✓</span>
      <span class="btitle">Discovery Complete</span>
      <span class="bf1" id="f1d">0.000</span>
      <span class="bmeta">Precision&nbsp;<b id="pvd">–</b>&nbsp;&middot;&nbsp;Recall&nbsp;<b id="rvd">–</b></span>
      <button class="rbtn" onclick="replay()">&#8635;&nbsp;Replay</button>
    </div>
  </div>

  <!-- Legend -->
  <div class="leg" id="leg">
    <div class="li"><div class="ll" style="background:#6C63FF;"></div>Causal edge</div>
    <div class="li">
      <svg width="20" height="4" style="flex-shrink:0">
        <line x1="0" y1="2" x2="20" y2="2" stroke="#EF4444" stroke-width="2" stroke-dasharray="5,3"/>
      </svg>
      Confounding
    </div>
    <div class="li"><div class="lc" style="background:#F59E0B;"></div>Confounder</div>
    <div class="li"><div class="lc" style="background:#10B981;"></div>Treatment</div>
    <div class="li"><div class="lc" style="background:#6C63FF;"></div>Mediator</div>
    <div class="li"><div class="lc" style="background:#EF4444;"></div>Outcome</div>
  </div>
  <div class="tt" id="tt"></div>
</div>

<script>
// ── Data from Python ──────────────────────────────────────────────────────────
const EDGE_META   = {_emeta_json};
const NODE_IDS    = {_nids_json};
const N_NORMAL    = {_n_norm};
const N_TOTAL     = {_n_total};
const F1_VAL      = {_f1:.3f};
const PR_VAL      = {_prec:.3f};
const RC_VAL      = {_rec:.3f};

// ── Utility ───────────────────────────────────────────────────────────────────
function setText(id, txt) {{ const el=document.getElementById(id); if(el) el.textContent=txt; }}
function setHTML(id, h)   {{ const el=document.getElementById(id); if(el) el.innerHTML=h; }}
function cls(el, ...c)    {{ if(el) c.forEach(x=>el.classList.add(x)); }}
function uncls(el, ...c)  {{ if(el) c.forEach(x=>el.classList.remove(x)); }}
function $id(id)          {{ return document.getElementById(id); }}
function $$cls(c)         {{ return document.querySelectorAll('.'+c); }}

function animCtr(id, target, dur, dec) {{
  const el = $id(id); if(!el) return;
  const t0 = Date.now();
  (function tick() {{
    const p = Math.min((Date.now()-t0)/dur, 1);
    const v = p<0.5 ? 2*p*p : -1+(4-2*p)*p;
    el.textContent = (v*target).toFixed(dec);
    if(p<1) requestAnimationFrame(tick); else el.textContent=target.toFixed(dec);
  }})();
}}

// ── Sparks: SVG circles that fly out and fade ─────────────────────────────────
const sparksG = $id('sparks-g');
function sparkAt(x, y, color, n) {{
  for(let i=0;i<n;i++) {{
    const ang  = (Math.PI*2/n)*i;
    const spd  = 14 + Math.random()*18;
    const dur  = 400 + Math.random()*250;
    const tx   = x + Math.cos(ang)*spd;
    const ty   = y + Math.sin(ang)*spd;
    const c    = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx', x);
    c.setAttribute('cy', y);
    c.setAttribute('r',  3);
    c.setAttribute('fill', color);
    c.setAttribute('opacity', 0.9);
    sparksG.appendChild(c);
    const t0 = Date.now();
    (function anim() {{
      const p = (Date.now()-t0)/dur;
      if(p >= 1) {{ c.remove(); return; }}
      c.setAttribute('cx', x + Math.cos(ang)*spd*p);
      c.setAttribute('cy', y + Math.sin(ang)*spd*p + p*p*10);
      c.setAttribute('opacity', 1-p);
      requestAnimationFrame(anim);
    }})();
  }}
}}

// ── Edge reveal ───────────────────────────────────────────────────────────────
let ecnt = 0;
function revealEdge(i) {{
  const el  = $id('e'+i);
  const meta= EDGE_META[i];
  if(!el || !meta) return;
  el.style.opacity         = '1';
  el.style.strokeDashoffset= '0';
  ecnt++;
  setText('ec', ecnt);
  // Flash + sparks at arrowhead endpoint
  el.classList.add('flash');
  setTimeout(()=>el.classList.remove('flash'), 700);
  sparkAt(meta.ex, meta.ey, meta.color, meta.confound?18:10);
  // Confounding: glow related nodes
  if(meta.confound) {{
    $$cls('dn').forEach(el=>el.classList.add('cglow'));
    el.classList.add('confglow');
  }}
}}

// ── Animation state ───────────────────────────────────────────────────────────
let timers = [], done = false;
function clearTimers() {{ timers.forEach(clearTimeout); timers=[]; }}

function startAnim() {{
  clearTimers();
  done = false; ecnt = 0;
  // Reset edge paths
  document.querySelectorAll('.edge,.edgec').forEach(el=>{{
    el.style.opacity='0'; el.style.strokeDashoffset='2000';
    el.classList.remove('flash','confglow');
  }});
  // Reset nodes
  NODE_IDS.forEach(id=>{{
    const el=$id('nd-'+id);
    if(el) {{ uncls(el,'vis','ana','cglow'); }}
  }});
  uncls($id('banner'),'show');
  uncls($id('leg'),'show');
  setText('ec','0');
  setText('f1d','0.000');
  setText('pvd','–');
  setText('rvd','–');
  $id('adot').style.background='#6C63FF';
  setText('atxt','PC Algorithm — Initialising');

  // Phase 1: nodes appear one by one (0 → ~2.2s)
  NODE_IDS.forEach((id,i) => {{
    timers.push(setTimeout(()=>{{
      const el=$id('nd-'+id);
      if(el) cls(el,'vis');
    }}, 200+i*210));
  }});

  // Phase 2: analysis pulse (~2.4s)
  const p2 = 200 + NODE_IDS.length*210 + 350;
  timers.push(setTimeout(()=>{{
    setText('atxt','PC Algorithm — Running Independence Tests');
    NODE_IDS.forEach(id=>{{ const el=$id('nd-'+id); if(el) cls(el,'ana'); }});
  }}, p2));

  // Phase 3: edges appear one by one (p2+1.4s → p3+N*0.6s)
  const p3   = p2 + 1400;
  const step = 560;
  for(let i=0; i<N_TOTAL; i++) {{
    const delay = p3 + i*step;
    timers.push(setTimeout(()=>{{
      if(i===0) {{
        NODE_IDS.forEach(id=>{{ const el=$id('nd-'+id); if(el) uncls(el,'ana'); }});
        setText('atxt','PC Algorithm — Orienting Edges');
      }}
      if(i===N_NORMAL)
        setText('atxt','Identifying Confounding Paths…');
      revealEdge(i);
    }}, delay));
  }}

  // Phase 4: confound glow
  const p4 = p3 + N_TOTAL*step + 400;
  timers.push(setTimeout(()=>{{
    setText('atxt','Confounding Path Identified — Backdoor Criterion Applied');
  }}, p4));

  // Phase 5: complete banner
  const p5 = p4 + 1200;
  timers.push(setTimeout(()=>{{
    cls($id('banner'),'show');
    cls($id('leg'),'show');
    animCtr('f1d', F1_VAL, 1400, 3);
    animCtr('pvd', PR_VAL, 1200, 3);
    animCtr('rvd', RC_VAL, 1200, 3);
    $id('adot').style.background='#10B981';
    setText('atxt','Discovery Complete — F1 '+F1_VAL.toFixed(3));
    done = true;
  }}, p5));
}}

function replay() {{
  uncls($id('banner'),'show');
  timers.push(setTimeout(startAnim, 300));
}}

// ── Drag: update node left/top CSS (edges stay correct since SVG is pre-drawn) ─
// NOTE: after dragging, edges won't follow because they are pre-drawn SVG.
// After animation, edges are visible; drag is for exploration only.
let isDrag=false, dragId=null, dox=0, doy=0;
const wrap = document.querySelector('.wrap');

wrap.addEventListener('mousedown', e => {{
  if(!done) return;
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX-wR.left, my = e.clientY-wR.top;
  for(const id of NODE_IDS) {{
    const el = $id('nd-'+id);
    if(!el) continue;
    const eR = el.getBoundingClientRect();
    const cx = eR.left-wR.left+eR.width/2;
    const cy = eR.top -wR.top +eR.height/2;
    if(Math.hypot(mx-cx, my-cy) < eR.width/2+6) {{
      isDrag=true; dragId=id; dox=mx-cx; doy=my-cy;
      el.style.cursor='grabbing'; break;
    }}
  }}
}});
window.addEventListener('mousemove', e => {{
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX-wR.left, my = e.clientY-wR.top;
  if(isDrag && dragId) {{
    const el = $id('nd-'+dragId);
    if(el) {{ el.style.left=(mx-dox)+'px'; el.style.top=(my-doy)+'px'; }}
  }}
  // Tooltip
  if(!isDrag && done) {{
    let found=false;
    for(const id of NODE_IDS) {{
      const el=$id('nd-'+id);
      if(!el) continue;
      const eR=el.getBoundingClientRect();
      const cx=eR.left-wR.left+eR.width/2, cy=eR.top-wR.top+eR.height/2;
      if(Math.hypot(mx-cx,my-cy)<eR.width/2+4) {{
        const tt=$id('tt');
        if(tt) {{
          tt.innerHTML='<b style="color:#A78BFA">'+el.dataset.role+'</b><br>'
            +'<span style="color:#9CA3AF;font-size:9.5px">'+el.dataset.desc+'</span>';
          tt.style.left=(cx+eR.width/2+8)+'px';
          tt.style.top =(cy-18)+'px';
          cls(tt,'show');
        }}
        found=true; break;
      }}
    }}
    if(!found) uncls($id('tt'),'show');
  }}
}});
window.addEventListener('mouseup',()=>{{
  if(dragId) {{ const el=$id('nd-'+dragId); if(el) el.style.cursor='grab'; }}
  isDrag=false; dragId=null;
}});

// Start
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
