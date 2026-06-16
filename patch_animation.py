# -*- coding: utf-8 -*-
"""Patch dashboard.py: replace agraph section with live canvas animation."""
import sys

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

START_MARKER = '        with _col_graph:'
END_MARKER   = '        with _col_stats:'

si = src.find(START_MARKER)
ei = src.find(END_MARKER)
if si == -1 or ei == -1:
    print("ERROR: markers not found"); sys.exit(1)

print(f"Replacing lines {src[:si].count(chr(10))+1}–{src[:ei].count(chr(10))}")

# Use r''' to avoid clashing with inner f""" triple-quotes
NEW_BLOCK = r'''        with _col_graph:
            import streamlit.components.v1 as _stc

            _ac  = _type_n.get("Case",             0)
            _am  = _type_n.get("Resource_Machine", 0)
            _aw  = _type_n.get("Resource_Worker",  0)
            _art = _type_n.get("Artifact",         0)
            _ao  = _type_n.get("Outcome",          0)

            _lbl_case     = _role_label.get("Case",             "Case")
            _lbl_machine  = _role_label.get("Resource_Machine", "Machine")
            _lbl_worker   = _role_label.get("Resource_Worker",  "Worker")
            _lbl_material = _role_label.get("Artifact",         "Material")
            _lbl_outcome  = _role_label.get("Outcome",          "Outcome")

            _sub_case    = "patients" if domain == "healthcare" else "orders"
            _sub_machine = "wards"    if domain == "healthcare" else "units"
            _sub_worker  = "clinicians" if domain == "healthcare" else "staff"

            _stc.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0D1117;font-family:'Inter',-apple-system,sans-serif;overflow:hidden;}}
.wrap{{position:relative;width:680px;height:420px;margin:0 auto;}}
canvas{{position:absolute;top:0;left:0;}}
.node{{position:absolute;border-radius:50%;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:pointer;
  transition:transform 0.2s;transform:translate(-50%,-50%);z-index:10;
  border:2px solid rgba(255,255,255,0.12);box-shadow:0 4px 20px rgba(0,0,0,0.5);}}
.node:hover{{transform:translate(-50%,-50%) scale(1.15);}}
.node.pulse{{animation:pulse 0.5s ease-out;}}
@keyframes pulse{{
  0%{{box-shadow:0 0 0 0 rgba(255,255,255,0.5);}}
  70%{{box-shadow:0 0 0 22px rgba(255,255,255,0);}}
  100%{{box-shadow:0 0 0 0 rgba(255,255,255,0);}}
}}
.nlbl{{font-size:11px;font-weight:700;color:#fff;text-align:center;line-height:1.2;}}
.nctr{{font-size:14px;font-weight:800;color:#fff;margin-top:2px;font-variant-numeric:tabular-nums;}}
.nsub{{font-size:9px;color:rgba(255,255,255,0.5);margin-top:1px;text-align:center;}}
.badge{{position:absolute;top:10px;right:10px;display:flex;align-items:center;gap:5px;
  background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);
  border-radius:20px;padding:4px 10px;z-index:20;}}
.bdot{{width:6px;height:6px;border-radius:50%;background:#10B981;animation:blink 1s infinite;}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:0.2;}}}}
.btxt{{font-size:10px;font-weight:700;color:#10B981;letter-spacing:0.1em;text-transform:uppercase;}}
.sbar{{position:absolute;bottom:8px;left:8px;right:8px;display:flex;
  justify-content:space-between;z-index:20;}}
.spill{{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
  border-radius:20px;padding:3px 10px;font-size:10px;color:rgba(255,255,255,0.4);}}
.spill b{{color:#fff;font-weight:700;}}
</style></head><body>
<div class="wrap">
  <div class="badge"><div class="bdot"></div><div class="btxt">Live Simulation</div></div>
  <canvas id="cv" width="680" height="420"></canvas>
  <div class="node" id="n-case"
       style="left:80px;top:210px;width:78px;height:78px;
              background:linear-gradient(135deg,#7C3AED,#6C63FF);">
    <div class="nlbl">{_lbl_case}</div>
    <div class="nctr" id="cnt-case">0</div>
    <div class="nsub">{_ac:,} {_sub_case}</div>
  </div>
  <div class="node" id="n-material"
       style="left:268px;top:88px;width:62px;height:62px;
              background:linear-gradient(135deg,#6D28D9,#A78BFA);">
    <div class="nlbl">{_lbl_material}</div>
    <div class="nsub">{_art} types</div>
  </div>
  <div class="node" id="n-machine"
       style="left:360px;top:210px;width:78px;height:78px;
              background:linear-gradient(135deg,#B45309,#F59E0B);">
    <div class="nlbl">{_lbl_machine}</div>
    <div class="nctr" id="cnt-machine">0</div>
    <div class="nsub">{_am} {_sub_machine}</div>
  </div>
  <div class="node" id="n-worker"
       style="left:360px;top:332px;width:64px;height:64px;
              background:linear-gradient(135deg,#065F46,#10B981);">
    <div class="nlbl">{_lbl_worker}</div>
    <div class="nsub">{_aw} {_sub_worker}</div>
  </div>
  <div class="node" id="n-outcome"
       style="left:600px;top:210px;width:78px;height:78px;
              background:linear-gradient(135deg,#991B1B,#EF4444);">
    <div class="nlbl">{_lbl_outcome}</div>
    <div class="nctr" id="cnt-outcome">0</div>
    <div class="nsub">{_ao:,} results</div>
  </div>
  <div class="sbar">
    <div class="spill">Types: <b>5</b></div>
    <div class="spill">Active: <b id="aflows">0</b></div>
    <div class="spill">Processed: <b id="tproc">0</b></div>
    <div class="spill">Rate: <b id="rate">0</b>/s</div>
  </div>
</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const N={{
  case:    {{x:80, y:210,r:37,c:'#6C63FF'}},
  material:{{x:268,y:88, r:29,c:'#A78BFA'}},
  machine: {{x:360,y:210,r:37,c:'#F59E0B'}},
  worker:  {{x:360,y:332,r:30,c:'#10B981'}},
  outcome: {{x:600,y:210,r:37,c:'#EF4444'}},
}};
const EDGES=[
  {{f:'case',    t:'machine', c:'#6C63FF',w:2.5,prim:true, freq:26}},
  {{f:'machine', t:'outcome', c:'#EF4444',w:2.5,prim:true, freq:32}},
  {{f:'material',t:'machine', c:'#A78BFA',w:1.5,prim:false,freq:50}},
  {{f:'worker',  t:'machine', c:'#10B981',w:1.5,prim:false,freq:58}},
  {{f:'case',    t:'worker',  c:'#6C63FF',w:1.2,prim:false,freq:68}},
];
let parts=[],cnts={{case:0,machine:0,outcome:0}},total=0,prev=0,rate=0,frame=0,lastT=Date.now();
function h2r(h,a){{
  const r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);
  return `rgba(${{r}},${{g}},${{b}},${{a}})`;
}}
function drawEdges(){{
  EDGES.forEach(e=>{{
    const f=N[e.f],t=N[e.t];
    ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(t.x,t.y);
    ctx.strokeStyle=h2r(e.c,0.2);ctx.lineWidth=e.w;ctx.stroke();
    const ang=Math.atan2(t.y-f.y,t.x-f.x);
    const ax=t.x-Math.cos(ang)*(t.r+5),ay=t.y-Math.sin(ang)*(t.r+5);
    ctx.beginPath();
    ctx.moveTo(ax,ay);
    ctx.lineTo(ax-9*Math.cos(ang-0.45),ay-9*Math.sin(ang-0.45));
    ctx.lineTo(ax-9*Math.cos(ang+0.45),ay-9*Math.sin(ang+0.45));
    ctx.closePath();ctx.fillStyle=h2r(e.c,0.4);ctx.fill();
  }});
}}
function spawn(ei){{
  const e=EDGES[ei],f=N[e.f],t=N[e.t];
  parts.push({{x:f.x,y:f.y,tx:t.x,ty:t.y,from:e.f,to:e.t,c:e.c,
    prog:0,spd:0.007+Math.random()*0.006,sz:e.prim?5:3.5,trail:[],done:false}});
}}
function pulse(id){{
  const el=document.getElementById('n-'+id);
  if(!el)return;el.classList.remove('pulse');void el.offsetWidth;el.classList.add('pulse');
}}
function setCtr(id,v){{const el=document.getElementById('cnt-'+id);if(el)el.textContent=v.toLocaleString();}}
function loop(){{
  ctx.clearRect(0,0,680,420);drawEdges();frame++;
  EDGES.forEach((e,i)=>{{if(frame%e.freq===0)spawn(i);}});
  parts=parts.filter(p=>p.prog<1);
  document.getElementById('aflows').textContent=parts.length;
  parts.forEach(p=>{{
    p.prog+=p.spd;if(p.prog>1)p.prog=1;
    p.x+=(p.tx-p.x)*p.spd*8;p.y+=(p.ty-p.y)*p.spd*8;
    p.trail.push({{x:p.x,y:p.y}});if(p.trail.length>9)p.trail.shift();
    p.trail.forEach((pt,i)=>{{
      ctx.beginPath();ctx.arc(pt.x,pt.y,p.sz*(i/p.trail.length)*0.7,0,Math.PI*2);
      ctx.fillStyle=h2r(p.c,(i/p.trail.length)*0.3);ctx.fill();
    }});
    ctx.beginPath();ctx.arc(p.x,p.y,p.sz,0,Math.PI*2);
    ctx.fillStyle=p.c;ctx.shadowColor=p.c;ctx.shadowBlur=12;ctx.fill();ctx.shadowBlur=0;
    if(p.prog>=0.97&&!p.done){{
      p.done=true;pulse(p.to);
      if(p.to==='machine'){{cnts.machine++;setCtr('machine',cnts.machine);}}
      if(p.to==='outcome'){{cnts.outcome++;total++;setCtr('outcome',cnts.outcome);
        document.getElementById('tproc').textContent=total.toLocaleString();}}
      if(p.from==='case'){{cnts.case++;setCtr('case',cnts.case);}}
    }}
  }});
  const now=Date.now();
  if(now-lastT>1000){{rate=total-prev;prev=total;lastT=now;document.getElementById('rate').textContent=rate;}}
  requestAnimationFrame(loop);
}}
loop();
</script></body></html>""", height=432)

            _lgd_pairs = [
                (_lbl_case,     "#6C63FF"),
                (_lbl_machine,  "#F59E0B"),
                (_lbl_worker,   "#10B981"),
                (_lbl_material, "#A78BFA"),
                (_lbl_outcome,  "#EF4444"),
            ]
            st.markdown(
                f'<div style="margin-top:4px;padding:6px 14px;background:{CARD};'
                f'border:1px solid {BORDER};border-radius:8px;display:flex;flex-wrap:wrap;">'
                + "".join(
                    f'<span style="display:inline-flex;align-items:center;gap:4px;'
                    f'margin:0 12px 4px 0;">'
                    f'<span style="width:8px;height:8px;border-radius:50%;'
                    f'background:{_lc};display:inline-block;"></span>'
                    f'<span style="font-size:0.75rem;color:{MUTED};">{_ll}</span></span>'
                    for _ll, _lc in _lgd_pairs
                )
                + "</div>",
                unsafe_allow_html=True,
            )

'''

out = src[:si] + NEW_BLOCK + src[ei:]

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Done — file is now {len(out):,} chars.")
