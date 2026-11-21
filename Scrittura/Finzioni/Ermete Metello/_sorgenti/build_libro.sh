#!/bin/sh
# Monta il libro dai sorgenti in libro/ e genera il .docx
cd "$(dirname "$0")"
cat libro/0*.txt > metello_libro.txt
python3 ../../_strumenti/build_finzione.py metello_libro.txt "../Ermete Metello - Storia di un monaco.docx"
