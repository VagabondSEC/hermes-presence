#!/bin/bash
# Hermes Presence Mac uninstaller (kills the process and removes autostart)
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python presence.py uninstall
echo "Hermes Presence is fully removed. You can delete the folder now."
sleep 2
