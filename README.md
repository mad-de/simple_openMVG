Vorarbeit:
- Stelle sicher, dass in Ordner ~/openMVG_Build/software/SfM/ auch der Ordner cameraSensorWidth existiert und in der darin befindlichen Datei "cameraGenerated.txt" die verwendete Kamera eingestragen ist. Sonst kommt es beim Start des Programs zu mehreren Fehlermeldungen


- Erstelle Ordner "Gummiente" mit Inhalt in ~/openMVG_Build/software/SfM/
- öffne die Datei "workflow-gummiente.py" 
- Im Bereich der Variablen passe ändere bei "arbeitsverzeichnis" den Ordner zu dem ordner den du benutzt.
- Image1 und Image2 stehen für die zwei Bilder mit den größten Übereinstimmungen (manuell zuzuordnen). Ändere die Dateinamen für diese beiden Bilder.
 
- Terminal:
~ cd openMVG_Build/software/SfM/
~ python workflow_gummiente.py


PMVS:
- Kopiere den PMVS Unterordner aus dem *DATEINAME*_sequential oder *DATEINAME*_global Ordner aus dem neuen Ordner *DATEINAME_out* mit den meisten Informationen in den Ordner Programs/pmvs-2/data. Benenne ihn jetzt zum Beispiel in gummiente_sequential um.
- Terminal:
~ cd Programs/pmvs-2/program/main 
~ ./pmvs2 ../../data/gummiente_sequential/ pmvs_options.txt

Warten bis das Programm durchgelaufen ist

~ cd ~/Programs/pmvs-2/data/gummiente_sequential/models
~ dir

Output müsste sein: pmvs_options.txt.patch	pmvs_options.txt.ply  pmvs_options.txt.pset

Auf Ubuntu Systemen müssen wir häufig noch die Punkte durch Kommas ersetzen, damit Meshlab sie lesen kann:
~ sed -i "s/\./,/g" pmvs_options.txt.ply
~ sed -i "s/format ascii 1,0/format ascii 1.0/g" pmvs_options.txt.ply
~ meshlab pmvs_options.txt.ply
