#!/bin/zsh
# Export a Word document to PDF using Microsoft Word, so brand fonts (Montserrat)
# and layout render exactly as in Word. The PDF is saved next to the .docx.
# Usage: Tools/docx_to_pdf.sh "path/to/file.docx"
set -e
in="${1:A}"
[[ -f "$in" && "$in" == *.docx ]] || { echo "Usage: $0 file.docx" >&2; exit 1; }
out="${in%.docx}.pdf"
# Word is sandboxed: export into its container first, then move the PDF.
tmp="$HOME/Library/Containers/com.microsoft.Word/Data/Documents/docx_to_pdf_$$.pdf"
osascript <<EOF
with timeout of 180 seconds
tell application "Microsoft Word"
  open (POSIX file "$in")
  delay 5
  set d to active document
  save as d file name (POSIX file "$tmp" as text) file format format PDF
  close d saving no
end tell
end timeout
EOF
mv -f "$tmp" "$out"
echo "Saved: $out"
