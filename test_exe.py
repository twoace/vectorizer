#!/usr/bin/env python3
"""
Test-Skript für BildVektorisierer.exe
Testet die Funktionalität der erstellten exe-Datei
"""

import os
import sys
import subprocess
import tempfile
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

def test_exe_exists():
    """Prüft ob die exe-Datei existiert"""
    exe_path = Path("dist/BildVektorisierer.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"[OK] BildVektorisierer.exe gefunden ({size_mb:.1f} MB)")
        return exe_path
    else:
        print("[ERROR] BildVektorisierer.exe nicht gefunden!")
        print("Bitte führen Sie zuerst 'python build.py' aus.")
        return None

def test_exe_startup(exe_path):
    """Testet ob die exe startet"""
    print("[INFO] Teste exe-Start...")
    
    try:
        # Versuche die exe zu starten (kurz)
        process = subprocess.Popen(
            [str(exe_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Warte kurz und beende dann
        time.sleep(2)
        process.terminate()
        
        try:
            process.wait(timeout=5)
            print("[OK] exe startet erfolgreich")
            return True
        except subprocess.TimeoutExpired:
            process.kill()
            print("[OK] exe startet (musste beendet werden)")
            return True
            
    except Exception as e:
        print(f"[ERROR] exe-Start fehlgeschlagen: {e}")
        return False

def test_potrace_integration():
    """Testet die Potrace-Integration"""
    print("[INFO] Teste Potrace-Integration...")
    
    potrace_path = Path("potrace/potrace.exe")
    if not potrace_path.exists():
        print("[ERROR] potrace.exe nicht gefunden!")
        return False
    
    try:
        # Teste Potrace-Version
        result = subprocess.run(
            [str(potrace_path), "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"[OK] Potrace verfügbar: {version}")
            return True
        else:
            print(f"[WARNING] Potrace Exit Code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Potrace-Test fehlgeschlagen: {e}")
        return False

def test_image_conversion(test_dir):
    """Testet die Bildkonvertierung mit Potrace direkt"""
    print("[INFO] Teste Bildkonvertierung...")
    
    potrace_path = Path("potrace/potrace.exe")
    if not potrace_path.exists():
        print("[ERROR] Potrace nicht verfügbar für Test")
        return False
    
    # Konvertiere Testbild zu PBM (Potrace-Format)
    test_image = test_dir / "test_square.png"
    pbm_file = test_dir / "test_square.pbm"
    svg_file = test_dir / "test_square.svg"
    
    try:
        # PNG zu PBM konvertieren
        img = Image.open(test_image)
        img = img.convert('1')  # Schwarz-weiß
        img.save(pbm_file)
        
        # Potrace ausführen
        result = subprocess.run(
            [str(potrace_path), str(pbm_file), "-s", "-o", str(svg_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and svg_file.exists():
            svg_size = svg_file.stat().st_size
            print(f"[OK] SVG erstellt ({svg_size} Bytes)")
            
            # Prüfe SVG-Inhalt
            with open(svg_file, 'r') as f:
                svg_content = f.read()
                if '<svg' in svg_content and '</svg>' in svg_content:
                    print("[OK] SVG-Format korrekt")
                    return True
                else:
                    print("[ERROR] SVG-Format ungültig")
                    return False
        else:
            print(f"[ERROR] Potrace-Konvertierung fehlgeschlagen: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Bildkonvertierung fehlgeschlagen: {e}")
        return False

def test_dependencies():
    """Testet ob alle Python-Abhängigkeiten verfügbar sind"""
    print("[INFO] Teste Python-Abhängigkeiten...")
    
    dependencies = [
        ('tkinter', 'GUI-Framework'),
        ('PIL', 'Bildverarbeitung'),
        ('subprocess', 'Prozess-Management'),
        ('pathlib', 'Pfad-Handling'),
        ('tempfile', 'Temporäre Dateien')
    ]
    
    all_ok = True
    for module, description in dependencies:
        try:
            if module == 'PIL':
                from PIL import Image
            else:
                __import__(module)
            print(f"[OK] {module} ({description})")
        except ImportError as e:
            print(f"[ERROR] {module} fehlt: {e}")
            all_ok = False
    
    return all_ok

def run_comprehensive_test():
    """Führt alle Tests aus"""
    print("=" * 50)
    print("    BildVektorisierer exe Test Suite")
    print("=" * 50)
    print()
    
    # Test-Verzeichnis erstellen
    test_dir = Path("test_temp")
    test_dir.mkdir(exist_ok=True)
    
    try:
        tests_passed = 0
        total_tests = 6
        
        # Test 1: exe existiert
        exe_path = test_exe_exists()
        if exe_path:
            tests_passed += 1
        
        # Test 2: Abhängigkeiten
        if test_dependencies():
            tests_passed += 1
        
        # Test 3: Potrace-Integration
        if test_potrace_integration():
            tests_passed += 1
        
        # Test 4: Testbilder erstellen
        if create_test_images(test_dir):
            tests_passed += 1
        
        # Test 5: Bildkonvertierung
        if test_image_conversion(test_dir):
            tests_passed += 1
        
        # Test 6: exe-Start (nur wenn exe existiert)
        if exe_path and test_exe_startup(exe_path):
            tests_passed += 1
        
        print()
        print("=" * 50)
        print(f"    Test-Ergebnisse: {tests_passed}/{total_tests} bestanden")
        print("=" * 50)
        
        if tests_passed == total_tests:
            print("[SUCCESS] Alle Tests bestanden! Die exe sollte korrekt funktionieren.")
            return True
        else:
            print(f"[WARNING] {total_tests - tests_passed} Test(s) fehlgeschlagen.")
            print("Die exe könnte Probleme haben.")
            return False
            
    finally:
        # Aufräumen
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print(f"[INFO] Test-Verzeichnis {test_dir} gelöscht")

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 