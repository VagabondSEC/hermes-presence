#!/usr/bin/env python3
"""Hermes Presence. Shows "Playing Hermes" on Discord like it's a real game.

Commands :
  install       installs autostart (Windows or Mac) then launches the presence
  uninstall     removes autostart and kills the running presence
  kill          kills the running presence without touching autostart
  run           runs the presence (used by autostart)

Configuration lives in config.json next to this file.
"""

import json
import os
import subprocess
import sys
import time

# Neutralise la pollution PYTHONPATH de l'app Hermes (venv pywin32 incomplet)
os.environ.pop("PYTHONPATH", None)
for _p in list(sys.path):
    if "hermes-agent" in _p or ".hermes-runtime" in _p:
        sys.path.remove(_p)

try:
    from pypresence import Presence
except ImportError:
    print("pypresence missing. Run  pip install -r requirements.txt  first")
    sys.exit(1)

try:
    import psutil
except ImportError:
    psutil = None

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")
DEFAULT_CONFIG = {
    "client_id": "1538766707638935552",
    "app_name": "Hermes",
    "details": None,
    "state": None,
    "large_image": None,
    "only_when_process": None,
    "check_interval": 15,
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg = dict(DEFAULT_CONFIG)
            cfg.update(json.load(f))
            return cfg
    except Exception as e:
        print("config.json unreadable", e)
        return dict(DEFAULT_CONFIG)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def _venv_pythonw():
    if sys.platform == "win32":
        return os.path.join(HERE, ".venv", "Scripts", "pythonw.exe")
    return os.path.join(HERE, ".venv", "bin", "python")


def autostart_windows():
    startup = os.path.join(
        os.environ["APPDATA"],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
    )
    os.makedirs(startup, exist_ok=True)
    vbs_path = os.path.join(startup, "hermes-presence.vbs")
    pythonw = _venv_pythonw()
    if not os.path.exists(pythonw):
        pythonw = sys.executable
    script = os.path.join(HERE, "presence.py")
    content = (
        'Set sh = CreateObject("WScript.Shell")\r\n'
        'sh.Run """{}"" ""{}"" run", 0, False\r\n'.format(pythonw, script)
    )
    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(content)
    return vbs_path


def _launchctl_load(plist_path):
    """Charge le LaunchAgent. Essaie bootstrap (moderne) puis load (ancien)."""
    try:
        uid = os.getuid() if hasattr(os, "getuid") else 0
        subprocess.run(
            ["launchctl", "bootstrap", f"gui/{uid}", plist_path],
            capture_output=True, check=False,
        )
    except Exception:
        pass
    subprocess.run(["launchctl", "load", "-w", plist_path], capture_output=True, check=False)


def _launchctl_unload(plist_path):
    try:
        uid = os.getuid() if hasattr(os, "getuid") else 0
        subprocess.run(
            ["launchctl", "bootout", f"gui/{uid}", plist_path],
            capture_output=True, check=False,
        )
    except Exception:
        pass
    subprocess.run(["launchctl", "unload", "-w", plist_path], capture_output=True, check=False)


def autostart_mac():
    plist_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(plist_dir, exist_ok=True)
    plist_path = os.path.join(plist_dir, "com.hermes.presence.plist")
    py = os.path.join(HERE, ".venv", "bin", "python")
    script = os.path.join(HERE, "presence.py")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hermes.presence</string>
    <key>ProgramArguments</key>
    <array>
        <string>{py}</string>
        <string>{script}</string>
        <string>run</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>"""
    with open(plist_path, "w", encoding="utf-8") as f:
        f.write(content)
    _launchctl_load(plist_path)
    return plist_path


def install_autostart():
    if sys.platform == "win32":
        return autostart_windows()
    return autostart_mac()


def uninstall_autostart():
    if sys.platform == "win32":
        startup = os.path.join(
            os.environ["APPDATA"],
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
        )
        vbs_path = os.path.join(startup, "hermes-presence.vbs")
        if os.path.exists(vbs_path):
            os.remove(vbs_path)
            return vbs_path
        return None
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.hermes.presence.plist")
    _launchctl_unload(plist_path)
    if os.path.exists(plist_path):
        os.remove(plist_path)
    return plist_path


def spawn_presence():
    """Lance la présence en tâche de fond, sans fenêtre."""
    if sys.platform == "win32":
        pythonw = _venv_pythonw()
        if not os.path.exists(pythonw):
            pythonw = sys.executable
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen(
            [pythonw, os.path.join(HERE, "presence.py"), "run"],
            creationflags=flags,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            [sys.executable, os.path.join(HERE, "presence.py"), "run"],
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def target_running(cfg):
    names = cfg.get("only_when_process")
    if not names:
        return True
    if isinstance(names, str):
        names = [names]
    if psutil is None:
        return True
    try:
        procs = {p.name().lower() for p in psutil.process_iter()}
        return any(str(n).lower() in procs for n in names)
    except Exception:
        return True


def kill_running():
    """Tue toutes les instances de présence en cours.

    Ne cible que les process lancés avec l'argument "run" (la présence).
    Sur Windows le python du venv est un stub qui lance le vrai process,
    donc os.getpid() ne protège que le stub : filtrer sur "run" évite de
    se tuer soi-même quand on exécute uninstall/kill.
    """
    killed = []
    if psutil is None:
        print("psutil missing, cannot kill processes")
        return killed
    for p in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmd = [str(c) for c in (p.info.get("cmdline") or [])]
            if "run" not in cmd:
                continue
            if not any("presence.py" in c for c in cmd):
                continue
            p.kill()
            killed.append(p.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed


def run_presence(cfg):
    rpc = Presence(cfg["client_id"])
    rpc.connect()
    start = int(time.time())
    last_ok = None
    while True:
        running = target_running(cfg)
        if running and not last_ok:
            start = int(time.time())
        last_ok = running
        try:
            if running:
                rpc.update(
                    state=cfg.get("state"),
                    details=cfg.get("details"),
                    large_image=cfg.get("large_image"),
                    start=start,
                )
            else:
                rpc.clear()
        except Exception:
            # Discord fermé ou connexion perdue, on réessaie plus tard
            time.sleep(30)
            try:
                rpc.connect()
            except Exception:
                pass
        time.sleep(int(cfg.get("check_interval", 15)))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    cfg = load_config()
    if cmd == "install":
        path = install_autostart()
        print("Autostart installed", path)
        spawn_presence()
        print("Presence launched")
    elif cmd == "uninstall":
        path = uninstall_autostart()
        print("Autostart removed", path or "nothing to remove")
        killed = kill_running()
        print("Presence process killed", killed or "nothing running")
    elif cmd == "kill":
        killed = kill_running()
        print("Presence process killed", killed or "nothing running")
    elif cmd == "run":
        run_presence(cfg)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
