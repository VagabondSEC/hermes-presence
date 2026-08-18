#!/bin/bash
# Hermes Presence Mac uninstaller
cd "$(dirname "$0")" || exit 1
.venv/bin/python presence.py uninstall
echo "Hermes Presence removed from startup. You can delete the folder now."
sleep 2
