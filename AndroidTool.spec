# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
hidden = []

# تضمين مكتبات mtkclient بالكامل
mtk_packages = ['mtkclient', 'usb', 'serial', 'Crypto', 'capstone']
for pkg in mtk_packages:
    try:
        datas += collect_data_files(pkg)
        hidden += collect_submodules(pkg)
    except Exception:
        pass

# مكتبات مخفية أساسية
hidden += [
    'usb', 'usb.core', 'usb.util', 'usb.backend.libusb1',
    'serial', 'serial.tools.list_ports',
    'Crypto', 'Crypto.Cipher.AES',
    'capstone',
    'customtkinter',
    'PIL', 'PIL.Image', 'PIL.ImageTk',
    'PySide6', 'PySide6.QtCore', 'PySide6.QtWidgets',
    'PySide6.QtGui',
]

# تضمين mtkclient كامل كمجلد
if os.path.isdir('mtkclient'):
    datas.append(('mtkclient', 'mtkclient'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'test', 'unittest', 'matplotlib', 'numpy'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AndroidTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='AndroidTool',
)