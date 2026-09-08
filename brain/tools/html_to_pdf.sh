#!/bin/zsh
# html_to_pdf.sh IN.html OUT.pdf
# Converte un HTML autonomo in PDF usando Chrome headless (nessuna dipendenza da
# installare). Usato da /giunta per produrre la sintesi stampabile.
set -e
IN="${1:?uso: html_to_pdf.sh IN.html OUT.pdf}"
OUT="${2:?uso: html_to_pdf.sh IN.html OUT.pdf}"

for C in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"; do
  if [[ -x "$C" ]]; then CHROME="$C"; break; fi
done
if [[ -z "$CHROME" ]]; then
  echo "Nessun browser Chromium trovato: apro l'HTML, stampa tu in PDF (Cmd-P)." >&2
  open "$IN"; exit 3
fi

# percorso assoluto -> file:// URL
case "$IN" in
  /*) ABS="$IN" ;;
  *)  ABS="$PWD/$IN" ;;
esac

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$ABS" 2>/dev/null || \
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$ABS" 2>/dev/null

[[ -f "$OUT" ]] && echo "PDF: $OUT" || { echo "Generazione PDF fallita" >&2; exit 1; }
