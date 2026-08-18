#!/bin/bash
# Hermes Presence uninstaller Mac
cd "$(dirname "$0")" || exit 1
.venv/bin/python presence.py uninstall
echo "Hermes Presence est retirée du démarrage. Tu peux supprimer le dossier."
sleep 2
