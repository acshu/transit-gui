# -*- mode: python -*-
a = Analysis(['..\\..\\..\\Transit.py'],
             pathex=['C:\\Users\\tolito\\work\\school\\projects\\workspace\\spyder\\transit-gui','C:\\Users\\tolito\\work\\school\\projects\\workspace\\spyder\\transit-lib'],
             hiddenimports=['atexit','matplotlib','scipy','transitlib','scipy.special._ufuncs_cxx'],
             hookspath=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\', 'TAC-maker.exe'),
          debug=False,
          strip=None,
          upx=False,
          console=False,
		  icon='..\\..\\..\\assets\\icon.ico')
		  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + [('assets/icon.png', '..\\..\\..\\assets\\icon.png',  'DATA'),
                          ('data/README', '..\\..\\..\\data\\README',  'DATA'),
                          ('data/wasp10/curve.dat', '..\\..\\..\\data\\wasp10\\curve.dat',  'DATA'),
                          ('data/wasp10/wasp10.ini', '..\\..\\..\\data\\wasp10\\wasp10.ini',  'DATA'),
                          ('config/README', '..\\..\\..\\config\\README',  'DATA'),
                          ('config/temp/README', '..\\..\\..\\config\\temp\\README',  'DATA')],
               strip=None,
               upx=True,
               name=os.path.join('dist', 'bin'))