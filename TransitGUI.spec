# -*- mode: python -*-
a = Analysis(['TransitGUI.py', 'TransitGUI.spec'],
             pathex=['C:\\Users\\tolito\\work\\school\\projects\\workspace\\spyder\\transit_gui'],
             hiddenimports=['atexit'],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          [('assets/icon.png', 'assets\\icon.png',  'DATA')],
          name=os.path.join('dist', 'TransitGUI.exe'),
          debug=False,
          strip=None,
          upx=False,
          console=True,
		  icon='assets\\icon.ico')
