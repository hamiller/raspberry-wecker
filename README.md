Wecker aus einem Raspberry Pi
=============================

Für die Rotations-Abfrage wurde die externe Klasse von Bob Rathbone (http://www.bobrathbone.com) verwendet


__WORK IN PROGRESS__

## Zielsystem
Anzeige der Uhrzeit vom System über 7-Segment Display (mit ntp synchronisiert - gehört nicht hierher)
* Einstellen einer Weckzeit
* Einstellen der Wecklautstärke
* Anzeige des aktuellen Menüs (Uhrzeit, Weckzeit, Lautstärke) mit 32x32-Punkt Matrix (?)
* Evtl. Einstellen des Wecktons (über einstellungen.txt eventuell)

## Funktionen/Steuerung
Die Steuerung des Systems wird durch 3 Taster, 1 Schalter und 1 Scrollrad vorgenommen:
* Scrollrad zum erhöhen/erniedrigen der aktuellen Funktion (abhängig vom aktuell ausgewählten Menü)
* Taster zum Durchschalten des Menüs (Weckzeit, Lautstärke, ...?)
* Taster zum "Schlafenlegen (=10min Pausieren) des aktiven Weckrufes"
* Taster zum Deaktieren des aktiven Weckrufes für 24 Stunden (oder bis zum nächsten Weckruf, wenn die Weckzeit zwischendurch geändert wird)
* Schalter zum Aktivieren/Deaktivieren der Weckfunktion

