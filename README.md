# Lösung für den InformatiCup 2022
### Teamname: **Team Zug zum Erfolg**
Dies ist eine Lösung für den von der [GI](https://gi.de/) veranstalteten Wettbewerb InformatiCup2022. Thema des Wettbewerbs ist, eine Software zu entwickeln, welche Fahrpläne erstellen/berechnen kann und die Gesamtverspätung der Passagiere möglichst minimiert. Die genaue Aufgabe des Wettbewerbs finden Sie [hier](https://informaticup.github.io/competition/20-current).

Entwickler:
Berkehan Ünal, Han Yang, Ling-Hsuan Hsu, Lukas Dreyer

<!-- Unsere Lösung wurde mit Python und Algorithmus Dynamischee Planung erstellt, mit Docker deployed. Weitere Informationen über das Projekt finden Sie in der [Dokumentation](./), die Informationen über API finden Sie [hier](./). -->
## Systemvoraussetzungen
Unsere Lösung wurde mit Python entwickelt. Zur Ausführung der Software wird mindestens **Python 3 (3.x.x)** und eine Betriebssystem-Distribution von **Windows** oder **Linux** benötigt. Python-spezifische Erweiterungen oder Module muss hingegen nur für die Entwickler-Dokumentation installiert werden und werden von unserer Software auch nicht weiter benötigt.
## Installation der Software und der Abhängigkeiten
Eine Entwicklungskopie des Repository des Projekts bzw. der Software kann mit folgendem Befehl erstellt werden.
```
$ git clone https://github.com/Team-Zugig-zum-Erfolg/InformatiCup.git
```

### Linux

#### Installation von Python
Zur Installation von **Python 3** muss der folgende Befehl ausgeführt werden.
```
$ sudo apt-get install python3
```
Nachdem die Installation abgeschlossen wurde, kann mit folgendem Befehl die Version von Python überprüft werden.

```
$ python3 --version
```
Wenn die Ausgabe **Python 3.x.x** entspricht, ist die Installation erfolgreich abgeschlossen und die für die Software benötigte Version von Python wurde erfolgreich installiert.

#### Installation von Docker
Ein Docker-Container enthält alle benötigte Umgebung und Module. Um die Software in einem Docker-Container auszuführen, muss Docker ebenfalls installiert werden, falls noch nicht geschehen.

Für die Installation von Docker gibt es, wie auf der offiziellen Internetseite unter https://docs.docker.com/engine/install beschrieben, mehrere Möglichkeiten. Wir empfehlen die Installation über ein DEB-/RPM-Package, denn bei dieser Möglichkeit sind am wenigsten Schritte durchzuführen.

1.  Dazu  muss  zuerst  im  Browser  zu  der  Internetseite  unter https://docs.docker.com/engine/install/navigiert werden.

2. Dort muss dann im nächsten Schritt das Betriebssystem ausgewählt werden.

3. Im dritten Schritt muss dann zu dem Block Install from a package navigiert werden.

4. Dort befindet sich, entsprechend der Beschreibung im Block, ein Link zu den verfügbaren DEB-/RPM-Packages. Nach der System-Archtitektur und der gewünschten Version (also z.B. stable oder test) kann das benötigte DEB-/RPM-Package ausfindig gemacht und heruntergeladen werden. DEB-Packages haben die Dateiendung `.deb` und RPM-Packages die Dateiendung `.rpm`.

Danach muss in der Kommandozeile zu dem Verzeichnis des heruntergeladenen DEB-/RPM-Packages gewechselt werden und der folgende Befehl ausgeführt werden:

**Ubuntu** und **Debian**:

```
$ sudo dpkg -i [Name/Pfad des DEB-Packages]
```
**CentOS**:

```
$ sudo yum install [Name/Pfad des RPM-Packages]
```

```
$ sudo systemctl start docker
```
Liegt ein anderes Betriebssystem vor, muss die im oberen Abschnitt genannte Internetseite aufgerufen werden und die für das Betriebssystem entsprechende Anleitung befolgt werden. Für die Befehle oben sind außerdem Administrator-Rechte notwendig.

### Windows

#### Installation von Python
Eine herkömmliche Installation in Windows ist über die Kommandozeile eher weniger zu empfehlen. Stattdessen wird die Installation über die graphische Benutzeroberfläche und mithilfe eines Internet-Browsers empfohlen. Dazu muss lediglich die folgende Internetseite bzw. URL aufgerufen werden:

    https://www.python.org/download

Dort ist dann ein Link zum Herunterladen der aktuellen Version von Python (diese entspricht der benötigten Version) aufgeführt. Über diesen wird dann eine ausführbare Installationsdatei heruntergeladen. Diese muss dann ausgeführt und den Anweisungen der Installation gefolgt werden.

> Achtung: Die Installation benötigt Administrator-Rechte!

Nachdem die Installation abgeschlossen wurde, kann mit folgendem Befehl in der Kommandozeile die installierte Version von Python überprüft werden:
```
$ python --version
```
#### Installation von Docker
Um die Ausführung unserer Software auf einem Windows-System in einem Docker-Container durchzuführen, muss auf diesem Windows-System die Anwendung `Docker` bzw. `Docker Desktop` installiert sein.

Für die Installation sind die folgenden Schritte notwendig:

1. Zuerst muss zu der Internetseite navigiert werden.

    https://docs.docker.com/desktop/windows/install

2. Danach muss auf der geladenen Seite über die (eindeutig sichtbare) Herunterladen-Schaltfläche, die ausführbare Installationsdatei heruntergeladen und dann ausgeführt werden.

3. Danach muss den Anweisungen des Installationsvorgangs Folge geleistet werden und zum Schluss der Rechner neu gestartet werden. Dabei muss (vermutlich) ein Update-Paket für den Linux-Kernel heruntergeladen werden, den Link zum diesem wird jedoch natürlich während der Installation mitgeteilt und ebenfalls darauf hingewiesen, dass dieses installiert werden muss. Ansonsten ist Docker auf dem Windows-System nicht vollständig einsatzbereit.


### Generierung der Entwickler-Dokumentation
```
$ python3 -m pdoc -o ./doc -d google abfahrt
```
Windows:
```
$ python -m pdoc -o ./doc -d google abfahrt
```
> Dazu muss zwingend die Python-Erweiterung `pdoc` installiert sein, falls noch nicht geschehen.

Die Installation von der Python-Erweiterung `pdoc` kann mit folgendem Befehl durchgeführt werden.

```
$ python3 -m pip install pdoc
```
Windows:
```
$ python -m pip install pdoc
```

## Ausführung
Die Ausführung der Software kann auf zwei unterschiedliche Möglichkeiten erfolgen. Jedoch muss bei beiden die Kommandozeile (engl. Terminal) genutzt werden. Bei ersten Möglichkeit handelt es sich um die direkte Ausführung mit einem Befehl, indem unser Python-Modul einfach mit Python gestartet wird. Die zwei Möglichkeit hingegen, beschreibt die Ausführung der Software in einem Docker-Container.

### Direkte Ausführung
**Linux**

Falls noch nicht erfolgt, muss zuerst in das Hauptverzeichnis des Projekts navigiert werden. In der Kommandozeile muss dann einfach abhängig vom Betriebssystem folgender Befehl ausgeführt werden:

```
$ python3 -m abfahrt
```

Um den Inhalt einer Eingabedatei einlesen zu lassen:

```
$ python3 -m abfahrt < [Dateipfad]
```

**Windows**
```
$ python -m abfahrt
```
Um den Inhalt einer Eingabedatei einlesen zu lassen:
```
$ python -m abfahrt < [Dateipfad]
```

### Docker

Zuerst muss mittels der Anwendung Docker ein Abbild (engl. Image) von der Software usw. erstellt werden. Dazu muss in dem Hauptverzeichnis des geklonten Projekts (engl. Repository) zuerst folgender Befehl ausgeführt werden:

```
$ docker build -t abfahrt .
```

Nun wurde ein Abbild (engl. Image) mit dem Namen `abfahrt` gebaut. Um nun die Software in einem Docker-Container auszuführen, muss nochmals anschließend der folgende Befehl ausgeführt werden:
```
$ docker run --rm -i --name container_abfahrt abfahrt [< input.txt]
```

Mit den Argumenten `--rm` und `-i` wird die korrekte Ausführung gewährleistet und deshalb sollten diese auch nicht fehlen. Mit `--rm ` wird einerseits sichergestellt, dass der Docker-Container nach der Ausführung wieder gelöscht wird und der Name `container_abfahrt` wieder freigegeben wird, andererseits mit dem Argument `-i` dafür gesorgt, dass die Eingabe über die Standardeingabe eingelesen werden kann.

> Die Ausführung in einem Docker-Container erfordert zusätzlich die Installation von Docker, was standardmäßig nicht der Fall ist (siehe Installation).

## Testen

Mit folgenden Werkzeugen/Modulen kann die Software getestet werden.

### Testen mit dem Modul **test_simulator**:
```
$ python3 -m abfahrt.testutils.test_simulator
```
Windows:
```
$ python -m abfahrt.testutils.test_simulator
```

### Testen mit dem Modul **test_generator**:
```
$ python3 -m abfahrt.testutils.test_generator
```
Windows:
```
$ python -m abfahrt.testutils.test_generator
```
Beispiel:
```
$ python3 -m abfahrt.testutils.test_generator -test_amount 10 -number_stations 10 -number_lines 20 -number_trains 10 -number_passengers 10 -max_capacity_station 10 -max_capacity_line 10 -max_length_line 10 -max_capacity_train 10
```
Windows:
```
$ python -m abfahrt.testutils.test_generator -test_amount 10 -number_stations 10 -number_lines 20 -number_trains 10 -number_passengers 10 -max_capacity_station 10 -max_capacity_line 10 -max_length_line 10 -max_capacity_train 10
```

### Ausführen der **Unittests**:
```
$ python3 -m abfahrt.unittest
```
Windows:
```
$ python -m abfahrt.unittest
```


**Beispiel**:
```
$ python -m abfahrt.testutils.test_generator -test_amount 10 -number_stations 10 -number_lines 20 -number_trains 10 -number_passengers 10 -max_capacity_station 10 -max_capacity_line 10 -max_length_line 10 -max_capacity_train 10
```


## Lizenz

Diese Projekt unterliegt der [MIT Lizenz](./LICENSE.md).

```
  _______                      ______                                     ______       __      _         ___   ___ ___  ___  
 |__   __|                    |___  /                                    |  ____|     / _|    | |       |__ \ / _ \__ \|__ \
    | | ___  __ _ _ __ ___       / /_   _  __ _    _____   _ _ __ ___    | |__   _ __| |_ ___ | | __ _     ) | | | | ) |  ) |
    | |/ _ \/ _` | '_ ` _ \     / /| | | |/ _` |  |_  / | | | '_ ` _ \   |  __| | '__|  _/ _ \| |/ _` |   / /| | | |/ /  / /
    | |  __/ (_| | | | | | |   / /_| |_| | (_| |   / /| |_| | | | | | |  | |____| |  | || (_) | | (_| |  / /_| |_| / /_ / /_
    |_|\___|\__,_|_| |_| |_|  /_____\__,_|\__, |  /___|\__,_|_| |_| |_|  |______|_|  |_| \___/|_|\__, | |____|\___/____|____|
                                           __/ |                                                  __/ |                      
                                          |___/                                                  |___/                       
```
