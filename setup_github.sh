#!/bin/bash

echo "🚀 GitHub Actions Setup für Windows-exe Erstellung"
echo "=================================================="
echo

# Prüfe ob Git installiert ist
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert!"
    echo "Bitte installieren Sie Git: https://git-scm.com/"
    exit 1
fi

echo "✅ Git gefunden: $(git --version)"

# Initialisiere Git Repository falls noch nicht vorhanden
if [ ! -d ".git" ]; then
    echo "📦 Initialisiere Git Repository..."
    git init
    git branch -M main
else
    echo "✅ Git Repository bereits vorhanden"
fi

# Füge alle Dateien hinzu
echo "📁 Füge Dateien hinzu..."
git add .

# Erstelle Commit
echo "💾 Erstelle Commit..."
git commit -m "Initial commit: Bild Vektorisierer mit GitHub Actions"

echo
echo "🎯 Nächste Schritte:"
echo "1. Erstellen Sie ein Repository auf GitHub.com"
echo "2. Führen Sie diese Befehle aus:"
echo
echo "   git remote add origin https://github.com/IHR_USERNAME/Vectorizer.git"
echo "   git push -u origin main"
echo
echo "3. GitHub Actions startet automatisch und erstellt die Windows-exe!"
echo
echo "📥 exe-Datei herunterladen:"
echo "   → Gehen Sie zu GitHub.com → Ihr Repository → Actions → Artifacts"
echo
echo "🎉 Für Releases (empfohlen):"
echo "   git tag v1.0.0"
echo "   git push origin v1.0.0"
echo "   → Automatisches Release mit exe-Datei!"
echo
echo "✅ Setup abgeschlossen!" 