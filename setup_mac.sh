#!/bin/bash

echo "🚀 Bild Vektorisierer - macOS Setup"
echo "Bereitet das Build-System für Windows Cross-Compilation vor"
echo "=========================================="
echo

# Prüfe Python-Installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installieren Sie Python 3 mit: brew install python"
    exit 1
fi

echo "✅ Python 3 gefunden: $(python3 --version)"

# Erstelle virtuelle Umgebung
echo "📦 Erstelle virtuelle Umgebung..."
python3 -m venv venv

# Aktiviere virtuelle Umgebung
echo "🔧 Aktiviere virtuelle Umgebung..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Aktualisiere pip..."
pip install --upgrade pip

# Installiere Abhängigkeiten
echo "📥 Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Abhängigkeiten erfolgreich installiert!"
else
    echo "❌ Fehler beim Installieren der Abhängigkeiten!"
    exit 1
fi

# Lade Potrace herunter
echo "⬇️ Lade Potrace herunter..."
python download_potrace.py

# Erstelle Windows exe
echo "🔨 Erstelle Windows exe-Datei..."
python build.py

if [ $? -eq 0 ]; then
    echo
    echo "🎉 BUILD ERFOLGREICH!"
    echo "=========================================="
    echo
    echo "📁 Die exe-Datei befindet sich in: dist/BildVektorisierer.exe"
    
    if [ -f "dist/BildVektorisierer.exe" ]; then
        SIZE=$(du -h "dist/BildVektorisierer.exe" | cut -f1)
        echo "📏 Dateigröße: $SIZE"
    fi
    
    echo
    echo "✅ Sie können die exe-Datei jetzt an Ihren Kumpel senden!"
    echo "✅ Die exe-Datei ist vollständig eigenständig."
    echo
    echo "Zum Testen der exe-Datei auf Windows:"
    echo "1. Kopieren Sie dist/BildVektorisierer.exe auf einen Windows-PC"
    echo "2. Doppelklicken Sie auf die Datei"
    echo "3. Das Programm sollte sofort starten"
    echo
else
    echo "❌ Build fehlgeschlagen!"
    exit 1
fi

echo "=========================================="
echo "🏁 Setup abgeschlossen!"
echo
echo "Für zukünftige Builds:"
echo "1. Aktivieren Sie die virtuelle Umgebung: source venv/bin/activate"
echo "2. Führen Sie den Build aus: python build.py"
echo "==========================================" 