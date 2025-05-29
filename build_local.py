#!/usr/bin/env python3
"""
Lokales Build-Skript für den Bild Vektorisierer
Erstellt plattformspezifische Builds
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Führt einen Befehl aus und zeigt den Fortschritt an"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} erfolgreich!")
            return True
        else:
            print(f"❌ Fehler bei {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Fehler bei {description}: {e}")
        return False

def check_dependencies():
    """Prüft, ob alle Abhängigkeiten installiert sind"""
    print("🔍 Prüfe Abhängigkeiten...")
    
    # Python-Pakete prüfen
    required_packages = ['PIL', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} verfügbar")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} fehlt")
    
    # PyInstaller prüfen
    try:
        import PyInstaller
        print("✅ PyInstaller verfügbar")
    except ImportError:
        print("❌ PyInstaller fehlt")
        print("   Installieren mit: pip install pyinstaller")
        return False
    
    if missing_packages:
        print(f"❌ Fehlende Pakete: {', '.join(missing_packages)}")
        print("   Installieren mit: pip install -r requirements.txt")
        return False
    
    return True

def setup_potrace():
    """Richtet potrace für das aktuelle System ein"""
    system = platform.system().lower()
    potrace_dir = Path("potrace")
    potrace_dir.mkdir(exist_ok=True)
    
    if system == 'darwin':  # macOS
        print("🍺 Suche potrace auf macOS...")
        potrace_paths = [
            '/opt/homebrew/bin/potrace',
            '/usr/local/bin/potrace'
        ]
        
        for path in potrace_paths:
            if os.path.exists(path):
                shutil.copy2(path, potrace_dir / 'potrace')
                print(f"✅ potrace kopiert von {path}")
                return True
        
        print("❌ potrace nicht gefunden")
        print("   Installieren mit: brew install potrace")
        return False
        
    elif system == 'linux':
        print("🐧 Suche potrace auf Linux...")
        potrace_paths = [
            '/usr/bin/potrace',
            '/usr/local/bin/potrace'
        ]
        
        for path in potrace_paths:
            if os.path.exists(path):
                shutil.copy2(path, potrace_dir / 'potrace')
                print(f"✅ potrace kopiert von {path}")
                return True
        
        print("❌ potrace nicht gefunden")
        print("   Installieren mit: sudo apt-get install potrace")
        return False
        
    elif system == 'windows':
        print("🪟 Lade potrace für Windows herunter...")
        potrace_exe = potrace_dir / 'potrace.exe'
        
        if potrace_exe.exists():
            print("✅ potrace.exe bereits vorhanden")
            return True
        
        # Hier könnte automatischer Download implementiert werden
        print("❌ potrace.exe nicht gefunden")
        print("   Laden Sie potrace manuell herunter:")
        print("   http://potrace.sourceforge.net/download.html")
        print(f"   Speichern Sie potrace.exe in: {potrace_dir}")
        return False
    
    return False

def build_app():
    """Erstellt die Anwendung mit PyInstaller"""
    print("🏗️ Erstelle Anwendung...")
    
    if not run_command("pyinstaller vectorizer.spec", "PyInstaller Build"):
        return False
    
    # Prüfe Ergebnis
    system = platform.system().lower()
    if system == 'darwin':
        app_path = Path("dist/BildVektorisierer.app")
        if app_path.exists():
            print(f"✅ macOS App erstellt: {app_path}")
            return True
    else:
        exe_name = "BildVektorisierer.exe" if system == 'windows' else "BildVektorisierer"
        exe_path = Path(f"dist/{exe_name}")
        if exe_path.exists():
            print(f"✅ Executable erstellt: {exe_path}")
            return True
    
    print("❌ Build-Ergebnis nicht gefunden")
    return False

def create_dmg():
    """Erstellt DMG für macOS"""
    if platform.system() != 'Darwin':
        return True  # Nur auf macOS relevant
    
    print("📦 Erstelle DMG...")
    
    # DMG-Ordner vorbereiten
    dmg_dir = Path("dmg")
    if dmg_dir.exists():
        shutil.rmtree(dmg_dir)
    dmg_dir.mkdir()
    
    # App kopieren
    app_src = Path("dist/BildVektorisierer.app")
    app_dst = dmg_dir / "BildVektorisierer.app"
    shutil.copytree(app_src, app_dst)
    
    # Applications-Link erstellen
    applications_link = dmg_dir / "Applications"
    if not applications_link.exists():
        os.symlink("/Applications", applications_link)
    
    # DMG erstellen
    dmg_cmd = 'hdiutil create -volname "Bild Vektorisierer" -srcfolder dmg -ov -format UDZO BildVektorisierer.dmg'
    return run_command(dmg_cmd, "DMG-Erstellung")

def main():
    print("🎨 Lokaler Build für Bild Vektorisierer")
    print("=" * 50)
    
    system_name = platform.system()
    print(f"🖥️  System: {system_name}")
    
    # Abhängigkeiten prüfen
    if not check_dependencies():
        print("\n❌ Build abgebrochen - Abhängigkeiten fehlen")
        return False
    
    # Potrace einrichten
    if not setup_potrace():
        print("\n❌ Build abgebrochen - potrace nicht verfügbar")
        return False
    
    # Build erstellen
    if not build_app():
        print("\n❌ Build fehlgeschlagen")
        return False
    
    # DMG für macOS erstellen
    if system_name == 'Darwin':
        if create_dmg():
            print("\n🎉 Build erfolgreich! DMG erstellt: BildVektorisierer.dmg")
        else:
            print("\n⚠️  App erstellt, aber DMG-Erstellung fehlgeschlagen")
    else:
        print(f"\n🎉 Build erfolgreich! Executable in dist/ Ordner")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 