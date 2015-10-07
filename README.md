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

~ cd Programs/pmvs-2/program/main 

