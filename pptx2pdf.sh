#!/bin/bash
# Convert PowerPoint decks to PDF with the copy of PowerPoint on this Mac.
#
#     ./pptx2pdf.sh ~/some/deck.pptx assets/slides/dai-fma2026-talk.pdf
#
# Why it looks like this: PowerPoint is sandboxed and refuses AppleScript access to
# ordinary paths with error -9074 — Dropbox, ~/Documents, even its own container.
# It *will* open a file inside the Office group container, so the deck is copied there,
# converted, and the PDF copied back out. The `in (POSIX file ...)` form matters too;
# passing the path as a plain string fails with a -50 parameter error.
#
# LibreOffice would make this a one-liner, but it isn't installed here.
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: $0 <input.pptx> <output.pdf>"; exit 1; }
in=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
out_dir=$(cd "$(dirname "$2")" && pwd); out="$out_dir/$(basename "$2")"
[ -f "$in" ] || { echo "no such file: $in"; exit 1; }

work="$HOME/Library/Group Containers/UBF8T346G9.Office/pptx2pdf"
mkdir -p "$work"
stem="conv_$$"
cp "$in" "$work/$stem.pptx"

osascript - "$stem" <<'APPLESCRIPT'
on run argv
	set stem to item 1 of argv
	set bse to (POSIX path of (path to home folder)) & "Library/Group Containers/UBF8T346G9.Office/pptx2pdf/"
	tell application "Microsoft PowerPoint"
		activate
		with timeout of 280 seconds
			open (bse & stem & ".pptx")
			delay 3
			set p to active presentation
			save p in (POSIX file (bse & stem & ".pdf")) as save as PDF
			delay 2
			close p saving no
		end timeout
	end tell
end run
APPLESCRIPT

[ -f "$work/$stem.pdf" ] || { echo "conversion produced nothing"; exit 1; }
mv "$work/$stem.pdf" "$out"
rm -f "$work/$stem.pptx" "$work/~\$$stem.pptx"
pages=$(mdls -name kMDItemNumberOfPages -raw "$out" 2>/dev/null)   # empty outside Spotlight-indexed folders
case "$pages" in ''|'(null)') echo "$out  ($(du -h "$out" | cut -f1))";;
                 *) echo "$out  ($(du -h "$out" | cut -f1), $pages pages)";; esac
