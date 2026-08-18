# Hermes Presence

Show your friends that you are a larper working on Hermes. Your Discord profile displays "Playing Hermes" like it's a real game, with the session timer and everything.

Why would I do this? No idea. But your friends will see "Playing Hermes" and start asking questions, or know that you are working hard to take their job. That's the point.

One double-click and you're done. No terminal to keep open, it restarts by itself every time you boot your machine.

## Windows install

1. Install Python from python.org if you don't have it (tick Add to PATH)
2. Double-click windows/install.vbs
3. Look at your Discord profile

## Mac install

1. Install Python from python.org if you don't have it
2. Double-click mac/install.command. If you downloaded the repo as a ZIP, macOS Gatekeeper blocks the first launch, right-click the file then Open to allow it once
3. Look at your Discord profile

If macOS complains about permissions or refuses to run the file, open a terminal in the repo folder and run

```
bash mac/install.command
```

no chmod needed.

## Uninstall

Double-click windows/uninstall.vbs on Windows, mac/uninstall.command on Mac.

It removes the autostart entry and kills the running presence process. Nothing survives, the Discord activity disappears within seconds. You can then delete the folder.

If you only want to stop the presence without removing autostart, open a terminal in the repo folder and run

Mac

```
.venv/bin/python presence.py kill
```

Windows

```
.venv\Scripts\python presence.py kill
```

## Customize

The first run creates config.json next to the script. Open it with a text editor.

- details    the first line under "Playing Hermes"
- state      the second line
- only_when_process    if you want the presence to show only when a specific program is running (e.g. Hermes.exe)
- client_id  your own Discord application ID if you don't want to use the shared app

## What's inside

```
presence.py            the script, shared by both platforms
requirements.txt       pypresence and psutil
config.json            created on first run, local only, never committed
windows/               install.vbs and uninstall.vbs
mac/                   install.command and uninstall.command
```

## How it works

Discord Rich Presence, the official Discord API. The script talks directly to the Discord client installed on your machine, exactly like a game would. No bot, no token, no data going through a third-party server.

## FAQ

**Do I need to create a Discord app?**
No. The script ships with a shared app named Hermes, ready to use. If you want your own app, create it at discord.com/developers/applications and paste your ID into config.json.

**Does it work if Discord is closed?**
No. Discord needs to be running, just like for a real game.

**Is it legal?**
Yes. It's the official Discord API, the same one games use.

**I don't have Python, does it still work?**
No. Python 3 is required, it's a two-minute install from python.org.
