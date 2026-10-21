# Notepad Automation

Mini projet Python d’automatisation desktop permettant d’ouvrir le Bloc-notes Windows et d’écrire automatiquement une série de textes pendant une durée définie.

Le projet utilise `pywinauto` avec le backend UI Automation (`uia`) afin d’interagir avec l’application Bloc-notes.

## Objectif

L’objectif du projet est de fournir une base simple pour découvrir l’automatisation d’applications Windows `.exe`.

Le script réalise les actions suivantes :

- ouverture automatique de Bloc-notes ;
- détection de la fenêtre active ;
- recherche de la zone d’édition ;
- écriture automatique de texte ;
- répétition de l’action à intervalle régulier ;
- arrêt automatique lorsque la durée définie est atteinte.

## Technologies utilisées

- Python
- pywinauto
- comtypes
- Windows UI Automation

## Prérequis

- Windows
- Python installé
- PowerShell ou terminal Windows

Il est recommandé d’utiliser Python 3.14 plutôt que Python 3.15 afin d’éviter certains avertissements de compatibilité avec `comtypes`.

Vérifier la version de Python :

```powershell
python --version
```

## Structure du projet

```text
notepad-automation/
├── .venv/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Création de l’environnement virtuel

Depuis la racine du projet :

```powershell
python -m venv .venv
```

Activation sous PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Une fois activé, le terminal doit afficher quelque chose comme :

```text
(.venv) PS C:\Develop\notepad-automation>
```

Pour quitter l’environnement virtuel :

```powershell
deactivate
```

## Installation des dépendances

Installer les dépendances depuis `requirements.txt` :

```powershell
python -m pip install -r requirements.txt
```

Exemple de contenu du fichier `requirements.txt` :

```text
pywinauto
```

Il est également possible d’installer directement la dépendance principale :

```powershell
python -m pip install pywinauto
```

## Configuration

Les principaux paramètres se trouvent au début du fichier `main.py`.

Exemple :

```python
DURATION_MINUTES = 5
INTERVAL_SECONDS = 5

TEXTS = [
    "Test automatisé en cours.",
    "Écriture périodique dans Bloc-notes.",
    "Validation de l'automatisation desktop.",
    "Nouvelle itération exécutée.",
]
```

### Durée d’exécution

Pour exécuter le script pendant 5 minutes :

```python
DURATION_MINUTES = 5
```

Pour 1 heure :

```python
DURATION_MINUTES = 60
```

Pour 2 heures :

```python
DURATION_MINUTES = 120
```

Pour 3 heures :

```python
DURATION_MINUTES = 180
```

### Intervalle entre les écritures

Le paramètre suivant définit le nombre de secondes entre deux écritures :

```python
INTERVAL_SECONDS = 5
```

Par exemple, pour écrire toutes les 30 secondes :

```python
INTERVAL_SECONDS = 30
```

## Lancer l’automatisation

Activer d’abord l’environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

Puis lancer :

```powershell
python main.py
```

Le script va :

1. ouvrir Bloc-notes ;
2. rechercher la fenêtre visible ;
3. identifier la zone d’édition ;
4. écrire une première ligne ;
5. attendre l’intervalle configuré ;
6. écrire la ligne suivante ;
7. continuer jusqu’à atteindre la durée maximale.

## Exemple de résultat

Le contenu du Bloc-notes pourra ressembler à :

```text
[09:00:00] Test automatisé en cours.
[09:00:05] Écriture périodique dans Bloc-notes.
[09:00:10] Validation de l'automatisation desktop.
[09:00:15] Nouvelle itération exécutée.
[09:00:20] Test automatisé en cours.
```

La console affiche également l’état de l’automatisation :

```text
Ouverture de Bloc-notes...
Recherche de la fenêtre...
1 fenêtre(s) Bloc-notes trouvée(s)
[0] title='Sans titre – Bloc-notes' pid=28184 visible=True
Fenêtre sélectionnée : 'Sans titre – Bloc-notes'
1 contrôle(s) Document trouvé(s)
Zone d'édition trouvée.
Automatisation lancée pendant 5 minute(s).

