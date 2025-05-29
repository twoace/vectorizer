#!/usr/bin/env python3
"""
Test-Skript für den Build-Prozess auf Mac
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Führt einen Befehl aus und zeigt das Ergebnis an"""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    print(f"Befehl: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ ERFOLGREICH")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FEHLER")
        print(f"Exit Code: {e.returncode}")
        if e.stdout:
            print("Output:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False

def main():
    print("🚀 Bild Vektorisierer - Build Test")
    print("Testet den Build-Prozess auf macOS für Windows")
    print()
    
    # Prüfe Python-Version
    print(f"Python Version: {sys.version}")
    print(f"Arbeitsverzeichnis: {Path.cwd()}")
    print()
    
    # Schritt 1: Requirements installieren
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Installiere Python-Abhängigkeiten"):
        print("❌ Abhängigkeiten konnten nicht installiert werden!")
        return False
    
    # Schritt 2: Potrace herunterladen
    if not run_command([sys.executable, "download_potrace.py"], 
                      "Lade Potrace herunter"):
        print("⚠️ Potrace-Download fehlgeschlagen, aber Build wird trotzdem versucht")
    
    # Schritt 3: Build ausführen
    if not run_command([sys.executable, "build.py"], 
                      "Erstelle Windows exe-Datei"):
        print("❌ Build fehlgeschlagen!")
        return False
    
    # Schritt 4: Ergebnis prüfen
    exe_path = Path("dist/BildVektorisierer.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n🎉 BUILD ERFOLGREICH!")
        print(f"📁 Datei: {exe_path}")
        print(f"📏 Größe: {size_mb:.1f} MB")
        print(f"\n✅ Die exe-Datei kann jetzt an Ihren Kumpel gesendet werden!")
        return True
    else:
        print(f"\n❌ exe-Datei wurde nicht erstellt!")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print("🏁 Test abgeschlossen!")
    print(f"{'='*50}") 