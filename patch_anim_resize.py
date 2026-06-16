# -*- coding: utf-8 -*-
"""
Patch dashboard.py — resize Tab 1 animation canvas from 680px to 640px
so it fits inside the ~660px left column without overflow.
Scale factor: 640/680 = 0.9412
"""
import sys

PATH = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

replacements = [
    # CSS wrap size
    ('.wrap{{position:relative;width:680px;height:420px;margin:0 auto;}}',
     '.wrap{{position:relative;width:640px;height:400px;margin:0 auto;overflow:hidden;}}'),

    # body overflow — also clip html
    ('body{{background:#0D1117;font-family:\'Inter\',-apple-system,sans-serif;overflow:hidden;}}',
     'html,body{{background:#0D1117;font-family:\'Inter\',-apple-system,sans-serif;overflow:hidden;max-width:100%;}}'),

    # Canvas element dimensions
    ('  <canvas id="cv" width="680" height="420"></canvas>',
     '  <canvas id="cv" width="640" height="400"></canvas>'),

    # HTML node positions (left / top)
    # n-case: left:80px → 75px, top:210px → 197px
    ('style="left:80px;top:210px;width:78px;height:78px;',
     'style="left:75px;top:197px;width:78px;height:78px;'),

    # n-material: left:268px → 252px, top:88px → 83px
    ('style="left:268px;top:88px;width:62px;height:62px;',
     'style="left:252px;top:83px;width:62px;height:62px;'),

    # n-machine: left:360px → 339px, top:210px → 197px
    ('style="left:360px;top:210px;width:78px;height:78px;',
     'style="left:339px;top:197px;width:78px;height:78px;'),

    # n-worker: left:360px → 339px, top:332px → 312px
    ('style="left:360px;top:332px;width:64px;height:64px;',
     'style="left:339px;top:312px;width:64px;height:64px;'),

    # n-outcome: left:600px → 564px, top:210px → 197px
    ('style="left:600px;top:210px;width:78px;height:78px;',
     'style="left:564px;top:197px;width:78px;height:78px;'),

    # JS canvas N positions
    ("  case:    {{x:80, y:210,r:37,c:'#6C63FF'}},",
     "  case:    {{x:75, y:197,r:37,c:'#6C63FF'}},"),
    ("  material:{{x:268,y:88, r:29,c:'#A78BFA'}},",
     "  material:{{x:252,y:83, r:29,c:'#A78BFA'}},"),
    ("  machine: {{x:360,y:210,r:37,c:'#F59E0B'}},",
     "  machine: {{x:339,y:197,r:37,c:'#F59E0B'}},"),
    ("  worker:  {{x:360,y:332,r:30,c:'#10B981'}},",
     "  worker:  {{x:339,y:312,r:30,c:'#10B981'}},"),
    ("  outcome: {{x:600,y:210,r:37,c:'#EF4444'}},",
     "  outcome: {{x:564,y:197,r:37,c:'#EF4444'}},"),

    # Canvas clearRect
    ('ctx.clearRect(0,0,680,420);',
     'ctx.clearRect(0,0,640,400);'),

    # iframe height
    ('</script></body></html>""", height=432)',
     '</script></body></html>""", height=412)'),
]

changed = 0
for old, new in replacements:
    if old in src:
        src = src.replace(old, new, 1)
        changed += 1
        print(f"  OK: {old[:60].strip()!r}")
    else:
        print(f"  MISS: {old[:60].strip()!r}")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\nDone — {changed}/{len(replacements)} replacements applied.")
