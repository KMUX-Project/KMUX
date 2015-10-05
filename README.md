# KMUX

## Entwicklungsumgebung aufsetzen
## Set up Development Environment

```
sudo apt-get install python3 python3-jinja2 python3-pip python3-pep8
sudo pip install blessings
```

## Coding Guidelines überprüfen
## Check Coding Guidelines

```
KMUX$ ./check_code.sh
```

## Kompletten Code automatisch formatieren
## Auto Format the complete code

```
KMUX$ ./autofix_code.sh
```

## Script ausführen
## Run script

```
$ cd KMUX
KMUX$ export PYTHONPATH="$PYTHONPATH:$PWD"
KMUX$ cd main/
KMUX/main$ ./kmux-manage.py
```

Anschließend kann man im Verzeichnis ``config.out/`` die automatisch generierten Dateien finden.
All automatically generated files are to be found in ``config.out/``
