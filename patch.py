import re, sys

PATH = "/app/app.py"
s = open(PATH, encoding="utf-8").read()

if "if required is None:" in s:
    print("ALREADY_PATCHED")
    sys.exit(0)

pat = re.compile(
    r'^([ \t]*)required = body\.get\("required_fields"\) or DEFAULT_REQUIRED[ \t]*$',
    re.M,
)
m = pat.search(s)
if not m:
    print("OLD_NOT_FOUND")
    sys.exit(1)

ind = m.group(1)
new = (
    ind + 'required = body.get("required_fields")\n'
    + ind + 'if required is None:\n'
    + ind + '    required = DEFAULT_REQUIRED'
)
s = pat.sub(lambda mm: new, s, count=1)
open(PATH, "w", encoding="utf-8").write(s)
print("PATCHED_OK len=%d" % len(s))
