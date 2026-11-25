#!/bin/zsh
# Rebuild the A-frame print PDF and a preview JPG from aframe.html
cd "$(dirname "$0")"
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
P="Aureus-A-Frame-600x900mm-PRINT-3mm-bleed.pdf"
"$C" --headless=new --disable-gpu --no-pdf-header-footer --allow-file-access-from-files --print-to-pdf="$P" "file://$PWD/aframe.html" 2>/dev/null
pdfinfo "$P" | grep -E "Pages"
pdftoppm -jpeg -r 80 -singlefile "$P" Aureus-A-Frame-preview 2>/dev/null
