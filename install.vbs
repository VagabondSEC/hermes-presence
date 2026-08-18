' Hermes Presence installer Windows (invisible, double-clic)
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
cmd = "cmd /c cd /d """ & dir & """ && python -m venv .venv && .venv\Scripts\python -m pip install -q -r requirements.txt && .venv\Scripts\python presence.py install"
code = sh.Run(cmd, 0, True)
If code <> 0 Then
  MsgBox "Un truc a planté (code " & code & "). Vérifie que Python est installé depuis python.org et coche Add to PATH, puis relance.", 48, "Hermes Presence"
Else
  MsgBox "C'est bon. Joue à Hermes sur Discord, comme un vrai gamer.", 64, "Hermes Presence"
End If
