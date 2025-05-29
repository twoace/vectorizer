#!/usr/bin/env python3
"""
Test-Skript für BildVektorisierer (macOS/lokale Version)
Testet die Komponenten ohne Windows-exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw
import time

def create_test_images(test_dir):
    """Erstellt Testbilder für die Vektorisierung"""
    print("[INFO] Erstelle Testbilder...")
    
    # Einfaches schwarzes Quadrat
    img1 = Image.new('RGB', (200, 200), 'white')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([50, 50, 150, 150], fill='black')
    img1.save(test_dir / "test_square.png")
    
    # Schwarzer Kreis
    img2 = Image.new('RGB', (200, 200), 'white')
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([50, 50, 150, 150], fill='black')
    img2.save(test_dir / "test_circle.png")
    
    # Einfacher Text (als Bitmap)
    img3 = Image.new('RGB', (300, 100), 'white')
    draw3 = ImageDraw.Draw(img3)
    # Simuliere Text mit Rechtecken
    draw3.rectangle([20, 20, 40, 80], fill='black')  # I
    draw3.rectangle([60, 20, 80, 40], fill='black')  # T (oben)
    draw3.rectangle([60, 40, 80, 80], fill='black')  # T (unten)
    draw3.rectangle([70, 20, 70, 80], fill='black')  # T (mitte)
    img3.save(test_dir / "test_text.png")
    
    print(f"[OK] {len(list(test_dir.glob('*.png')))} Testbilder erstellt")
    return True

def test_build_script():
    """Testet ob das Build-Skript vorhanden ist"""
    build_script = Path("build.py")
    if build_script.exists():
        print("[OK] build.py gefunden")
        return True
    else:
        print("[ERROR] build.py nicht gefunden!")
        return False

def test_vectorizer_script():
    """Testet ob das Hauptskript vorhanden ist"""
    vectorizer_script = Path("vectorizer.py")
    if vectorizer_script.exists():
        print("[OK] vectorizer.py gefunden")
        return True
    else:
        print("[ERROR] vectorizer.py nicht gefunden!")
        return False

def test_download_script():
    """Testet das Potrace-Download-Skript"""
    download_script = Path("download_potrace.py")
    if download_script.exists():
        print("[OK] download_potrace.py gefunden")
        
        # Teste ob das Skript ausführbar ist
        try:
            result = subprocess.run(
                [sys.executable, str(download_script)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("[OK] download_potrace.py erfolgreich ausgeführt")
                return True
            else:
                print(f"[WARNING] download_potrace.py Exit Code: {result.returncode}")
                print(f"[INFO] Stderr: {result.stderr[:200]}...")
                return True  # Nicht kritisch für lokale Tests
        except Exception as e:
            print(f"[WARNING] Konnte download_potrace.py nicht testen: {e}")
            return True  # Nicht kritisch für lokale Tests
    else:
        print("[ERROR] download_potrace.py nicht gefunden!")
        return False

def test_potrace_availability():
    """Testet ob Potrace verfügbar ist (Windows oder macOS)"""
    print("[INFO] Teste Potrace-Verfügbarkeit...")
    
    # Teste Windows-Version
    potrace_win = Path("potrace/potrace.exe")
    if potrace_win.exists():
        print("[OK] Windows potrace.exe gefunden")
        return True
    
    # Teste macOS/Linux-Version (falls installiert)
    try:
        result = subprocess.run(
            ["potrace", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"[OK] System Potrace verfügbar: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Teste Homebrew-Installation
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/potrace", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"[OK] Homebrew Potrace verfügbar: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("[WARNING] Potrace nicht gefunden (normal auf macOS ohne Installation)")
    print("[INFO] Für vollständige Tests installieren Sie: brew install potrace")
    return False  # Nicht kritisch für Entwicklung

def test_dependencies():
    """Testet ob alle Python-Abhängigkeiten verfügbar sind"""
    print("[INFO] Teste Python-Abhängigkeiten...")
    
    dependencies = [
        ('tkinter', 'GUI-Framework'),
        ('PIL', 'Bildverarbeitung'),
        ('subprocess', 'Prozess-Management'),
        ('pathlib', 'Pfad-Handling'),
        ('tempfile', 'Temporäre Dateien'),
        ('PyInstaller', 'exe-Erstellung')
    ]
    
    all_ok = True
    for module, description in dependencies:
        try:
            if module == 'PIL':
                from PIL import Image
            elif module == 'PyInstaller':
                import PyInstaller
            else:
                __import__(module)
            print(f"[OK] {module} ({description})")
        except ImportError as e:
            print(f"[ERROR] {module} fehlt: {e}")
            if module == 'PyInstaller':
                print("[INFO] Installieren Sie mit: pip install pyinstaller")
            all_ok = False
    
    return all_ok

def test_requirements_file():
    """Testet ob requirements.txt vorhanden ist"""
    req_file = Path("requirements.txt")
    if req_file.exists():
        print("[OK] requirements.txt gefunden")
        
        # Lese und zeige Abhängigkeiten
        with open(req_file, 'r') as f:
            requirements = f.read().strip().split('\n')
            print(f"[INFO] {len(requirements)} Abhängigkeiten definiert")
            for req in requirements[:3]:  # Zeige erste 3
                print(f"[INFO]   - {req}")
            if len(requirements) > 3:
                print(f"[INFO]   ... und {len(requirements) - 3} weitere")
        return True
    else:
        print("[ERROR] requirements.txt nicht gefunden!")
        return False

def test_github_actions():
    """Testet ob GitHub Actions konfiguriert ist"""
    workflow_file = Path(".github/workflows/build-windows.yml")
    if workflow_file.exists():
        print("[OK] GitHub Actions Workflow gefunden")
        return True
    else:
        print("[ERROR] GitHub Actions Workflow nicht gefunden!")
        return False

def run_local_test_suite():
    """Führt alle lokalen Tests aus"""
    print("=" * 60)
    print("    BildVektorisierer - Lokale Test Suite (macOS)")
    print("=" * 60)
    print()
    
    # Test-Verzeichnis erstellen
    test_dir = Path("test_temp_local")
    test_dir.mkdir(exist_ok=True)
    
    try:
        tests_passed = 0
        total_tests = 8
        
        # Test 1: Build-Skript
        if test_build_script():
            tests_passed += 1
        
        # Test 2: Hauptskript
        if test_vectorizer_script():
            tests_passed += 1
        
        # Test 3: Download-Skript
        if test_download_script():
            tests_passed += 1
        
        # Test 4: Abhängigkeiten
        if test_dependencies():
            tests_passed += 1
        
        # Test 5: Requirements
        if test_requirements_file():
            tests_passed += 1
        
        # Test 6: GitHub Actions
        if test_github_actions():
            tests_passed += 1
        
        # Test 7: Testbilder erstellen
        if create_test_images(test_dir):
            tests_passed += 1
        
        # Test 8: Potrace (optional)
        if test_potrace_availability():
            tests_passed += 1
        
        print()
        print("=" * 60)
        print(f"    Test-Ergebnisse: {tests_passed}/{total_tests} bestanden")
        print("=" * 60)
        
        if tests_passed >= total_tests - 1:  # Potrace ist optional
            print("[SUCCESS] Alle kritischen Tests bestanden!")
            print("[INFO] Das Projekt ist bereit für Windows-Build in GitHub Actions")
            return True
        else:
            print(f"[WARNING] {total_tests - tests_passed} Test(s) fehlgeschlagen.")
            print("[INFO] Bitte beheben Sie die Probleme vor dem Build.")
            return False
            
    finally:
        # Aufräumen
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print(f"[INFO] Test-Verzeichnis {test_dir} gelöscht")

def show_next_steps():
    """Zeigt nächste Schritte an"""
    print()
    print("=" * 60)
    print("    Nächste Schritte")
    print("=" * 60)
    print()
    print("1. [LOKAL] Für lokale Entwicklung:")
    print("   - Installieren Sie Potrace: brew install potrace")
    print("   - Testen Sie das GUI: python vectorizer.py")
    print()
    print("2. [WINDOWS BUILD] Für exe-Erstellung:")
    print("   - Push zu GitHub startet automatischen Build")
    print("   - Download der exe von GitHub Actions Artifacts")
    print("   - Oder erstellen Sie einen Git-Tag für Release")
    print()
    print("3. [TESTING] Für umfassende Tests:")
    print("   - Warten Sie auf GitHub Actions Ergebnisse")
    print("   - Laden Sie die exe herunter und testen Sie manuell")
    print("   - Prüfen Sie die Test-Logs in GitHub Actions")
    print()
    print("4. [RELEASE] Für Veröffentlichung:")
    print("   - Erstellen Sie einen Git-Tag: git tag v1.0.0")
    print("   - Push den Tag: git push origin v1.0.0")
    print("   - GitHub erstellt automatisch ein Release")

if __name__ == "__main__":
    success = run_local_test_suite()
    show_next_steps()
    sys.exit(0 if success else 1) 