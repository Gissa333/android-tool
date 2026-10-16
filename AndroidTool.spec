# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
hidden = []

# تضمين mtkclient
if os.path.isdir('mtkclient'):
    datas.append(('mtkclient', 'mtkclient'))
    for root, dirs, files in os.walk('mtkclient'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'test', 'tests']]
        for f in files:
            if f.endswith('.py'):
                rel = os.path.relpath(os.path.join(root, f), '.')
                module = rel[:-3].replace(os.sep, '.')
                if not module.endswith('__init__'):
                    hidden.append(module)
                else:
                    hidden.append(module[:-9])

# مكتبات mtkclient
for pkg in ['usb', 'serial', 'Crypto', 'capstone']:
    try:
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
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
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