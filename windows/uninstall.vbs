' Hermes Presence Windows uninstaller (kills the process and removes autostart)
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
code = sh.Run("cmd /c cd /d """ & dir & """ && .venv\Scripts\python presence.py uninstall", 0, True)
MsgBox "Hermes Presence is fully removed. You can delete the folder now.", 64, "Hermes Presence"
