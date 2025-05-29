# BildVektorisierer - Test-Anleitung

Diese Anleitung erklärt, wie Sie sicherstellen können, dass die `BildVektorisierer.exe` korrekt funktioniert.

## 🔧 Automatisierte Tests

### 1. Lokale Tests ausführen

```bash
# Alle Tests ausführen
python test_exe.py
```

Das Test-Skript prüft:
- ✅ Existenz der exe-Datei
- ✅ Python-Abhängigkeiten
- ✅ Potrace-Integration
- ✅ Bildkonvertierung
- ✅ exe-Start-Fähigkeit

### 2. GitHub Actions Tests

Die Tests laufen automatisch bei jedem Push:
- Gehen Sie zu: `https://github.com/twoace/vectorizer/actions`
- Klicken Sie auf den neuesten Workflow-Lauf
- Überprüfen Sie alle Test-Schritte

## 🧪 Manuelle Tests

### Test 1: exe-Datei Grundfunktionen

```bash
# 1. Prüfen ob exe existiert
ls -la dist/BildVektorisierer.exe

# 2. Dateigröße prüfen (sollte 20-50 MB sein)
du -h dist/BildVektorisierer.exe
```

### Test 2: Potrace-Integration

```bash
# Potrace-Version prüfen
potrace/potrace.exe --version

# Sollte ausgeben: "potrace 1.16"
```

### Test 3: Testbilder erstellen und konvertieren

```python
# Erstelle ein Testbild
from PIL import Image, ImageDraw

img = Image.new('RGB', (200, 200), 'white')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 150, 150], fill='black')
img.save('test_input/test.png')
```

### Test 4: exe manuell testen

1. **Doppelklick auf `BildVektorisierer.exe`**
2. **GUI sollte sich öffnen**
3. **Ordner mit Testbildern auswählen**
4. **Threshold einstellen (z.B. 128)**
5. **"Vektorisierung starten" klicken**
6. **Prüfen ob SVG-Dateien im output-Ordner erstellt wurden**

## 🎯 Erwartete Ergebnisse

### Erfolgreiche Tests zeigen:

```
[OK] BildVektorisierer.exe gefunden (XX.X MB)
[OK] tkinter (GUI-Framework)
[OK] PIL (Bildverarbeitung)
[OK] subprocess (Prozess-Management)
[OK] pathlib (Pfad-Handling)
[OK] tempfile (Temporäre Dateien)
[OK] Potrace verfügbar: potrace 1.16
[OK] 3 Testbilder erstellt
[OK] SVG erstellt (XXX Bytes)
[OK] SVG-Format korrekt
[OK] exe startet erfolgreich

Test-Ergebnisse: 6/6 bestanden
[SUCCESS] Alle Tests bestanden! Die exe sollte korrekt funktionieren.
```

### Bei Problemen:

#### Problem: "exe startet nicht"
```bash
# Lösung 1: Prüfen Sie Windows Defender / Antivirus
# Lösung 2: Führen Sie als Administrator aus
# Lösung 3: Prüfen Sie fehlende DLLs mit Dependency Walker
```

#### Problem: "Potrace nicht gefunden"
```bash
# Lösung: Potrace neu herunterladen
python download_potrace.py
```

#### Problem: "SVG-Dateien werden nicht erstellt"
```bash
# Lösung 1: Prüfen Sie Schreibrechte im output-Ordner
# Lösung 2: Prüfen Sie ob Eingabebilder gültig sind
# Lösung 3: Prüfen Sie Threshold-Wert (0-255)
```

## 🔍 Detaillierte Diagnose

### Windows-spezifische Tests

```powershell
# Prüfe exe-Abhängigkeiten
dumpbin /dependents dist/BildVektorisierer.exe

# Prüfe ob exe signiert ist
Get-AuthenticodeSignature dist/BildVektorisierer.exe

# Teste exe-Start mit Logging
dist/BildVektorisierer.exe > output.log 2>&1
```

### Kompatibilitätstests

Die exe sollte funktionieren auf:
- ✅ Windows 10 (64-bit)
- ✅ Windows 11 (64-bit)
- ⚠️ Windows 7/8 (möglicherweise fehlende DLLs)
- ❌ 32-bit Systeme (exe ist 64-bit)

## 📊 Performance-Tests

### Benchmark-Test

```python
import time
from pathlib import Path

# Teste Verarbeitungsgeschwindigkeit
start_time = time.time()
# ... Vektorisierung von 10 Testbildern ...
end_time = time.time()

print(f"Verarbeitung von 10 Bildern: {end_time - start_time:.2f} Sekunden")
# Erwartung: < 30 Sekunden für 10 einfache Bilder
```

### Speicher-Test

```bash
# Überwachen Sie den Speicherverbrauch während der Ausführung
# Erwartung: < 200 MB RAM-Verbrauch
```

## 🚀 Deployment-Tests

### Vor der Veröffentlichung prüfen:

1. **Alle automatisierten Tests bestanden** ✅
2. **Manuelle GUI-Tests erfolgreich** ✅
3. **Verschiedene Bildformate getestet** (PNG, JPG, BMP) ✅
4. **Verschiedene Bildgrößen getestet** (klein, mittel, groß) ✅
5. **Edge-Cases getestet** (leere Bilder, sehr große Bilder) ✅
6. **Performance akzeptabel** (< 5 Sekunden pro Bild) ✅

### Release-Checkliste:

- [ ] Alle Tests bestanden
- [ ] exe-Datei < 100 MB
- [ ] Keine Abhängigkeiten zu externen DLLs
- [ ] GUI startet ohne Fehler
- [ ] Vektorisierung funktioniert
- [ ] SVG-Output ist gültig
- [ ] Dokumentation aktuell

## 📞 Support

Bei Problemen:

1. **Führen Sie `python test_exe.py` aus**
2. **Prüfen Sie die GitHub Actions Logs**
3. **Erstellen Sie ein Issue mit:**
   - Betriebssystem-Version
   - Fehlermeldung
   - Test-Ergebnisse
   - Beispiel-Eingabebild

---

**Hinweis:** Diese Tests garantieren, dass die exe-Datei technisch funktioniert. Für die beste Benutzererfahrung sollten Sie die exe auch manuell mit echten Bildern testen. 