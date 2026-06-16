# -*- coding: utf-8 -*-
"""Patch dashboard.py: v2 of the animated DAG with fixed edges + layout + banner."""
import sys

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

START_MARKER = '    # Animated Causal Discovery ─────────────────────────────────────────────────────'
END_MARKER   = '    # 2. Ablation Study ────────────────────────────────────────────────────────'

si = src.find(START_MARKER)
ei = src.find(END_MARKER)

# Fallback: search without unicode box-drawing chars
if si == -1:
    import re
    m = re.search(r'    # Animated Causal Discovery', src)
    if m: si = m.start()
if ei == -1:
    m = re.search(r'    # 2\. Ablation Study', src)
    if m: ei = m.start()

if si == -1 or ei == -1:
    print(f"ERROR: start={si}, end={ei}")
    sys.exit(1)

print(f"Replacing lines {src[:si].count(chr(10))+1}–{src[:ei].count(chr(10))}")

NEW_BLOCK = r'''    # Animated Causal Discovery v2 ──────────────────────────────────────────
    if dag.number_of_nodes() > 0:
        import json as _json
        import streamlit.components.v1 as _stc

        _f1   = dag_metrics.get("f1_score",  0.0)
        _prec = dag_metrics.get("precision", 0.0)
        _rec  = dag_metrics.get("recall",    0.0)

        # Classify each node
        _node_role: Dict[str, str] = {}
        for _n in dag.nodes():
            if _n == outcome_var:     _node_role[_n] = "outcome"
            elif _n == treatment_var: _node_role[_n] = "treatment"
            elif _n in confounder_set:_node_role[_n] = "confounder"
            else:                     _node_role[_n] = "mediator"

        _ROLE_COLOR  = {"outcome":"#EF4444","treatment":"#10B981",
                        "confounder":"#F59E0B","mediator":"#6C63FF"}
        _ROLE_RADIUS = {"outcome":44,"treatment":36,"confounder":38,"mediator":31}

        # ── Layout: group by role into columns ────────────────────────────
        _CW, _CH = 760, 460
        _bkt: Dict[str, list] = {
            "confounder":[],"treatment":[],"mediator":[],"outcome":[]
        }
        for _n, _r in _node_role.items():
            _bkt[_r].append(_n)

        _pos: Dict[str, Dict] = {}

        def _ys(count, cy=230, spacing=110):
            return [int(cy + (i - (count-1)/2)*spacing) for i in range(count)]

        # Confounders — far left
        for _i, _nd in enumerate(_bkt["confounder"]):
            _pos[_nd] = {"x": 95, "y": _ys(len(_bkt["confounder"]))[_i]}
        # Treatments — center-left
        for _i, _nd in enumerate(_bkt["treatment"]):
            _pos[_nd] = {"x": 255, "y": _ys(len(_bkt["treatment"]))[_i]}
        # Outcome — far right
        for _i, _nd in enumerate(_bkt["outcome"]):
            _pos[_nd] = {"x": 685, "y": _ys(len(_bkt["outcome"]))[_i]}
        # Mediators — two sub-columns 420 / 510
        _meds = _bkt["mediator"]
        _nmed = len(_meds)
        _nrows = (_nmed + 1) // 2
        _row_h = min(130, max(80, (_CH - 120) // max(_nrows, 1)))
        for _i, _nd in enumerate(_meds):
            _col = _i % 2
            _row = _i // 2
            _pos[_nd] = {
                "x": 425 + _col * 90,
                "y": max(70, min(_CH - 70, 70 + _row * _row_h)),
            }

        # ── Build label helper ─────────────────────────────────────────────
        def _node_label(name):
            words = name.replace("_", " ").title().split()
            if len(words) == 1:
                return words[0]
            if len(words) == 2:
                return words[0] + "<br>" + words[1]
            mid = (len(words) + 1) // 2
            return " ".join(words[:mid]) + "<br>" + " ".join(words[mid:])

        _ROLE_DESC = {
            "outcome":    "Primary outcome — target of all causal interventions",
            "treatment":  "Treatment variable — causal lever identified by PC algorithm",
            "confounder": "Confounder — creates spurious correlation; must be adjusted",
            "mediator":   "Direct causal driver of the outcome",
        }

        # ── JS data ────────────────────────────────────────────────────────
        _js_nodes = []
        for _n in dag.nodes():
            _r = _node_role[_n]
            _js_nodes.append({
                "id":    _n,
                "label": _node_label(_n),
                "role":  _r,
                "color": _ROLE_COLOR[_r],
                "r":     _ROLE_RADIUS[_r],
                "x":     _pos[_n]["x"],
                "y":     _pos[_n]["y"],
                "desc":  _ROLE_DESC[_r],
            })

        # Sort edges: normal first, confounding last
        _js_edges = []
        for _s, _d in dag.edges():
            _cf = (_s, _d) in confound_path_edges
            _js_edges.append({"from":_s,"to":_d,"confound":_cf,
                               "color":"#EF4444" if _cf else "#6C63FF"})
        _js_edges.sort(key=lambda e: e["confound"])

        _nd_json = _json.dumps(_js_nodes)
        _ed_json = _json.dumps(_js_edges)

        _stc.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0D1117;font-family:'Inter',-apple-system,sans-serif;overflow:hidden;}}
.wrap{{position:relative;width:760px;height:460px;margin:0 auto;}}
canvas{{position:absolute;top:0;left:0;pointer-events:none;z-index:1;}}
#nh{{position:absolute;inset:0;z-index:10;}}
.dn{{
  position:absolute;border-radius:50%;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  cursor:grab;user-select:none;
  border:2.5px solid rgba(255,255,255,0.15);
  box-shadow:0 4px 24px rgba(0,0,0,0.6);
  transform:translate(-50%,-50%) scale(0);opacity:0;
  transition:transform 0.4s cubic-bezier(0.34,1.56,0.64,1),opacity 0.3s ease;
}}
.dn.vis{{transform:translate(-50%,-50%) scale(1);opacity:1;}}
.dn:hover{{transform:translate(-50%,-50%) scale(1.1)!important;z-index:99;}}
.dn:active{{cursor:grabbing;}}
.dn.ana{{animation:ana 0.75s ease-in-out infinite;}}
@keyframes ana{{
  0%,100%{{box-shadow:0 4px 24px rgba(0,0,0,0.6),0 0 0 0 rgba(255,255,255,0.25);}}
  50%{{box-shadow:0 4px 24px rgba(0,0,0,0.6),0 0 0 14px rgba(255,255,255,0);}}
}}
.dn.cglow{{animation:cg 1.1s ease-in-out infinite;}}
@keyframes cg{{
  0%,100%{{box-shadow:0 4px 24px rgba(0,0,0,0.6),0 0 8px 2px rgba(239,68,68,0.4);}}
  50%{{box-shadow:0 4px 24px rgba(0,0,0,0.6),0 0 28px 10px rgba(239,68,68,0.75);}}
}}
.nl{{font-size:11px;font-weight:700;color:#fff;text-align:center;
     line-height:1.35;padding:0 5px;pointer-events:none;
     text-shadow:0 1px 4px rgba(0,0,0,0.9);}}
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
/* Completion banner — slides DOWN from top (not a center overlay) */
.banner{{
  position:absolute;top:0;left:50%;
  transform:translateX(-50%) translateY(-70px);
  background:rgba(3,20,10,0.97);
  border:1.5px solid #10B981;border-radius:0 0 12px 12px;
  padding:10px 22px;z-index:50;
  transition:transform 0.5s cubic-bezier(0.34,1.56,0.64,1);
  pointer-events:none;white-space:nowrap;
}}
.banner.show{{transform:translateX(-50%) translateY(0);pointer-events:all;}}
.binner{{display:flex;align-items:center;gap:12px;}}
.bcheck{{font-size:16px;color:#10B981;}}
.btitle{{font-size:11px;font-weight:700;color:#10B981;letter-spacing:0.1em;text-transform:uppercase;}}
.bf1{{font-size:22px;font-weight:800;color:#10B981;letter-spacing:-0.02em;}}
.bmeta{{font-size:11px;color:#6B7280;}}
.brp{{margin-left:10px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);
  border-radius:7px;padding:5px 12px;color:#10B981;font-size:10px;font-weight:700;
  cursor:pointer;letter-spacing:0.08em;text-transform:uppercase;}}
.brp:hover{{background:rgba(16,185,129,0.3);}}
/* Legend */
.leg{{position:absolute;bottom:8px;left:8px;display:flex;gap:12px;z-index:30;
  pointer-events:none;opacity:0;transition:opacity 0.5s;}}
.leg.show{{opacity:1;}}
.li{{display:flex;align-items:center;gap:4px;font-size:9.5px;color:#6B7280;font-weight:600;}}
.lc{{width:9px;height:9px;border-radius:50%;}}
.ll{{width:18px;height:2px;border-radius:1px;}}
/* Tooltip */
.tt{{position:absolute;background:#161B27;border:1px solid #2D3748;border-radius:8px;
  padding:7px 11px;font-size:10px;color:#E2E8F0;pointer-events:none;z-index:100;
  opacity:0;transition:opacity 0.15s;white-space:nowrap;max-width:220px;white-space:normal;}}
.tt.show{{opacity:1;}}
</style></head><body>
<div class="wrap">
  <!-- Status bar -->
  <div class="sbar">
    <div class="abadge">
      <div class="adot" id="adot"></div>
      <div class="atxt" id="atxt">PC Algorithm — Initialising</div>
    </div>
    <div class="ectr">Edges: <b id="ec">0</b>/{len(_js_edges)}</div>
  </div>
  <!-- Canvas for edges (z-index:1, below nodes) -->
  <canvas id="cv" width="760" height="460"></canvas>
  <!-- Nodes host (position:absolute;inset:0 so coords match canvas) -->
  <div id="nh"></div>
  <!-- Completion banner (slides from top) -->
  <div class="banner" id="banner">
    <div class="binner">
      <span class="bcheck">✓</span>
      <span class="btitle">Discovery Complete</span>
      <span class="bf1" id="f1d">0.000</span>
      <span class="bmeta">Precision: <b id="pvd">0.000</b> &middot; Recall: <b id="rvd">0.000</b></span>
      <button class="brp" onclick="replay()">↺ Replay</button>
    </div>
  </div>
  <!-- Legend -->
  <div class="leg" id="leg">
    <div class="li"><div class="ll" style="background:#6C63FF;"></div>Causal edge</div>
    <div class="li"><div class="ll" style="background:#EF4444;border-top:2px dashed #EF4444;height:0;"></div>Confounding</div>
    <div class="li"><div class="lc" style="background:#F59E0B;"></div>Confounder</div>
    <div class="li"><div class="lc" style="background:#10B981;"></div>Treatment</div>
    <div class="li"><div class="lc" style="background:#6C63FF;"></div>Mediator</div>
    <div class="li"><div class="lc" style="background:#EF4444;"></div>Outcome</div>
  </div>
  <!-- Tooltip -->
  <div class="tt" id="tt"></div>
</div>
<script>
const NODES_DATA = {_nd_json};
const EDGES_DATA = {_ed_json};
const F1_VAL = {_f1:.3f};
const PR_VAL = {_prec:.3f};
const RC_VAL = {_rec:.3f};

const cv  = document.getElementById('cv');
const ctx = cv.getContext('2d');
const nh  = document.getElementById('nh');

// Build DOM nodes
NODES_DATA.forEach(n => {{
  const el = document.createElement('div');
  el.className = 'dn';
  el.id = 'nd-' + n.id;
  el.dataset.nid   = n.id;
  el.dataset.role  = n.role;
  el.dataset.desc  = n.desc;
  el.dataset.color = n.color;
  const sz = n.r * 2;
  el.style.cssText = 'left:'+n.x+'px;top:'+n.y+'px;width:'+sz+'px;height:'+sz+'px;'
    + 'background:radial-gradient(circle at 35% 35%,'+n.color+'EE,'+n.color+','+n.color+'AA);';
  el.innerHTML = '<div class="nl">' + n.label + '</div>';
  nh.appendChild(el);
}});

// ── DOM-position reading (fixes canvas↔DOM coordinate mismatch) ──────────────
function getPos(nid) {{
  const wrap = document.querySelector('.wrap');
  const wR   = wrap.getBoundingClientRect();
  const el   = document.getElementById('nd-' + nid);
  if (!el || !el.classList.contains('vis')) return null;
  const eR = el.getBoundingClientRect();
  return {{
    x: eR.left - wR.left + eR.width  / 2,
    y: eR.top  - wR.top  + eR.height / 2,
    r: eR.width / 2,
  }};
}}

let drawnEdges = [], parts = [], ecnt = 0, done = false;

function h2r(h, a) {{
  const r=parseInt(h.slice(1,3),16), g=parseInt(h.slice(3,5),16), b=parseInt(h.slice(5,7),16);
  return 'rgba('+r+','+g+','+b+','+a+')';
}}

function drawCanvas() {{
  ctx.clearRect(0, 0, 760, 460);

  // ── Edges ──────────────────────────────────────────────────────────────────
  drawnEdges.forEach(e => {{
    const f = getPos(e.from);
    const t = getPos(e.to);
    if (!f || !t) return;

    const ang  = Math.atan2(t.y - f.y, t.x - f.x);
    const sx   = f.x + Math.cos(ang) * (f.r + 2);
    const sy   = f.y + Math.sin(ang) * (f.r + 2);
    const ex   = t.x - Math.cos(ang) * (t.r + 5);
    const ey   = t.y - Math.sin(ang) * (t.r + 5);

    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey);
    if (e.confound) {{
      ctx.setLineDash([8, 5]);
      ctx.strokeStyle = '#EF4444';
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#EF4444';
      ctx.shadowBlur = e.glow ? 18 : 3;
    }} else {{
      ctx.setLineDash([]);
      ctx.strokeStyle = h2r(e.color, 0.8);
      ctx.lineWidth = 2;
      ctx.shadowBlur = 0;
    }}
    ctx.stroke();
    ctx.shadowBlur = 0; ctx.setLineDash([]);

    // Arrowhead
    ctx.beginPath();
    ctx.moveTo(ex, ey);
    ctx.lineTo(ex - 11*Math.cos(ang-0.38), ey - 11*Math.sin(ang-0.38));
    ctx.lineTo(ex - 11*Math.cos(ang+0.38), ey - 11*Math.sin(ang+0.38));
    ctx.closePath();
    ctx.fillStyle = e.confound ? (e.glow ? '#EF4444' : '#EF444466') : h2r(e.color, 0.65);
    ctx.fill();
  }});

  // ── Spark particles ────────────────────────────────────────────────────────
  parts = parts.filter(p => p.life > 0);
  parts.forEach(p => {{
    p.x += p.vx; p.y += p.vy; p.vy += 0.1; p.life -= 2;
    const a = p.life / p.ml;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.sz * a, 0, Math.PI*2);
    ctx.fillStyle = p.c + Math.floor(a*255).toString(16).padStart(2,'0');
    ctx.fill();
  }});
}}

function sparks(x, y, c, n) {{
  for (let i = 0; i < n; i++) {{
    const ang = (Math.PI*2/n)*i, sp = 1.5 + Math.random()*2.5;
    parts.push({{x,y,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp-1,
      life:40+Math.random()*25,ml:65,sz:2+Math.random()*2,c}});
  }}
}}

function showNode(nid, delay) {{
  setTimeout(() => {{
    const el = document.getElementById('nd-' + nid);
    if (el) el.classList.add('vis');
    // Sparks at initial CSS position (before DOM reflowing)
    const n = NODES_DATA.find(n => n.id === nid);
    if (n) sparks(n.x, n.y, n.color, 8);
  }}, delay);
}}

function addEdge(ei) {{
  const e = EDGES_DATA[ei];
  drawnEdges.push({{...e, glow:false}});
  ecnt++;
  document.getElementById('ec').textContent = ecnt;
  // Sparks at destination DOM position
  const tp = getPos(e.to);
  if (tp) sparks(tp.x, tp.y, e.color, e.confound ? 22 : 12);
  // Glow confounding nodes
  if (e.confound) {{
    [e.from, e.to].forEach(nid => {{
      const el = document.getElementById('nd-' + nid);
      if (el) el.classList.add('cglow');
    }});
  }}
}}

function animCtr(id, target, dur, dec) {{
  const el = document.getElementById(id);
  const t0 = Date.now();
  (function tick() {{
    const p = Math.min((Date.now()-t0)/dur, 1);
    const v = p < 0.5 ? 2*p*p : -1+(4-2*p)*p;
    el.textContent = (v * target).toFixed(dec);
    if (p < 1) requestAnimationFrame(tick);
    else el.textContent = target.toFixed(dec);
  }})();
}}

let timers = [];
function clearTimers() {{ timers.forEach(clearTimeout); timers = []; }}

function startAnim() {{
  clearTimers();
  done = false; drawnEdges = []; parts = []; ecnt = 0;
  document.getElementById('ec').textContent = '0';
  document.getElementById('banner').classList.remove('show');
  document.getElementById('leg').classList.remove('show');
  document.getElementById('atxt').textContent = 'PC Algorithm — Initialising';
  document.getElementById('adot').style.background = '#6C63FF';

  // Reset nodes
  NODES_DATA.forEach(n => {{
    const el = document.getElementById('nd-' + n.id);
    if (!el) return;
    el.classList.remove('vis','ana','cglow');
    el.style.left = n.x + 'px';
    el.style.top  = n.y + 'px';
  }});

  // Phase 1 — nodes appear one by one
  NODES_DATA.forEach((n, i) => {{
    timers.push(setTimeout(() => showNode(n.id, 0), 200 + i * 200));
  }});

  // Phase 2 — analysis pulsing
  const p2 = 200 + NODES_DATA.length * 200 + 300;
  timers.push(setTimeout(() => {{
    document.getElementById('atxt').textContent = 'PC Algorithm — Running Independence Tests';
    NODES_DATA.forEach(n => {{
      const el = document.getElementById('nd-' + n.id);
      if (el) el.classList.add('ana');
    }});
  }}, p2));

  // Phase 3 — edges appear
  const p3 = p2 + 1500;
  const step = 600;
  const nNormal = EDGES_DATA.filter(e => !e.confound).length;
  EDGES_DATA.forEach((e, i) => {{
    timers.push(setTimeout(() => {{
      if (i === 0) {{
        NODES_DATA.forEach(n => {{
          const el = document.getElementById('nd-' + n.id);
          if (el) el.classList.remove('ana');
        }});
        document.getElementById('atxt').textContent = 'PC Algorithm — Orienting Edges';
      }}
      if (i === nNormal) {{
        document.getElementById('atxt').textContent = 'Identifying Confounding Paths…';
      }}
      addEdge(i);
    }}, p3 + i * step));
  }});

  // Phase 4 — confounding glow
  const p4 = p3 + EDGES_DATA.length * step + 500;
  timers.push(setTimeout(() => {{
    drawnEdges.forEach(e => {{ if (e.confound) e.glow = true; }});
    document.getElementById('atxt').textContent =
      'Confounding Path Identified — Backdoor Criterion Applied';
  }}, p4));

  // Phase 5 — complete banner
  const p5 = p4 + 1500;
  timers.push(setTimeout(() => {{
    document.getElementById('banner').classList.add('show');
    document.getElementById('leg').classList.add('show');
    animCtr('f1d', F1_VAL, 1400, 3);
    animCtr('pvd', PR_VAL, 1200, 3);
    animCtr('rvd', RC_VAL, 1200, 3);
    document.getElementById('adot').style.background = '#10B981';
    document.getElementById('atxt').textContent =
      'Discovery Complete — F1 ' + F1_VAL.toFixed(3);
    done = true;
  }}, p5));
}}

function replay() {{
  document.getElementById('banner').classList.remove('show');
  timers.push(setTimeout(startAnim, 300));
}}

// ── Drag (enabled after animation) ────────────────────────────────────────────
let isDrag = false, dragId = null, dox = 0, doy = 0;
const wrap = document.querySelector('.wrap');

wrap.addEventListener('mousedown', e => {{
  if (!done) return;
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX - wR.left, my = e.clientY - wR.top;
  for (const n of NODES_DATA) {{
    const p = getPos(n.id);
    if (p && Math.hypot(mx - p.x, my - p.y) < p.r + 6) {{
      isDrag = true; dragId = n.id; dox = mx - p.x; doy = my - p.y;
      const el = document.getElementById('nd-' + n.id);
      if (el) el.style.cursor = 'grabbing';
      break;
    }}
  }}
}});

window.addEventListener('mousemove', e => {{
  const wR = wrap.getBoundingClientRect();
  const mx = e.clientX - wR.left, my = e.clientY - wR.top;

  if (isDrag && dragId) {{
    const el = document.getElementById('nd-' + dragId);
    if (el) {{ el.style.left = (mx - dox) + 'px'; el.style.top = (my - doy) + 'px'; }}
  }}

  if (!isDrag && done) {{
    let found = false;
    for (const n of NODES_DATA) {{
      const p = getPos(n.id);
      if (p && Math.hypot(mx - p.x, my - p.y) < p.r + 4) {{
        const el = document.getElementById('nd-' + n.id);
        const tt = document.getElementById('tt');
        if (tt && el) {{
          tt.innerHTML = '<b style="color:'+n.color+'">' + el.dataset.role + '</b><br>'
            + el.dataset.desc;
          tt.style.left = (p.x + p.r + 8) + 'px';
          tt.style.top  = (p.y - 20) + 'px';
          tt.classList.add('show');
        }}
        found = true; break;
      }}
    }}
    if (!found) document.getElementById('tt').classList.remove('show');
  }}
}});

window.addEventListener('mouseup', () => {{
  if (dragId) {{
    const el = document.getElementById('nd-' + dragId);
    if (el) el.style.cursor = 'grab';
  }}
  isDrag = false; dragId = null;
}});

// ── Render loop ────────────────────────────────────────────────────────────────
(function loop() {{ drawCanvas(); requestAnimationFrame(loop); }})();
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
        _leg_html = "".join(
            f'<span style="display:inline-flex;align-items:center;gap:5px;margin:0 14px 6px 0;">'
            f'<span style="width:10px;height:10px;border-radius:50%;'
            f'background:{_c};display:inline-block;"></span>'
            f'<span style="font-size:0.78rem;color:{MUTED};">{_lbl}</span></span>'
            for _c, _lbl in _dag_legend_items
        )
        st.markdown(
            f'<div style="margin-top:6px;padding:8px 16px;background:{CARD};'
            f'border:1px solid {BORDER};border-radius:8px;display:flex;flex-wrap:wrap;">'
            f"{_leg_html}</div>",
            unsafe_allow_html=True,
        )

'''

out = src[:si] + NEW_BLOCK + src[ei:]

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Done — file is now {len(out):,} chars.")
