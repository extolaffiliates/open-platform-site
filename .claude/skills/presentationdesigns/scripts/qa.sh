#!/usr/bin/env bash
# QA every rendering of a deck: Impeccable detector, Guizang validators, PPTX -> PNG contact sheet, Spectacle syntax.
# Usage: qa.sh presentations/<deck-name>
set -uo pipefail
DECK="${1:?usage: qa.sh presentations/<deck-name>}"
DECK="$(cd "$DECK" && pwd)"
SK="$HOME/.claude/skills"
OUT="${TMPDIR:-/tmp}/deck-qa-$(basename "$DECK")"; rm -rf "$OUT"; mkdir -p "$OUT"
export NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}"

echo "== Impeccable detector"
for f in "$DECK"/guizang/index.html "$DECK"/spectacle/index.html; do
  [ -f "$f" ] || continue
  echo "-- ${f#$DECK/}"
  "$SK/impeccable/scripts/impeccable" detect --json "$f" 2>/dev/null \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print(f'{len(d)} findings');[print(' ',x['severity'],x['antipattern'],'|',x['snippet'][:110]) for x in d]"
done

if [ -f "$DECK/guizang/index.html" ]; then
  echo "== Guizang validators"
  node "$SK/guizang-ppt-skill/scripts/validate-swiss-deck.mjs" "$DECK/guizang/index.html" 2>&1 | tail -6
  node "$SK/guizang-ppt-skill/scripts/validate-presenter-mode.mjs" "$DECK/guizang/index.html" 2>&1 | tail -2
fi

if [ -f "$DECK/spectacle/index.html" ]; then
  echo "== Spectacle module syntax"
  python3 -c "
import sys;s=open(sys.argv[1]).read();m=s[s.index('<script type=\"module\">')+22:s.rindex('</script>')];open(sys.argv[2],'w').write(m)" "$DECK/spectacle/index.html" "$OUT/spectacle.mjs" \
    && node --check "$OUT/spectacle.mjs" && echo "ok"
fi

PPTX=$(ls "$DECK"/pptx/*.pptx 2>/dev/null | head -1)
if [ -n "$PPTX" ] && command -v soffice >/dev/null; then
  echo "== PPTX render"
  soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
  pdftoppm -r 50 -png "$OUT"/*.pdf "$OUT/s" && python3 - "$OUT" <<'PY'
import sys, glob
from PIL import Image
files = sorted(glob.glob(sys.argv[1] + "/s-*.png"), key=lambda p: int(p.rsplit("-", 1)[1][:-4]))
ims = [Image.open(f) for f in files]; w, h = ims[0].size; rows = (len(ims) + 1) // 2
g = Image.new("RGB", (w * 2, h * rows), "white")
for i, im in enumerate(ims): g.paste(im, ((i % 2) * w, (i // 2) * h))
g.save(sys.argv[1] + "/pptx-contact-sheet.png"); print(f"{len(ims)} slides -> {sys.argv[1]}/pptx-contact-sheet.png")
PY
fi

[ -f "$DECK/quarkdown/main.qd" ] && { echo "== Quarkdown"; command -v quarkdown >/dev/null \
  && (cd "$DECK/quarkdown" && quarkdown c main.qd -o "$OUT/qd" && echo "compiled -> $OUT/qd") \
  || echo "quarkdown CLI not installed: source only"; }
echo "QA output: $OUT"
