# 🎨 BildVektorisierer

Ein einfaches Tool zur Konvertierung von Bitmap-Bildern (PNG, JPG, BMP) in SVG-Vektorgrafiken.

## 📥 Download

**Für Windows-Benutzer:**
- Gehen Sie zu [Releases](https://github.com/twoace/vectorizer/releases/latest)
- Laden Sie `BildVektorisierer_v1.0.exe` herunter
- Keine Installation erforderlich - einfach ausführen!

## 🚀 Verwendung

1. **Starten:** Doppelklick auf `BildVektorisierer_v1.0.exe`
2. **Ordner auswählen:** Wählen Sie den Ordner mit Ihren Bildern
3. **Threshold einstellen:** Anpassen für bessere Ergebnisse (Standard: 128)
4. **Vektorisierung starten:** Klicken Sie auf "Vektorisierung starten"
5. **Ergebnisse:** SVG-Dateien werden im "output" Ordner gespeichert

## ✨ Features

- ✅ **Unterstützte Formate:** PNG, JPG, JPEG, BMP, TIFF
- ✅ **Ausgabeformat:** SVG (Scalable Vector Graphics)
- ✅ **Benutzerfreundlich:** Einfache grafische Oberfläche
- ✅ **Eigenständig:** Keine Installation oder Abhängigkeiten erforderlich
- ✅ **Konfigurierbarer Threshold:** Für optimale Ergebnisse
- ✅ **Batch-Verarbeitung:** Mehrere Bilder gleichzeitig

## 🛠️ Für Entwickler

### Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/twoace/vectorizer.git
cd vectorizer

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Programm starten
python vectorizer.py
```

### Build-Prozess

Der Build läuft automatisch über **GitHub Actions**:
- Jeder Push startet automatisch den Windows-Build
- Die exe-Datei wird als Artifact bereitgestellt
- Bei Git-Tags wird automatisch ein Release erstellt

### Projektstruktur

```
vectorizer/
├── vectorizer.py           # Hauptprogramm (GUI)
├── build.py               # Build-Skript für exe-Erstellung
├── download_potrace.py    # Automatischer Potrace-Download
├── requirements.txt       # Python-Abhängigkeiten
├── version_info.txt       # Windows exe-Metadaten
├── icon.ico              # Programm-Icon
├── .github/workflows/    # GitHub Actions Konfiguration
└── README.md             # Diese Datei
```

## 🔧 Technische Details

- **GUI-Framework:** tkinter (Python Standard Library)
- **Bildverarbeitung:** Pillow (PIL)
- **Vektorisierung:** Potrace (automatisch heruntergeladen)
- **Build-Tool:** PyInstaller
- **CI/CD:** GitHub Actions

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

## 📞 Support

Bei Problemen oder Fragen:
- Erstellen Sie ein [Issue](https://github.com/twoace/vectorizer/issues)
- Beschreiben Sie das Problem detailliert
- Fügen Sie Screenshots bei, falls hilfreich

---

**Entwickelt mit ❤️ von Aaron's Software** 