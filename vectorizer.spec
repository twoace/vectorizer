# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Bestimme das Betriebssystem
is_windows = sys.platform.startswith('win')
is_macos = sys.platform == 'darwin'
is_linux = sys.platform.startswith('linux')

# Potrace-Pfad bestimmen
if is_windows:
    potrace_src = 'potrace/potrace.exe'
    potrace_dst = 'potrace'
elif is_macos:
    potrace_src = 'potrace/potrace'
    potrace_dst = 'potrace'
else:  # Linux
    potrace_src = 'potrace/potrace'
    potrace_dst = 'potrace'

# Daten-Dateien
datas = []
if os.path.exists(potrace_src):
    datas.append((potrace_src, potrace_dst))
else:
    print(f"Warning: {potrace_src} not found, potrace will not be bundled")

# Icon-Pfad
icon_path = 'icon.ico' if os.path.exists('icon.ico') else None

block_cipher = None

a = Analysis(
    ['vectorizer.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'platform'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BildVektorisierer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

# macOS App Bundle
if is_macos:
    app = BUNDLE(
        exe,
        name='BildVektorisierer.app',
        icon=icon_path,
        bundle_identifier='com.aaron.bildvektorisierer',
        info_plist={
            'CFBundleName': 'Bild Vektorisierer',
            'CFBundleDisplayName': 'Bild Vektorisierer',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
            'NSDocumentsFolderUsageDescription': 'Diese App benötigt Zugriff auf Dokumente, um Bilder zu vektorisieren.',
            'NSDesktopFolderUsageDescription': 'Diese App benötigt Zugriff auf den Desktop, um Bilder zu vektorisieren.',
        },
    ) 