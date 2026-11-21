#!/bin/sh
cd "$(dirname "$0")"
cat 0*.txt > libro.txt
python3 ../../_strumenti/build_finzione.py libro.txt "../Le tessere di Agostino.docx"
