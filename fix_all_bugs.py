# -*- coding: utf-8 -*-
"""Fix all 4 bugs in dashboard.py."""

path = r'D:\placement\project\Causal OCPM\causal_ocpm\app\dashboard.py'

with open(path, 'rb') as f:
    data = f.read()

# ── BUG 3: emoji mojibake (binary replacements) ─────────────────────────────
emoji_fixes = [
    # ● U+25CF BLACK CIRCLE  (stage-dot ○/●)
    (b'\xc3\xa2\xe2\x80\x94\xc2\x8f', '●'.encode('utf-8')),
    # variation selector U+FE0F  (fixes ⚙️ on tab + ⚠️ on warnings)
    (b'\xc3\xaf\xc2\xb8\xc2\x8f', '️'.encode('utf-8')),
    # 🌐 U+1F310 GLOBE WITH MERIDIANS  (sidebar Analysis Domain)
    (b'\xc3\xb0\xc5\xb8\xc5\x92\xc2\x90', '\U0001f310'.encode('utf-8')),
    # 🌍 U+1F30D EARTH GLOBE EUROPE-AFRICA  (BPI 2019 tab + section icons)
    (b'\xc3\xb0\xc5\xb8\xc5\x92\xc2\x8d', '\U0001f30d'.encode('utf-8')),
    # 📋 U+1F4CB CLIPBOARD  (Case Attribution tab + section icon)
    (b'\xc3\xb0\xc5\xb8\xe2\x80\x9d\xc2\x8d', '\U0001f4cb'.encode('utf-8')),
    # 🏥 U+1F3E5 HOSPITAL  (Domain Comparison tab + section icon)
    (b'\xc3\xb0\xc5\xb8\xc2\x8f\xc2\xa5', '\U0001f3e5'.encode('utf-8')),
    # 📐 U+1F4D0 TRIANGULAR RULER  (Ablation Study section icon)
    (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\x90', '\U0001f4d0'.encode('utf-8')),
    # 📏 U+1F4CF STRAIGHT RULER  (Equation Fit section icon)
    (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\x8f', '\U0001f4cf'.encode('utf-8')),
]
for bad, good in emoji_fixes:
    count = data.count(bad)
    if count:
        print(f'  emoji fix applied x{count}')
    data = data.replace(bad, good)

# Decode to text for remaining fixes
text = data.decode('utf-8')

# ── BUG 1: Object Interaction Graph config ───────────────────────────────────
old_cfg = (
    '            ag_config = Config(\n'
    '                width=None,\n'
    '                height=460,\n'
    '                directed=False,\n'
    '                physics=False,\n'
    '                hierarchical=False,\n'
    '                backgroundColor=CARD,\n'
    '            )'
)
new_cfg = (
    '            ag_config = Config(\n'
    '                width=700,\n'
    '                height=460,\n'
    '                directed=False,\n'
    '                physics=True,\n'
    '                hierarchical=False,\n'
    '                backgroundColor=CARD,\n'
    '            )'
)
if old_cfg in text:
    text = text.replace(old_cfg, new_cfg)
    print('  BUG1: agraph Config -> physics=True, width=700')
else:
    print('  BUG1: Config block NOT FOUND')

# ── BUG 2: Policy Simulation sign format ─────────────────────────────────────
sign_fixes = [
    ('f"+{naive_val:.2f}"',  'f"{naive_val:+.2f}"'),
    ('f"+{causal_val:.2f}"', 'f"{causal_val:+.2f}"'),
    ('f"+{gt_val:.2f}"',     'f"{gt_val:+.2f}"'),
    ("f\"+{mfg_res['naive']:.3f}\"",   "f\"{mfg_res['naive']:+.3f}\""),
    ("f\"+{hc_res['naive']:.3f}\"",    "f\"{hc_res['naive']:+.3f}\""),
    ("f\"+{mfg_res['causal']:.3f}\"",  "f\"{mfg_res['causal']:+.3f}\""),
    ("f\"+{hc_res['causal']:.3f}\"",   "f\"{hc_res['causal']:+.3f}\""),
    ('f"+{mfg_true:.3f}"',             'f"{mfg_true:+.3f}"'),
    ('f"+{hc_true:.3f}"',              'f"{hc_true:+.3f}"'),
]
for old, new in sign_fixes:
    if old in text:
        text = text.replace(old, new)
        print(f'  BUG2: fixed sign format')
    else:
        print(f'  BUG2: NOT FOUND: {old!r}')

# ── BUG 4: Truncated metric card labels ──────────────────────────────────────
label_fixes = [
    ('"Machines / Wards"',     '"Machines"'),
    ('"Workers / Clinicians"', '"Workers"'),
    ('"Materials / Meds"',     '"Materials"'),
]
for old, new in label_fixes:
    if old in text:
        text = text.replace(old, new)
        print(f'  BUG4: {old} -> {new}')
    else:
        print(f'  BUG4: NOT FOUND: {old}')

with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print('Done.')
