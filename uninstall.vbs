' Hermes Presence uninstaller Windows
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
code = sh.Run("cmd /c cd /d """ & dir & """ && .venv\Scripts\python presence.py uninstall", 0, True)
MsgBox "Hermes Presence est retirée du démarrage. Tu peux supprimer le dossier.", 64, "Hermes Presence"
