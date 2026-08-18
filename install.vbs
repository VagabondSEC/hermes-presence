' Hermes Presence Windows installer (silent, double-click)
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
cmd = "cmd /c cd /d """ & dir & """ && python -m venv .venv && .venv\Scripts\python -m pip install -q -r requirements.txt && .venv\Scripts\python presence.py install"
code = sh.Run(cmd, 0, True)
If code <> 0 Then
  MsgBox "Something went wrong (code " & code & "). Make sure Python is installed from python.org with Add to PATH ticked, then run again.", 48, "Hermes Presence"
Else
  MsgBox "Done. Play Hermes on Discord, like a real gamer.", 64, "Hermes Presence"
End If
