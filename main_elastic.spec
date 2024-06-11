# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_elastic.py'],
    pathex=[],
    binaries=[],
    datas=[('crutch_elastic.py', '.'), ('args_parse_elastic.py', '.'), ('class_elastic_request.py', '.'), ('styles_elasticv2.py', '.'), ('time_elastic.py', '.'), ('notnorm_body.py', '.'), ('notnorm_request.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main_elastic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['mp.ico'],
)
