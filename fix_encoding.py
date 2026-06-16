"""
Reverse CP1252-double-encoding in dashboard.py.

The file was accidentally saved with each UTF-8 byte re-encoded through
Windows-1252, producing garbled output like â€" instead of — and
ðŸ"¬ instead of 🔬. This script reverses that process.
"""
import ast

INFILE  = 'app/dashboard.py'
OUTFILE = 'app/dashboard.py'

def fix_encoding(text: str) -> str:
    """
    Greedily scan the string. When a non-ASCII char is found that can be
    CP1252-encoded, try accumulating more chars until the CP1252 bytes form
    a valid UTF-8 sequence. If successful replace; otherwise pass through.
    """
    chars  = list(text)
    result = []
    i = 0
    while i < len(chars):
        ch = chars[i]
        if ord(ch) <= 0x7F:
            result.append(ch)
            i += 1
            continue
        # Non-ASCII — try to CP1252-encode and find a valid UTF-8 completion
        replaced = False
        # Look ahead up to 6 extra chars (covers 4-byte emoji → 4 cp1252 chars)
        for look in range(1, 7):
            chunk = ''.join(chars[i : i + look])
            try:
                raw = chunk.encode('cp1252')
            except (UnicodeEncodeError, LookupError):
                break  # not cp1252-encodable, stop
            try:
                decoded = raw.decode('utf-8')
                # Decoded successfully — verify it's a strict improvement
                # (resulting char count < chunk char count)
                if len(decoded) < len(chunk):
                    result.append(decoded)
                    i += look
                    replaced = True
                    break
                # len==1 chunk decoded to 1 char: check if same char
                if len(decoded) == 1 and len(chunk) == 1:
                    result.append(decoded)
                    i += look
                    replaced = True
                    break
            except UnicodeDecodeError:
                continue   # incomplete sequence, try more chars
        if not replaced:
            result.append(ch)
            i += 1
    return ''.join(result)


with open(INFILE, 'r', encoding='utf-8-sig') as f:
    original = f.read()

fixed = fix_encoding(original)

# Verify syntax
try:
    ast.parse(fixed)
except SyntaxError as e:
    print(f"SYNTAX ERROR after fix: {e}")
    exit(1)

# Spot-check known replacements
checks = [
    ('—', '—'),    # em-dash present
    ('\U0001F52C', '🔬'),  # microscope emoji
    ('→', '→'),    # rightwards arrow
    ('╔', '╔'),    # box drawing
]
for char, label in checks:
    count = fixed.count(char)
    safe_label = label.encode('ascii', errors='replace').decode()
    safe_repr  = repr(char).encode('ascii', errors='replace').decode()
    print(f"  {safe_label} ({safe_repr}): {count} occurrences")

changed = sum(1 for a, b in zip(original, fixed) if a != b)
print(f"\nChars changed: {changed}")
print(f"Original len: {len(original)}  Fixed len: {len(fixed)}")

if changed == 0:
    print("No changes needed.")
else:
    with open(OUTFILE, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print(f"Saved to {OUTFILE}")
