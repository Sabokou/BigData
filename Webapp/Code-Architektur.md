# Code Architektur in der Webapp
## Allgemeines
```run.py```
Die run.py wird genutzt um die App im Container auszuführen. Wichtig hierbei ist, dass die IP-Adresse umgesetzt wird auf
0.0.0.0. Dieses erlaubt Verbindungen von außerhalb des Container-Netzes.
```config.py```
Wird genutzt um während der Entwicklungsphase, die DEBUG-Funktionen innerhalb von Flask zu nutzen.
## App-Ordner
Der App-Ornder ist in standardmäßiger Flask-Struktur aufgebaut. 
- ```static/``` beinhaltet Assets wie das CSS-Layout und notwendige Javascript applets.
- ```templates/``` beinhaltet die Jinja3 Vorlagen für die Flask-App. Benannt werden sie nach der Seite für die sie genutzt werden.

Python-Dateien:
- ```legerible.py``` bildet sämtliche Funktionen fürs Backend ab, ergo Abfragen auf der Datenbank.
- ```book.py``` ist eine ausgelagerte Klasse, in der Methoden für die Interaktion mit Büchern abgebildet sind.
- ```views.py``` ist das zentrale Steuerelement über die Seitennavigation in der App. Hier werden die Seiten funktionstechnisch aufgebaut und die jeweiligen Seiten mit Inhalten gefüllt.

## Database-Ornder
Im Datenbanken-Ordner liegen 2 Dateien. Die ```init.sql``` ist eine Textdatei in der die SQL-Instruktionen für den Bau der Datenbank hinterlegt sind.
In der ```isbn.txt``` sind beispielhaft ISBNs aufgelistet, die genutzt werden während der Initialisierung um Bücher in der Datenbank zu schreiben.