# Hermes Presence

Fais croire à tes potes que tu joues à Hermes sur Discord. Comme si c'était un vrai jeu. Avec le chrono qui tourne et tout.

Un double-clic et c'est réglé. Aucun terminal à garder ouvert, ça se relance tout seul à chaque démarrage de ta machine. Ton profil affiche "Joue à Hermes" et personne ne saura que c'est pas un jeu AAA.

## Installation Windows

1. Installe Python depuis python.org si tu ne l'as pas (coche Add to PATH)
2. Double-clique sur install.vbs
3. Regarde ton profil Discord

## Installation Mac

1. Installe Python depuis python.org si tu ne l'as pas
2. Double-clique sur install.command (la première fois, clic droit puis Ouvrir)
3. Regarde ton profil Discord

Si macOS refuse de lancer le fichier, ouvre un terminal dans le dossier et tape chmod +x install.command puis réessaie.

## Personnaliser

Ouvre config.json avec un éditeur de texte.

- details    la première ligne sous "Joue à Hermes"
- state      la deuxième ligne
- only_when_process    si tu veux que la présence s'affiche seulement quand un programme précis tourne (par exemple Hermes.exe)
- client_id  ton propre ID d'application Discord si tu veux pas utiliser l'app partagée

## Désinstaller

Double-clique sur uninstall.vbs sur Windows, uninstall.command sur Mac. C'est tout.

## Comment ça marche

Discord Rich Presence, l'API officielle de Discord. Le script parle directement au client Discord installé sur ta machine, exactement comme le ferait un jeu. Aucun bot, aucun token, aucune donnée qui passe par un serveur tiers.

## Questions fréquentes

**Il faut créer une app Discord ?**
Non. Le repo embarque une app partagée nommée Hermes, prête à l'emploi. Si tu veux ta propre app, crée-la sur discord.com/developers/applications et colle ton ID dans config.json.

**Ça marche si Discord est fermé ?**
Non. Discord doit tourner, comme pour un vrai jeu.

**C'est légal ?**
Oui. C'est l'API officielle de Discord, la même que celle utilisée par les jeux.

**J'ai pas Python, ça marche quand même ?**
Non. Python 3 est requis, c'est une installation de deux minutes sur python.org.

**Pourquoi je devrais faire ça ?**
Aucune idée. Mais tes potes verront "Joue à Hermes" et se poseront des questions. C'est le but.
