# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['typuspocus\\__main__.py'],
             pathex=['Z:\\typuspocus'],
             binaries=[],
             datas=[],
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
          name='__main__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='windows\\typuspocus.ico')
coll = COLLECT(exe,
               Tree('typuspocus\\icons', prefix='typuspocus\\icons'),
               Tree('typuspocus\\music', prefix='typuspocus\\music'),
               Tree('typuspocus\\locale', prefix='typuspocus\\locale'),
               Tree('typuspocus\\sounds', prefix='typuspocus\\sounds'),
               Tree('typuspocus\\audiencia', prefix='typuspocus\\audiencia'),
               Tree('typuspocus\\escenario', prefix='typuspocus\\escenario'),
               a.binaries,
               a.zipfiles,
               a.datas + [
                   ('gpl-2.txt', 'gpl-2.txt', 'DATA'),
               ],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='__main__')





