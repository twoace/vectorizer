import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path
from download_potrace import download_potrace

def build_exe():
    """Erstellt die Windows exe-Datei mit PyInstaller"""
    
    print("========================================")
    print("    Bild Vektorisierer - Build")
    print("========================================")
    print()
    
    # Aktuelles Verzeichnis
    current_dir = Path(__file__).parent
    
    # Schritt 1: Potrace automatisch herunterladen
    print("Schritt 1: Potrace herunterladen...")
    if not download_potrace():
        print("[ERROR] Potrace konnte nicht heruntergeladen werden!")
        print("Bitte laden Sie es manuell herunter und versuchen Sie es erneut.")
        return False
    print()
    
    # Schritt 2: Prüfe ob potrace.exe vorhanden ist
    potrace_dir = current_dir / "potrace"
    potrace_exe = potrace_dir / "potrace.exe"
    
    if not potrace_exe.exists():
        print("[ERROR] potrace.exe nicht gefunden!")
        print("Bitte stellen Sie sicher, dass potrace.exe im potrace/ Ordner vorhanden ist.")
        return False
    
    print("[OK] potrace.exe gefunden!")
    print()
    
    # Schritt 3: PyInstaller Build
    print("Schritt 2: PyInstaller Build starten...")
    
    # PyInstaller Argumente für Cross-Platform Build
    args = [
        'vectorizer.py',
        '--onefile',
        '--windowed',
        '--name=BildVektorisierer',
        f'--add-data={potrace_dir}{os.pathsep}potrace',
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        '--clean',
        '--noconfirm'
    ]
    
    # Icon hinzufügen falls vorhanden
    icon_path = current_dir / "icon.ico"
    if icon_path.exists():
        args.append(f'--icon={icon_path}')
    
    print("PyInstaller Argumente:")
    for arg in args:
        print(f"  {arg}")
    print()
    
    try:
        print("Starte PyInstaller...")
        PyInstaller.__main__.run(args)
        
        # Prüfe welche Dateien erstellt wurden
        dist_dir = current_dir / 'dist'
        created_files = list(dist_dir.glob('*')) if dist_dir.exists() else []
        
        print(f"\nErstelle Dateien in dist/:")
        for file in created_files:
            print(f"  {file.name}")
        
        # Suche nach der ausführbaren Datei
        exe_candidates = [
            dist_dir / 'BildVektorisierer.exe',  # Windows
            dist_dir / 'BildVektorisierer',      # macOS/Linux
        ]
        
        exe_path = None
        for candidate in exe_candidates:
            if candidate.exists() and candidate.is_file():
                exe_path = candidate
                break
        
        if exe_path:
            # Wenn es nicht bereits eine .exe-Datei ist, umbenennen für Windows-Kompatibilität
            final_exe_path = dist_dir / 'BildVektorisierer.exe'
            if exe_path != final_exe_path:
                print(f"Benenne {exe_path.name} zu BildVektorisierer.exe um...")
                if final_exe_path.exists():
                    final_exe_path.unlink()
                shutil.copy2(exe_path, final_exe_path)
                exe_path = final_exe_path
            
            print()
            print("========================================")
            print("    Build erfolgreich abgeschlossen!")
            print("========================================")
            print()
            print(f"[OK] Die exe-Datei befindet sich in: {exe_path}")
            print(f"[OK] Dateigröße: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            print()
            print("[INFO] WICHTIG für Windows-Kompatibilität:")
            print("Die Datei wurde auf macOS erstellt, sollte aber auf Windows funktionieren.")
            print("PyInstaller erstellt plattformspezifische Binärdateien.")
            print()
            print("[SUCCESS] Sie können die exe-Datei jetzt an Ihren Kumpel senden!")
            print("[SUCCESS] Die exe-Datei ist vollständig eigenständig.")
            print()
            print("[WARNING] HINWEIS: Für echte Windows-Kompatibilität sollte das Programm")
            print("   idealerweise auf einem Windows-System oder mit Wine gebaut werden.")
            return True
        else:
            print("[ERROR] Keine ausführbare Datei wurde erstellt!")
            return False
            
    except Exception as e:
        print(f"[ERROR] Fehler beim Build: {e}")
        return False

def clean_build():
    """Löscht Build-Artefakte"""
    current_dir = Path(__file__).parent
    
    # Lösche Build-Verzeichnisse
    for dir_name in ['build', 'dist', '__pycache__']:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"[OK] {dir_name}/ gelöscht")
    
    # Lösche .spec Dateien
    for spec_file in current_dir.glob('*.spec'):
        spec_file.unlink()
        print(f"[OK] {spec_file.name} gelöscht")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        print("Lösche Build-Artefakte...")
        clean_build()
        print("[OK] Bereinigung abgeschlossen!")
    else:
        success = build_exe()
        if not success:
            sys.exit(1) 