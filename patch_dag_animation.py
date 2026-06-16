# -*- coding: utf-8 -*-
"""Patch dashboard.py: replace agraph DAG with live animated causal discovery."""
import sys

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

START_MARKER = '    # agraph DAG (CausalNex-inspired: nodes labelled, edges coloured) ──────────'
END_MARKER   = '    # 2. Ablation Study ────────────────────────────────────────────────────────'

si = src.find(START_MARKER)
ei = src.find(END_MARKER)
if si == -1 or ei == -1:
    print("ERROR: markers not found")
    print("START found:", si != -1, "| END found:", ei != -1)
    sys.exit(1)

print(f"Replacing lines {src[:si].count(chr(10))+1}–{src[:ei].count(chr(10))}")

# NEW_BLOCK uses r'''...''' so inner f""" triple-quotes don't conflict
NEW_BLOCK = r'''    # Animated Causal Discovery ─────────────────────────────────────────────
    if dag.number_of_nodes() > 0:
        import json as _json
        import streamlit.components.v1 as _stc

        _f1   = dag_metrics.get("f1_score",  0.0)
        _prec = dag_metrics.get("precision", 0.0)
        _rec  = dag_metrics.get("recall",    0.0)

        # Classify nodes by role
        _node_role: Dict[str, str] = {}
        for _n in dag.nodes():
            if _n == outcome_var:
                _node_role[_n] = "outcome"
            elif _n == treatment_var:
                _node_role[_n] = "treatment"
            elif _n in confounder_set:
                _node_role[_n] = "confounder"
            else:
                _node_role[_n] = "mediator"

        _ROLE_COLOR = {
            "outcome":    "#EF4444",
            "treatment":  "#10B981",
            "confounder": "#F59E0B",
            "mediator":   "#6C63FF",
        }
        _ROLE_RADIUS = {
            "outcome": 42, "treatment": 32,
            "confounder": 34, "mediator": 28,
        }
        _ROLE_DESC = {
            "outcome":    "Primary outcome — target of all causal policy interventions",
            "treatment":  "Treatment variable — direct causal lever identified by PC algorithm",
            "confounder": "Confounder — creates spurious correlation; blocked by adjustment",
            "mediator":   "Direct causal driver of the outcome",
        }

        # Compute canvas positions
        _CW, _CH = 760, 450
        _buckets: Dict[str, list] = {
            "confounder": [], "treatment": [], "mediator": [], "outcome": []
        }
        for _n, _r in _node_role.items():
            _buckets[_r].append(_n)

        _X_COLS = {"confounder": 90, "treatment": 250, "mediator": 460, "outcome": 660}
        _pos: Dict[str, Dict] = {}
        for _role, _nodes in _buckets.items():
            _cx = _X_COLS[_role]
            _n  = len(_nodes)
            for _i, _nd in enumerate(_nodes):
                _pos[_nd] = {
                    "x": _cx + (_i % 2) * 60,
                    "y": int(_CH / (_n + 1) * (_i + 1)) + (_i % 2) * 30,
                }

        # Build JS-ready node list
        _js_nodes = []
        for _n in dag.nodes():
            _r    = _node_role[_n]
            _lbl  = _n.replace("_", " ").title()
            _lbl2 = (_lbl[:11] + "..") if len(_lbl) > 13 else _lbl
            _js_nodes.append({
                "id": _n, "label": _lbl2, "fullLabel": _lbl,
                "role": _r, "color": _ROLE_COLOR[_r],
                "r": _ROLE_RADIUS[_r],
                "x": _pos[_n]["x"], "y": _pos[_n]["y"],
                "desc": _ROLE_DESC[_r],
            })

        # Sort edges: normal first, confounding last (so they animate last)
        _js_edges = []
        for _s, _d in dag.edges():
            _cf = (_s, _d) in confound_path_edges
            _js_edges.append({
                "from": _s, "to": _d,
                "confound": _cf,
                "color": "#EF4444" if _cf else "#6C63FF",
            })
        _js_edges.sort(key=lambda e: e["confound"])

        _nd_json = _json.dumps(_js_nodes)
        _ed_json = _json.dumps(_js_edges)

        _stc.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0D1117;font-family:'Inter',-apple-system,sans-serif;overflow:hidden;}}
.wrap{{position:relative;width:760px;height:490px;margin:0 auto;}}
canvas{{position:absolute;top:0;left:0;pointer-events:none;}}
.dn{{
  position:absolute;border-radius:50%;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:grab;
  transform:translate(-50%,-50%) scale(0);opacity:0;
  transition:transform 0.4s cubic-bezier(0.34,1.56,0.64,1),opacity 0.3s ease;
  z-index:10;border:2px solid rgba(255,255,255,0.15);
  box-shadow:0 4px 20px rgba(0,0,0,0.5);user-select:none;
}}
.dn.vis{{transform:translate(-50%,-50%) scale(1);opacity:1;}}
.dn:hover{{transform:translate(-50%,-50%) scale(1.12)!important;z-index:20;}}
.dn:active{{cursor:grabbing;}}
.dn.ana{{animation:ana 0.7s ease-in-out infinite;}}
@keyframes ana{{
  0%,100%{{box-shadow:0 0 0 0 rgba(255,255,255,0.3);}}
  50%{{box-shadow:0 0 0 14px rgba(255,255,255,0);}}
}}
.dn.cglow{{animation:cg 1s ease-in-out infinite;}}
@keyframes cg{{
  0%,100%{{box-shadow:0 0 8px 2px rgba(239,68,68,0.4);}}
  50%{{box-shadow:0 0 28px 10px rgba(239,68,68,0.7);}}
}}
.nl{{font-size:10px;font-weight:700;color:#fff;text-align:center;
     line-height:1.3;padding:0 4px;pointer-events:none;text-shadow:0 1px 3px rgba(0,0,0,0.9);}}
.sbar{{position:absolute;top:8px;left:8px;right:8px;display:flex;
  align-items:center;justify-content:space-between;z-index:30;pointer-events:none;}}
.abadge{{display:flex;align-items:center;gap:7px;
  background:rgba(108,99,255,0.13);border:1px solid rgba(108,99,255,0.3);
  border-radius:20px;padding:4px 12px;}}
.adot{{width:6px;height:6px;border-radius:50%;background:#6C63FF;animation:blink 0.9s infinite;}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:0.15;}}}}
.atxt{{font-size:10px;font-weight:700;color:#A78BFA;letter-spacing:0.08em;text-transform:uppercase;}}
.ectr{{background:rgba(13,17,23,0.9);border:1px solid #1E2433;
  border-radius:8px;padding:4px 12px;font-size:11px;color:#6B7280;}}
.ectr b{{color:#6C63FF;font-weight:700;}}
.overlay{{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%) scale(0);opacity:0;
  background:linear-gradient(135deg,#1E1B4B,#0D1117);
  border:2px solid #6C63FF;border-radius:16px;padding:22px 38px;
  text-align:center;z-index:50;pointer-events:none;
  transition:all 0.5s cubic-bezier(0.34,1.56,0.64,1);
  box-shadow:0 0 60px rgba(108,99,255,0.3);
}}
.overlay.show{{transform:translate(-50%,-50%) scale(1);opacity:1;}}
.otitle{{font-size:11px;font-weight:700;color:#A78BFA;letter-spacing:0.15em;
  text-transform:uppercase;margin-bottom:6px;}}
.oscore{{font-size:44px;font-weight:800;color:#10B981;letter-spacing:-0.04em;line-height:1;}}
.osub{{font-size:11px;color:#6B7280;margin-top:3px;}}
.ometa{{margin-top:10px;display:flex;gap:20px;justify-content:center;}}
.omv{{font-size:11px;color:#6B7280;}}
.omv b{{color:#E2E8F0;font-weight:700;}}
.rbtn{{margin-top:12px;background:rgba(108,99,255,0.2);border:1px solid rgba(108,99,255,0.4);
  border-radius:8px;padding:5px 14px;color:#A78BFA;font-size:10px;font-weight:700;
  cursor:pointer;pointer-events:all;letter-spacing:0.08em;text-transform:uppercase;}}
.rbtn:hover{{background:rgba(108,99,255,0.4);}}
.leg{{position:absolute;bottom:8px;left:8px;display:flex;gap:14px;z-index:20;
  pointer-events:none;opacity:0;transition:opacity 0.5s;}}
.leg.show{{opacity:1;}}
.li{{display:flex;align-items:center;gap:5px;font-size:9px;color:#6B7280;font-weight:600;}}
.lline{{width:20px;height:2px;border-radius:1px;}}
.tt{{position:absolute;background:#161B27;border:1px solid #2D3748;
  border-radius:8px;padding:7px 11px;font-size:10px;color:#E2E8F0;
  pointer-events:none;z-index:100;opacity:0;transition:opacity 0.15s;
  white-space:nowrap;}}
.tt.show{{opacity:1;}}
</style></head><body>
<div class="wrap">
  <div class="sbar">
    <div class="abadge">
      <div class="adot" id="adot"></div>
      <div class="atxt" id="atxt">PC Algorithm — Initialising</div>
    </div>
    <div class="ectr">Edges: <b id="ec">0</b>/{len(_js_edges)}</div>
  </div>
  <canvas id="cv" width="760" height="490"></canvas>
  <div id="nodes-host"></div>
  <div class="overlay" id="ov">
    <div class="otitle">Discovery Complete</div>
    <div class="oscore" id="f1d">0.000</div>
    <div class="osub">F1 Score — Causal Structure Recovered</div>
    <div class="ometa">
      <div class="omv">Precision <b id="pvd">0.000</b></div>
      <div class="omv">Recall <b id="rvd">0.000</b></div>
    </div>
    <button class="rbtn" onclick="replay()">&#8635; Replay</button>
  </div>
  <div class="leg" id="leg">
    <div class="li"><div class="lline" style="background:#6C63FF;"></div>Causal edge</div>
    <div class="li"><div class="lline" style="background:#EF4444;border-top:2px dashed #EF4444;height:0;"></div>Confounding</div>
    <div class="li"><div style="width:9px;height:9px;border-radius:50%;background:#F59E0B;"></div>Confounder</div>
    <div class="li"><div style="width:9px;height:9px;border-radius:50%;background:#10B981;"></div>Treatment</div>
    <div class="li"><div style="width:9px;height:9px;border-radius:50%;background:#EF4444;"></div>Outcome</div>
  </div>
  <div class="tt" id="tt"></div>
</div>
<script>
const NODES_DATA = {_nd_json};
const EDGES_DATA = {_ed_json};
const F1_VAL  = {_f1:.3f};
const PR_VAL  = {_prec:.3f};
const RC_VAL  = {_rec:.3f};

const cv  = document.getElementById('cv');
const ctx = cv.getContext('2d');
const host= document.getElementById('nodes-host');

// Build mutable node state from data
const NM = {{}};  // id -> node state
NODES_DATA.forEach(n => {{
  NM[n.id] = {{...n}};
}});

// Create DOM nodes
NODES_DATA.forEach(n => {{
  const el = document.createElement('div');
  el.className = 'dn';
  el.id = 'nd-' + n.id;
  el.style.cssText = [
    'left:' + n.x + 'px',
    'top:'  + n.y + 'px',
    'width:'  + (n.r*2) + 'px',
    'height:' + (n.r*2) + 'px',
    'background:radial-gradient(circle at 35% 35%,' + n.color + 'EE,' + n.color + ',' + n.color + 'BB)',
  ].join(';');
  el.dataset.role = n.role;
  el.dataset.desc = n.desc;
  el.dataset.nid  = n.id;
  el.innerHTML = '<div class="nl">' + n.label.replace(' ','<br>') + '</div>';
  host.appendChild(el);
}});

let drawnEdges=[], parts=[], ecnt=0, done=false;
let isDrag=false, dragId=null, dox=0, doy=0;

function hex2rgba(h,a){{
  const ri=parseInt(h.slice(1,3),16),gi=parseInt(h.slice(3,5),16),bi=parseInt(h.slice(5,7),16);
  return 'rgba('+ri+','+gi+','+bi+','+a+')';
}}

function drawAll(){{
  ctx.clearRect(0,0,760,490);
  drawnEdges.forEach(e=>{{
    const f=NM[e.from], t=NM[e.to];
    if(!f||!t)return;
    ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(t.x,t.y);
    if(e.confound){{
      ctx.setLineDash([8,5]);
      ctx.strokeStyle=e.color;
      ctx.lineWidth=2.5;
      ctx.shadowColor='#EF4444';
      ctx.shadowBlur=e.glow?16:4;
    }} else {{
      ctx.setLineDash([]);
      ctx.strokeStyle=hex2rgba(e.color,0.75);
      ctx.lineWidth=2;
      ctx.shadowBlur=0;
    }}
    ctx.stroke();
    ctx.shadowBlur=0;ctx.setLineDash([]);
    const ang=Math.atan2(t.y-f.y,t.x-f.x);
    const ax=t.x-Math.cos(ang)*(t.r+4),ay=t.y-Math.sin(ang)*(t.r+4);
    ctx.beginPath();
    ctx.moveTo(ax,ay);
    ctx.lineTo(ax-11*Math.cos(ang-0.38),ay-11*Math.sin(ang-0.38));
    ctx.lineTo(ax-11*Math.cos(ang+0.38),ay-11*Math.sin(ang+0.38));
    ctx.closePath();
    ctx.fillStyle=e.confound?(e.glow?'#EF4444':'#EF444466'):hex2rgba(e.color,0.6);
    ctx.fill();
  }});

  parts=parts.filter(p=>p.life>0);
  parts.forEach(p=>{{
    p.x+=p.vx;p.y+=p.vy;p.vy+=0.08;p.life-=2;
    ctx.beginPath();ctx.arc(p.x,p.y,p.sz*(p.life/p.ml),0,Math.PI*2);
    const al=Math.floor(p.life/p.ml*255).toString(16).padStart(2,'0');
    ctx.fillStyle=p.c+al;ctx.fill();
  }});
}}

function sparks(x,y,c,n){{
  for(let i=0;i<n;i++){{
    const a=(Math.PI*2/n)*i, sp=1.5+Math.random()*2.5;
    parts.push({{x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-1,
      life:40+Math.random()*25,ml:65,sz:2+Math.random()*2,c}});
  }}
}}

function showNode(nid,delay){{
  setTimeout(()=>{{
    const el=document.getElementById('nd-'+nid);
    if(el)el.classList.add('vis');
    const n=NM[nid];
    if(n)sparks(n.x,n.y,n.color,8);
  }},delay);
}}

function drawEdge(ei){{
  const e=EDGES_DATA[ei];
  drawnEdges.push({{...e,glow:false}});
  ecnt++;
  document.getElementById('ec').textContent=ecnt;
  const t=NM[e.to];
  if(t)sparks(t.x,t.y,e.color,e.confound?22:12);
  if(e.confound){{
    [e.from,e.to].forEach(nid=>{{
      const el=document.getElementById('nd-'+nid);
      if(el)el.classList.add('cglow');
    }});
  }}
}}

function animCounter(elId,target,dur,decimals){{
  const el=document.getElementById(elId);
  const st=Date.now();
  function upd(){{
    const p=Math.min((Date.now()-st)/dur,1);
    const v=(-1+(4-2*p)*p)*target;  // ease-in-out
    el.textContent=(p<0.5?2*p*p*target:v).toFixed(decimals);
    if(p<1)requestAnimationFrame(upd);
    else el.textContent=target.toFixed(decimals);
  }}
  upd();
}}

let animTimer=[];
function clearTimers(){{animTimer.forEach(clearTimeout);animTimer=[];}}

function startAnim(){{
  clearTimers();
  done=false;drawnEdges=[];parts=[];ecnt=0;
  document.getElementById('ec').textContent='0';
  document.getElementById('ov').classList.remove('show');
  document.getElementById('leg').classList.remove('show');
  document.getElementById('atxt').textContent='PC Algorithm — Initialising';
  document.getElementById('adot').style.background='#6C63FF';

  // Hide + reset all nodes
  NODES_DATA.forEach(n=>{{
    const el=document.getElementById('nd-'+n.id);
    if(el){{el.classList.remove('vis','ana','cglow');}}
    NM[n.id].x=n.x;NM[n.id].y=n.y;
    if(el){{el.style.left=n.x+'px';el.style.top=n.y+'px';}}
  }});

  // Phase 1: nodes appear
  NODES_DATA.forEach((n,i)=>{{
    animTimer.push(setTimeout(()=>showNode(n.id,0),300+i*220));
  }});

  // Phase 2: analysing
  animTimer.push(setTimeout(()=>{{
    document.getElementById('atxt').textContent='PC Algorithm — Running Independence Tests';
    NODES_DATA.forEach(n=>{{
      const el=document.getElementById('nd-'+n.id);
      if(el)el.classList.add('ana');
    }});
  }},2200));

  // Phase 3: draw edges
  const baseDelay=3800;
  const stepMs=620;
  const confStart=EDGES_DATA.filter(e=>!e.confound).length;

  EDGES_DATA.forEach((e,i)=>{{
    animTimer.push(setTimeout(()=>{{
      if(i===0){{
        NODES_DATA.forEach(n=>{{
          const el=document.getElementById('nd-'+n.id);
          if(el)el.classList.remove('ana');
        }});
        document.getElementById('atxt').textContent='PC Algorithm — Orienting Edges';
      }}
      if(i===confStart){{
        document.getElementById('atxt').textContent='Identifying Confounding Paths...';
      }}
      drawEdge(i);
    }},baseDelay+i*stepMs));
  }});

  // Phase 4: confounding glow
  const glowTime=baseDelay+EDGES_DATA.length*stepMs+600;
  animTimer.push(setTimeout(()=>{{
    drawnEdges.forEach(e=>{{if(e.confound)e.glow=true;}});
    document.getElementById('atxt').textContent='Confounding Path Identified — Backdoor Criterion Applied';
  }},glowTime));

  // Phase 5: complete
  const doneTime=glowTime+1800;
  animTimer.push(setTimeout(()=>{{
    document.getElementById('ov').classList.add('show');
    document.getElementById('leg').classList.add('show');
    animCounter('f1d', F1_VAL, 1400, 3);
    animCounter('pvd', PR_VAL, 1200, 3);
    animCounter('rvd', RC_VAL, 1200, 3);
    document.getElementById('adot').style.background='#10B981';
    document.getElementById('atxt').textContent='Discovery Complete — F1: '+F1_VAL.toFixed(3);
    done=true;
  }},doneTime));
}}

function replay(){{
  document.getElementById('ov').classList.remove('show');
  animTimer.push(setTimeout(startAnim,300));
}}

// Drag
const wrap=document.querySelector('.wrap');
wrap.addEventListener('mousedown',e=>{{
  if(!done)return;
  const rc=wrap.getBoundingClientRect();
  const mx=e.clientX-rc.left, my=e.clientY-rc.top;
  for(const n of Object.values(NM)){{
    if(Math.hypot(mx-n.x,my-n.y)<n.r+8){{
      isDrag=true;dragId=n.id;dox=mx-n.x;doy=my-n.y;
      const el=document.getElementById('nd-'+n.id);
      if(el)el.style.cursor='grabbing';
      break;
    }}
  }}
}});
window.addEventListener('mousemove',e=>{{
  const rc=wrap.getBoundingClientRect();
  const mx=e.clientX-rc.left, my=e.clientY-rc.top;
  if(isDrag&&dragId){{
    NM[dragId].x=mx-dox;NM[dragId].y=my-doy;
    const el=document.getElementById('nd-'+dragId);
    if(el){{el.style.left=NM[dragId].x+'px';el.style.top=NM[dragId].y+'px';}}
  }}
  if(!isDrag&&done){{
    let found=false;
    for(const n of Object.values(NM)){{
      if(Math.hypot(mx-n.x,my-n.y)<n.r+5){{
        const nl=document.getElementById('nd-'+n.id);
        const tt=document.getElementById('tt');
        if(tt){{
          tt.textContent=(nl?nl.dataset.role:'')+'  —  '+(nl?nl.dataset.desc:'');
          tt.style.left=(n.x+n.r+8)+'px';tt.style.top=(n.y-16)+'px';
          tt.classList.add('show');
        }}
        found=true;break;
      }}
    }}
    if(!found)document.getElementById('tt').classList.remove('show');
  }}
}});
window.addEventListener('mouseup',()=>{{
  if(dragId){{const el=document.getElementById('nd-'+dragId);if(el)el.style.cursor='grab';}}
  isDrag=false;dragId=null;
}});

function loop(){{drawAll();requestAnimationFrame(loop);}}
loop();
setTimeout(startAnim,400);
</script></body></html>""", height=510)

        # Static legend strip below animation
        _dag_legend_items = [
            (SUCCESS, "Treatment"),
            (ERROR,   "Outcome"),
            (WARNING, "Confounder"),
            (PRIMARY, "Other"),
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
