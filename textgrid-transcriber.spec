# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['textgrid-transcriber.py'],
             pathex=['C:\\Users\\rolan\\Desktop\\python_scripts\\textgrid-transcriber'],
             binaries=[('sendpraat.exe', '.')],
             datas=[
               ('praat-scripts/*', 'praat-scripts/'),
               ('img/*', 'img'),
               ('LICENSE', '.'),
               ('settings.ini', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='textgrid-transcriber',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\rolan\\Desktop\\python_scripts\\textgrid-transcriber\\img\\logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='textgrid-transcriber')
