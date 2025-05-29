# Bild Vektorisierer

Ein Windows-Programm zur Konvertierung von Bildern in Vektorgrafiken (SVG) mit konfigurierbarem Threshold-Wert.

## Features

- 🖼️ Unterstützt PNG, JPG, JPEG, BMP, TIFF Formate
- ⚙️ Konfigurierbarer Threshold-Wert (0-255, Standard: 128)
- 📁 Automatische Ordnerauswahl mit GUI
- 📊 Fortschrittsanzeige während der Verarbeitung
- 📤 Automatische Erstellung eines "output" Ordners
- 🖥️ Benutzerfreundliche Windows-Oberfläche
- 🚀 **Vollständig eigenständige exe-Datei** (keine weiteren Dateien erforderlich)

## 🎯 EMPFOHLEN: GitHub Actions (Automatische Windows-exe)

### ✅ Die beste Lösung für zuverlässige Windows-exe Dateien!

**Warum GitHub Actions?**
- ✅ **100% Windows-kompatibel** - Läuft auf echten Windows-Servern
- ✅ **Kostenlos** für öffentliche Repositories
- ✅ **Automatisch** bei jedem Code-Update
- ✅ **Professionell** - Wie große Software-Unternehmen arbeiten

### 🚀 Schnellstart (2 Minuten Setup)

```bash
# 1. GitHub Setup ausführen
./setup_github.sh

# 2. Repository auf GitHub.com erstellen

# 3. Repository verknüpfen und pushen
git remote add origin https://github.com/IHR_USERNAME/Vectorizer.git
git push -u origin main

# 4. Fertig! GitHub Actions erstellt automatisch die Windows-exe
```

**📥 exe-Datei herunterladen:**
- Gehen Sie zu GitHub.com → Ihr Repository → Actions → Artifacts
- Oder erstellen Sie ein Release: `git tag v1.0.0 && git push origin v1.0.0`

**📖 Detaillierte Anleitung:** [GITHUB_ACTIONS_ANLEITUNG.md](GITHUB_ACTIONS_ANLEITUNG.md)

---

## 🔧 Alternative: Lokaler Build (Mac → Windows)

### Für Mac-Benutzer (Cross-Compilation für Windows)

```bash
# 1. Abhängigkeiten installieren
pip install -r requirements.txt

# 2. Vollautomatischer Build (lädt Potrace automatisch herunter)
python build.py
```

**⚠️ Hinweis:** Cross-Compilation kann Kompatibilitätsprobleme verursachen. 
**GitHub Actions wird empfohlen** für 100%ige Windows-Kompatibilität.

### Alternative: Testskript verwenden

```bash
python test_build.py
```

Dieses Skript führt den kompletten Build-Prozess durch und zeigt detaillierte Informationen an.

## Installation und Build

### Voraussetzungen

- **Python 3.8+** installiert
- **Internet-Verbindung** (für automatischen Potrace-Download)

### Automatischer Build-Prozess

Das Build-System lädt automatisch alle benötigten Komponenten herunter:

1. **Potrace für Windows** wird automatisch von der offiziellen Quelle heruntergeladen
2. **PyInstaller** erstellt eine eigenständige exe-Datei
3. **Alle Abhängigkeiten** werden in die exe-Datei eingebettet

### Manuelle Schritte (falls automatischer Download fehlschlägt)

```bash
# Schritt 1: Abhängigkeiten installieren
pip install -r requirements.txt

# Schritt 2: Potrace manuell herunterladen (falls nötig)
python download_potrace.py

# Schritt 3: Windows exe erstellen
python build.py

# Optional: Build-Artefakte löschen
python build.py clean
```

### Windows-Benutzer (direkter Build)

```batch
# Einfach das Batch-Skript ausführen
install_and_build.bat
```

## Verwendung

1. **Programm starten**: Doppelklick auf `BildVektorisierer.exe`
2. **Ordner auswählen**: Klicken Sie auf "Durchsuchen" und wählen Sie den Ordner mit Ihren Bildern
3. **Threshold einstellen**: Verwenden Sie den Schieberegler (0-255, Standard: 128)
   - Niedrigere Werte = mehr Details werden als schwarz erkannt
   - Höhere Werte = nur sehr dunkle Bereiche werden als schwarz erkannt
4. **Vektorisierung starten**: Klicken Sie auf "Vektorisierung starten"
5. **Ergebnisse**: Die SVG-Dateien werden im `output` Ordner innerhalb Ihres Bilderordners gespeichert

## Funktionsweise

Das Programm:
1. Lädt jedes Bild und konvertiert es zu Graustufen
2. Wendet den Threshold-Wert an (Schwarz-Weiß-Konvertierung)
3. Verwendet Potrace zur Vektorisierung des Bitmaps
4. Speichert das Ergebnis als SVG-Datei

