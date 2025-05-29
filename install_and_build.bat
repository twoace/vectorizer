@echo off
echo ========================================
echo    Bild Vektorisierer - Installation
echo    Vollautomatischer Build für Windows
echo ========================================
echo.

echo Schritt 1: Python-Abhängigkeiten installieren...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo FEHLER: Abhängigkeiten konnten nicht installiert werden!
    echo Stellen Sie sicher, dass Python und pip installiert sind.
    pause
    exit /b 1
)
echo ✓ Abhängigkeiten erfolgreich installiert!
echo.

echo Schritt 2: Potrace automatisch herunterladen...
python download_potrace.py
if %errorlevel% neq 0 (
    echo WARNUNG: Automatischer Potrace-Download fehlgeschlagen.
    echo Das Build-Skript wird es nochmals versuchen.
)
echo.

echo Schritt 3: Windows exe erstellen...
python build.py
if %errorlevel% neq 0 (
    echo FEHLER: Build fehlgeschlagen!
    pause
    exit /b 1
)
echo.

echo ========================================
echo    Installation abgeschlossen!
echo ========================================
echo.
echo ✓ Die exe-Datei befindet sich in: dist\BildVektorisierer.exe
echo ✓ Die exe-Datei ist vollständig eigenständig
echo ✓ Keine weiteren Dateien erforderlich
echo.
echo Sie können jetzt:
echo 1. Die exe-Datei an Ihren Kumpel senden
echo 2. Die exe-Datei direkt verwenden
echo.
echo Zum Testen können Sie die exe-Datei doppelklicken.
echo.
pause 