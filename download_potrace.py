import urllib.request
import zipfile
import os
import shutil
from pathlib import Path

def download_potrace():
    """Lädt Potrace für Windows herunter und extrahiert es"""
    
    # URLs für Potrace Windows Binärdateien
    potrace_url_64 = "https://potrace.sourceforge.net/download/1.16/potrace-1.16.win64.zip"
    potrace_url_32 = "https://potrace.sourceforge.net/download/1.16/potrace-1.16.win32.zip"
    
    # Versuche zuerst 64-bit Version
    potrace_url = potrace_url_64
    filename = "potrace-1.16.win64.zip"
    
    current_dir = Path(__file__).parent
    potrace_dir = current_dir / "potrace"
    potrace_dir.mkdir(exist_ok=True)
    
    # Prüfe ob potrace.exe bereits existiert
    if (potrace_dir / "potrace.exe").exists():
        print("[OK] potrace.exe bereits vorhanden!")
        return True
    
    try:
        print(f"Lade Potrace herunter von: {potrace_url}")
        
        # Download mit Progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded * 100) // total_size)
                print(f"\rDownload: {percent}%", end="", flush=True)
        
        urllib.request.urlretrieve(potrace_url, filename, show_progress)
        print("\n[OK] Download abgeschlossen!")
        
        # Extrahiere ZIP
        print("Extrahiere Potrace...")
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            # Finde potrace.exe in der ZIP
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('potrace.exe'):
                    # Extrahiere nur potrace.exe
                    with zip_ref.open(file_info) as source:
                        with open(potrace_dir / "potrace.exe", 'wb') as target:
                            shutil.copyfileobj(source, target)
                    print(f"[OK] {file_info.filename} extrahiert!")
                    break
            else:
                raise Exception("potrace.exe nicht in ZIP gefunden!")
        
        # Lösche ZIP-Datei
        os.unlink(filename)
        print("[OK] Temporäre Dateien gelöscht!")
        
        # Prüfe ob Extraktion erfolgreich war
        if (potrace_dir / "potrace.exe").exists():
            print("[OK] Potrace erfolgreich installiert!")
            return True
        else:
            raise Exception("Extraktion fehlgeschlagen!")
            
    except Exception as e:
        print(f"\n[ERROR] Fehler beim Download der 64-bit Version: {e}")
        
        # Versuche 32-bit Version
        try:
            print("Versuche 32-bit Version...")
            potrace_url = potrace_url_32
            filename = "potrace-1.16.win32.zip"
            
            urllib.request.urlretrieve(potrace_url, filename, show_progress)
            print("\n[OK] Download abgeschlossen!")
            
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith('potrace.exe'):
                        with zip_ref.open(file_info) as source:
                            with open(potrace_dir / "potrace.exe", 'wb') as target:
                                shutil.copyfileobj(source, target)
                        print(f"[OK] {file_info.filename} extrahiert!")
                        break
                else:
                    raise Exception("potrace.exe nicht in ZIP gefunden!")
            
            os.unlink(filename)
            
            if (potrace_dir / "potrace.exe").exists():
                print("[OK] Potrace (32-bit) erfolgreich installiert!")
                return True
            else:
                raise Exception("Extraktion fehlgeschlagen!")
                
        except Exception as e2:
            print(f"\n[ERROR] Fehler beim Download der 32-bit Version: {e2}")
            print("\nBitte laden Sie Potrace manuell herunter:")
            print("1. Gehen Sie zu: https://potrace.sourceforge.net/download.html")
            print("2. Laden Sie potrace-1.16.win64.zip oder potrace-1.16.win32.zip herunter")
            print("3. Extrahieren Sie potrace.exe in den 'potrace' Ordner")
            return False

if __name__ == "__main__":
    download_potrace() 