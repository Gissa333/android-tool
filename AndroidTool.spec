# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# جمع بيانات mtkclient
mtk_datas = []
mtk_hidden = []

if os.path.isdir('mtkclient'):
    mtk_datas = collect_data_files('mtkclient', include_py_files=False)
    mtk_hidden = collect_submodules('mtkclient')

# مكتبات مخفية إضافية
hidden = [
    'usb', 'usb.core', 'usb.util', 'usb.backend.libusb1',
    'serial', 'serial.tools.list_ports',
    'Crypto', 'Crypto.Cipher.AES',
    'capstone',
    'customtkinter',
    'PIL', 'PIL.Image', 'PIL.ImageTk',
] + mtk_hidden

datas = [
    ('mtkclient', 'mtkclient'),
] + mtk_datas

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test', 'test', 'unittest',
        'matplotlib', 'numpy', 'scipy', 'pandas',
    ],
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