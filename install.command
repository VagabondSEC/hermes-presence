#!/bin/bash
# Hermes Presence Mac installer (double-click)
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 missing. Install it from python.org then run this file again."
  read -r -p "Press Enter to close..."
  exit 1
fi
python3 -m venv .venv
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python presence.py install
echo "Done. Play Hermes on Discord, like a real gamer."
sleep 2
