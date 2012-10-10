# -*- mode: python -*-
a = Analysis(['TransitGUI.py'],
             pathex=['C:\\Users\\tolito\\work\\school\\projects\\workspace\\spyder\\transit-gui','C:\\Users\\tolito\\work\\school\\projects\\workspace\\spyder\\transit-lib'],
             hiddenimports=['atexit','matplotlib','scipy','transitlib'],
             hookspath=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\TransitGUI', 'Transit.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True,
		  icon='assets\\icon.ico')
		  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + [('assets/icon.png', 'assets\\icon.png',  'DATA'),('data/README', 'data\\README',  'DATA'),('config/README', 'config\\README',  'DATA')],
               strip=None,
               upx=True,
               name=os.path.join('dist\win32\Transit', 'bin'))