Itération 1: [09:00:00] Test automatisé en cours.
Prochaine saisie dans 5s - temps restant : 299s
```

## Arrêter manuellement le script

Il est possible d’arrêter le script avec :

```text
Ctrl + C
```

Le script intercepte l’arrêt clavier et affiche un résumé :

```text
Arrêt manuel demandé.
Fin de l'automatisation.
Durée réelle : 45 seconde(s)
Nombre d'itérations : 9
```

## Fonctionnement technique

Le script utilise :

```python
Application(backend="uia")
```

pour lancer Bloc-notes.

Puis :

```python
Desktop(backend="uia")
```

pour rechercher la fenêtre réellement exposée par Windows.

La fenêtre est identifiée avec :

```python
title_re=r".*(Notepad|Bloc-notes).*"
```

afin de fonctionner sur un Windows en français ou en anglais.

La zone d’édition est recherchée en priorité avec :

```python
control_type="Document"
```

et, en fallback :

```python
control_type="Edit"
```

Cette approche permet de supporter plusieurs versions de Bloc-notes.

## Diagnostic UI Automation

Si le script ne trouve pas correctement la zone d’édition, il est possible d’inspecter les contrôles exposés par Bloc-notes.

Décommenter dans `main.py` :

```python
window.print_control_identifiers()
```

Puis relancer le script.

La console affichera la hiérarchie des contrôles Windows détectés.

Cela permet notamment d’identifier :

- Window
- Document
- Edit
- Button
- MenuBar
- MenuItem

## Limites

Cette automatisation dépend de l’interface Windows et de la structure UI Automation de Bloc-notes.

Des différences peuvent exister selon :

- la version de Windows ;
- la version de Bloc-notes ;
- la langue du système ;
- le backend UI Automation ;
- la version de Python ;
- la version de `pywinauto`.

Il est également préférable de ne pas fermer Bloc-notes manuellement pendant l’exécution.

## Python 3.15 et comtypes

Avec Python 3.15, un avertissement de ce type peut apparaître :

```text
FutureWarning: You are running 'comtypes' on Python 3.15
```

Cela ne bloque pas nécessairement l’exécution, mais indique une compatibilité encore partielle.

Pour un projet plus stable, il est recommandé d’utiliser Python 3.14.

## Bonnes pratiques

Pour une automatisation desktop plus robuste :

- privilégier les contrôles UI Automation plutôt que des coordonnées fixes ;
- éviter les clics basés uniquement sur la position écran ;
- identifier les contrôles par `control_type`, titre ou AutomationId ;
- gérer explicitement les timeouts ;
- conserver des logs d’exécution ;
- séparer les actions techniques des scénarios de test ;
- éviter de dépendre d’un seul titre de fenêtre si plusieurs fenêtres peuvent être ouvertes.

## Évolutions possibles

Le projet peut être enrichi avec :

- durée passée en argument de commande ;
- intervalle configurable en argument ;
- choix dynamique des textes ;
- sauvegarde automatique du fichier ;
- fermeture automatique de Bloc-notes ;
- gestion de plusieurs applications `.exe` ;
- screenshots en cas d’erreur ;
- logs dans un fichier ;
- tests structurés avec `pytest` ;
- Page Objects / Screen Objects pour les applications desktop ;
- intégration CI ;
- rapport d’exécution.

## Exemple d’évolution avec arguments

À terme, le script pourra être lancé comme ceci :

```powershell
python main.py --duration 60 --interval 10
```

où :

- `--duration 60` représente 60 minutes ;
- `--interval 10` représente 10 secondes entre deux écritures.

## `.gitignore`

Exemple recommandé :

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

L’environnement virtuel ne doit pas être versionné dans Git.
