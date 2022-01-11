# Lösung für den InformatiCup 2022
### Teamname: **Team Zug zum Erfolg**
Dies ist eine Lösung für den von der [GI](https://gi.de/) veranstalteten Wettbewerb InformatiCup2022. Thema des Wettbewerbs ist es, mit Hilfe von Software und Algorithmen eine Lösung mit der geringsten Verspätung für das Reisen von Zügen und Fahrgästen zu planen. Die genaue Aufgabe des Wettbewerbs finden Sie [hier](https://informaticup.github.io/competition/20-current).

<!-- Unsere Lösung wurde mit Python und Algorithmus Dynamischee Planung erstellt, mit Docker deployed. Weitere Informationen über das Projekt finden Sie in der [Dokumentation](./), die Informationen über API finden Sie [hier](./). -->
## Systemvoraussetzungen
Unsere Lösung wurde mit Python erstellt. Zur Ausführung der Software brauchen Sie zumindest **Python 3 (3.x.x)** und Betriebssystem **Windows** oder **Linux**. Python-spezifische Erweiterungen oder Module muss hingegen nur für die Entwickler-Dokumentation installiert werden und werden von unserer Software auch nicht weiter benötigt.
## Installation
Eine Entwicklungskopie des Repository des Projekts bzw. der Software kann mit folgendem Befehl erstellt werden.
```
$ git clone https://gitlab.uni-hannover.de/informaticup-2022/gruppe-3/team-zug-zum-erfolg.git
```

### Linux

#### Installation von Python3
Zur Installation von **Python3** Sie können folgender Befehl ausgeführt. 
```
$ sudo apt-get install python
```
Nachdem die Installation abgeschlossen wurde, kann mit folgendem Befehl die Version von Python überprüft werden:

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

#### Installation von Python3
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

## Benutzung
Die Ausführung der Software kann auf zwei unterschiedliche Möglichkeiten erfolgen. Jedoch muss bei beiden die Kommandozeile (engl. Terminal) genutzt werden. Bei ersten Möglichkeit handelt es sich um die direkte Ausführung mit einem Befehl, indem unser Python-Modul einfach mit Python gestartet wird. Die zwei Möglichkeit hingegen, beschreibt die Ausführung der Software in einem Docker-Container.

### Direkte Benutzung
**Linux**

Falls noch nicht erfolgt, muss zuerst in das Hauptverzeichnis des Projekts navigiert werden. In der Kommandozeile muss dann einfach abhängig vom Betriebssystem folgender Befehl ausgeführt werden:

```
$ python3 -m abfahrt
```

Um den Inhalt einer Eingabedatei einlesen zu lassen:

```
$ python -m abfahrt < [Dateipfad]
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

Im Folgenden sind einige Methoden zum Testen.

### Zur Erzeugung der Dokumentation mit `pdoc`


```
$ python -m pdoc -o ./doc -d google abfahrt
```
> Sie müssen eventuell das Modul `pdoc` installieren

```
$ pip install pdoc
```
---

### Zum Testen vom Modul **main**:

```
$ python -m abfahrt [< input.txt]
```



**Example**:

```
$ python -m abfahrt < abfahrt/testfiles/test_1.txt
```

---


### Zum Testen vom Modul **test_simulator**:
```
$ python -m abfahrt.testutils.test_simulator
```


**Example only one Test**:

```
$ python -m abfahrt.testutils.test_simulator -singletest test_1.txt
```



**Example Verbose**:
```
$ python -m abfahrt.testutils.test_simulator -verbose
```


**Example soft**:
```
$ python -m abfahrt.testutils.test_simulator -soft
```
---

### Zum Testen vom Modul **test_generator**:
```
$ python -m abfahrt.testutils.test_generator
```


**Example**:

```
$ python -m abfahrt.testutils.test_generator
```


```
$ python -m abfahrt.testutils.test_generator -test_amount 10 -number_stations 10 -number_lines 20 -number_trains 10 -number_passengers 10 -max_capacity_station 10 -max_capacity_line 10 -max_length_line 10 -max_capacity_train 10 -max_groups
```


## Lizenz

Diese Projekt unterliegt der [MIT Lizenz](./LICENSE).

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