## Unterstützte Dateiformate

**Eingabe:**
- PNG
- JPG/JPEG
- BMP
- TIFF/TIF

**Ausgabe:**
- SVG (Scalable Vector Graphics)

## Projektstruktur

```
Vectorizer/
├── vectorizer.py              # Hauptprogramm
├── build.py                   # Build-Skript für PyInstaller
├── download_potrace.py        # Automatischer Potrace-Download
├── test_build.py              # Test-Skript für Build-Prozess
├── setup_github.sh            # GitHub Actions Setup
├── requirements.txt           # Python-Abhängigkeiten
├── install_and_build.bat      # Windows Batch-Skript
├── .github/workflows/         # GitHub Actions
│   └── build-windows.yml      # Automatischer Windows-Build
├── README.md                  # Diese Datei
├── potrace/                   # Potrace-Binärdateien (automatisch erstellt)
│   └── potrace.exe            # (automatisch heruntergeladen)
├── dist/                      # Generierte exe-Datei
│   └── BildVektorisierer.exe  # ← Diese Datei an Kumpel senden!
└── build/                     # Temporäre Build-Dateien
```

## 🎯 Für Mac-Benutzer: exe an Windows-Kumpel senden

### Option 1: GitHub Actions (EMPFOHLEN)

1. **Setup ausführen:**
   ```bash
   ./setup_github.sh
   ```

2. **Repository auf GitHub erstellen und pushen**

3. **exe-Datei automatisch herunterladen:**
   - GitHub.com → Repository → Actions → Artifacts
   - Oder über Releases bei Git Tags

4. **Link an Kumpel senden:**
   ```
   https://github.com/IHR_USERNAME/Vectorizer/releases/latest
   ```

### Option 2: Lokaler Build

1. **Build ausführen:**
   ```bash
   python build.py
   ```

2. **exe-Datei finden:**
   ```
   dist/BildVektorisierer.exe
   ```

3. **Datei senden:**
   - Per E-Mail, Cloud-Storage, USB-Stick, etc.
   - Die exe-Datei ist vollständig eigenständig
   - Keine weiteren Dateien erforderlich

4. **Kumpel kann direkt verwenden:**
   - Doppelklick auf die exe-Datei
   - Keine Installation erforderlich
   - Funktioniert auf allen Windows-Versionen (7, 8, 10, 11)

## Fehlerbehebung

### "Potrace konnte nicht heruntergeladen werden"
- Prüfen Sie Ihre Internet-Verbindung
- Das Build-Skript versucht automatisch 64-bit und 32-bit Versionen
- Bei anhaltenden Problemen: Manueller Download von https://potrace.sourceforge.net/

### "Build fehlgeschlagen"
- Stellen Sie sicher, dass alle Abhängigkeiten installiert sind: `pip install -r requirements.txt`
- Verwenden Sie das Test-Skript für detaillierte Fehleranalyse: `python test_build.py`

### "exe-Datei startet nicht auf Windows"
- **GitHub Actions exe:** 100% kompatibel
- **Cross-Compiled exe:** Kann Kompatibilitätsprobleme haben
- Antivirus-Software könnte die Datei blockieren (Whitelist hinzufügen)
- Bei Problemen: Windows Defender SmartScreen "Trotzdem ausführen" wählen

## Technische Details

- **GUI Framework**: tkinter (Python Standard)
- **Bildverarbeitung**: Pillow (PIL)
- **Vektorisierung**: Potrace 1.16
- **Build Tool**: PyInstaller
- **Empfohlene Methode**: GitHub Actions (Windows Server)
- **Alternative**: Cross-Compilation (Mac → Windows)
- **Zielplattform**: Windows 7/8/10/11 (32-bit und 64-bit)

## Lizenz

Dieses Projekt ist für den persönlichen und kommerziellen Gebrauch frei verfügbar.

---

## 🔧 Entwickler-Notizen

### Build-System Features
- ✅ **GitHub Actions** - Automatische Windows-exe (EMPFOHLEN)
- ✅ Automatischer Potrace-Download
- ✅ Cross-Platform Build (Mac → Windows)
- ✅ Eigenständige exe-Datei (keine DLL-Abhängigkeiten)
- ✅ Automatische Fehlerbehandlung
- ✅ Detaillierte Build-Logs

### Getestete Umgebungen
- **GitHub Actions** (Windows Server - 100% kompatibel)
- macOS (Build-System)
- Windows 7/8/10/11 (Zielplattform)
- Python 3.8, 3.9, 3.10, 3.11 