# KMUX

## Entwicklungsumgebung aufsetzen

```
sudo apt-get install python3 python3-jinja2 python3-pip python3-pep8
sudo pip install blessings
```

## Coding Guidelines überprüfen

```
KMUX$ ./check_code.sh
```

## Kompletten Code automatisch formatieren

```
KMUX$ ./autofix_code.sh
```

## Script ausfüren

```
$ cd KMUX
KMUX$ export PYTHONPATH="$PYTHONPATH:$PWD"
KMUX$ cd main/
KMUX/main$ ./kmux-manage.py
```

Anschließend kann man im Verzeichnis ``config.out/`` die automatisch generierten Dateien finden.
