# 🎨 Bild Vektorisierer

Ein plattformübergreifendes Python-Programm zur Vektorisierung von Bildern mit einer grafischen Benutzeroberfläche.

## 📥 Download (Empfohlen)

**Fertige Anwendungen herunterladen:**

### Automatische Builds
Bei jedem Push werden automatisch Builds für alle Plattformen erstellt:

- **Windows**: `BildVektorisierer.exe` 
- **macOS**: `BildVektorisierer.dmg`
- **Linux**: `BildVektorisierer-Linux.tar.gz`

**Download-Links:**
1. Gehen Sie zu [Actions](../../actions)
2. Wählen Sie den neuesten erfolgreichen Build
3. Laden Sie das Artifact für Ihr System herunter

### Releases
Stabile Versionen finden Sie unter [Releases](../../releases)

## 🚀 Lokale Entwicklung

Falls Sie den Code selbst ausführen oder modifizieren möchten:

### Voraussetzungen
- Python 3.11+
- Git

### Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/vectorizer.git
cd vectorizer

# Virtuelle Umgebung erstellen (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Virtuelle Umgebung erstellen (Windows)
python -m venv venv
venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Potrace installieren
# macOS:
brew install potrace

# Ubuntu/Debian:
sudo apt-get install potrace

# Windows: Wird automatisch beim Build heruntergeladen
```

### Programm starten
```bash
python vectorizer.py
```

### Eigene Builds erstellen
```bash
# PyInstaller installieren
pip install pyinstaller

# Build erstellen
pyinstaller vectorizer.spec

# Ergebnis in dist/ Ordner
```

## ✨ Features

- ✅ **Plattformübergreifend:** Windows, macOS, Linux
- ✅ **Unterstützte Formate:** PNG, JPG, JPEG, BMP, TIFF
- ✅ **Ausgabeformat:** SVG (Scalable Vector Graphics)
- ✅ **Benutzerfreundlich:** Einfache grafische Oberfläche
- ✅ **Konfigurierbarer Threshold:** Für optimale Ergebnisse
- ✅ **Batch-Verarbeitung:** Mehrere Bilder gleichzeitig
- ✅ **Automatische Builds:** GitHub Actions CI/CD

## 📝 Verwendung

1. **Programm starten:** Doppelklick auf die heruntergeladene Datei
2. **Ordner auswählen:** Klicken Sie auf "Durchsuchen" und wählen Sie den Ordner mit Ihren Bildern
3. **Threshold einstellen:** Anpassen für bessere Ergebnisse (Standard: 128)
4. **Vektorisierung starten:** Klicken Sie auf "Vektorisierung starten"
5. **Ergebnisse:** SVG-Dateien werden im "output" Ordner gespeichert

## 🔧 Technische Details

- **GUI-Framework:** tkinter (Python Standard Library)
- **Bildverarbeitung:** Pillow (PIL)
- **Vektorisierung:** Potrace
- **Build-Tool:** PyInstaller
- **CI/CD:** GitHub Actions
- **Unterstützte Systeme:** Windows 10+, macOS 10.13+, Linux

## 🏗️ Build-Prozess

Der Build-Prozess läuft vollautomatisch über GitHub Actions:

1. **Bei jedem Push:** Automatische Builds für alle Plattformen
2. **Potrace-Integration:** Automatischer Download und Einbindung
3. **Plattformspezifische Optimierung:** Native Apps für jedes System
4. **Artifact-Upload:** Fertige Builds als Download verfügbar

### Build-Status
![Build Status](../../actions/workflows/build.yml/badge.svg)

## 🐛 Fehlerbehebung

### macOS: "App kann nicht geöffnet werden"
```bash
# Gatekeeper umgehen (nur bei vertrauenswürdigen Quellen!)
sudo xattr -rd com.apple.quarantine BildVektorisierer.app
```

### Windows: "Windows hat den Start dieser App verhindert"
- Klicken Sie auf "Weitere Informationen"
- Klicken Sie auf "Trotzdem ausführen"

### Linux: Ausführungsrechte setzen
```bash
chmod +x BildVektorisierer
```

## 📞 Support

Bei Problemen oder Fragen:
- Erstellen Sie ein [Issue](../../issues)
- Beschreiben Sie das Problem detailliert
- Geben Sie Ihr Betriebssystem an
- Fügen Sie Screenshots bei, falls hilfreich

## 🤝 Beitragen

Beiträge sind willkommen! Der Build-Prozess läuft automatisch:

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Push löst automatisch Builds aus
5. Erstellen Sie einen Pull Request

---

**Entwickelt mit ❤️ von Aaron's Software** 