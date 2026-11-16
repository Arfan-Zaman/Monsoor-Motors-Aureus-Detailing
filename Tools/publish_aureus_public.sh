#!/bin/zsh
# Publishes a clean public copy of the "Aureus Detailing" folder to github.com/Arfan-Zaman/Aureus-Detailing.
# Only files already tracked in the private repo are copied (so no videos, no HR, nothing ignored).
# Left out on purpose: the trainer's real face photos, third-party reference material, account set-up notes.
# The public repo gets one fresh commit each time (no private history). Run again whenever the public copy should be updated.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; OUT="$(mktemp -d)/Aureus-Detailing"; mkdir -p "$OUT"
cd "$ROOT"
git ls-files -z "Aureus Detailing" | grep -zvE "^Aureus Detailing/(06 References/|08 Social Media/Character Board/references/|08 Social Media/Instagram-TikTok-Setup\.md)" \
  | while IFS= read -r -d '' f; do d="$OUT/${f#Aureus Detailing/}"; mkdir -p "$(dirname "$d")"; cp "$f" "$d"; done
cd "$OUT"; git init -q -b main; git add -A; git commit -q -m "Aureus Detailing: brand, website and social media work (public copy, $(date +%Y-%m-%d))"
gh repo view Arfan-Zaman/Aureus-Detailing >/dev/null 2>&1 || gh repo create Arfan-Zaman/Aureus-Detailing --public --description "Aureus Detailing, Perth: brand kit, website and social media work" >/dev/null
git remote add origin https://github.com/Arfan-Zaman/Aureus-Detailing.git; git push -q -f origin main
echo "published $(git ls-files | wc -l | tr -d ' ') files -> https://github.com/Arfan-Zaman/Aureus-Detailing"
