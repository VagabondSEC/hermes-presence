#!/bin/bash
# Hermes Presence installer Mac (double-clic)
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 manquant. Installe-le depuis python.org puis relance ce fichier."
  read -r -p "Appuie sur Entrée pour fermer..."
  exit 1
fi
python3 -m venv .venv
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python presence.py install
echo "C'est bon. Joue à Hermes sur Discord, comme un vrai gamer."
sleep 2
