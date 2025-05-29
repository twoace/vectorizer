# Makefile für Bild Vektorisierer
# Für Mac-Benutzer zum Cross-Compilation für Windows

.PHONY: all build test clean install help

# Standard-Ziel
all: build

# Installiere Abhängigkeiten
install:
	@echo "📦 Installiere Python-Abhängigkeiten..."
	pip install -r requirements.txt
	@echo "✅ Abhängigkeiten installiert!"

# Lade Potrace herunter
potrace:
	@echo "⬇️ Lade Potrace herunter..."
	python download_potrace.py
	@echo "✅ Potrace heruntergeladen!"

# Erstelle Windows exe
build: install potrace
	@echo "🔨 Erstelle Windows exe-Datei..."
	python build.py
	@echo "🎉 Build abgeschlossen!"
	@echo "📁 exe-Datei: dist/BildVektorisierer.exe"

# Führe vollständigen Test durch
test:
	@echo "🧪 Führe Build-Test durch..."
	python test_build.py

# Lösche Build-Artefakte
clean:
	@echo "🧹 Lösche Build-Artefakte..."
	python build.py clean
	@echo "✅ Bereinigung abgeschlossen!"

# Zeige Hilfe
help:
	@echo "🚀 Bild Vektorisierer - Build-Befehle"
	@echo ""
	@echo "Verfügbare Befehle:"
	@echo "  make build    - Vollständiger Build (Standard)"
	@echo "  make test     - Build-Test mit detaillierten Logs"
	@echo "  make install  - Nur Abhängigkeiten installieren"
	@echo "  make potrace  - Nur Potrace herunterladen"
	@echo "  make clean    - Build-Artefakte löschen"
	@echo "  make help     - Diese Hilfe anzeigen"
	@echo ""
	@echo "Schnellstart:"
	@echo "  make build"
	@echo ""
	@echo "Die fertige exe-Datei befindet sich in: dist/BildVektorisierer.exe" 