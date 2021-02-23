# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/lucbertin/Documents/5_Project/selenium_project/karim_localch/GUIapp2/src/main/python/main.py'],
             pathex=['/Users/lucbertin/Documents/5_Project/selenium_project/karim_localch/GUIapp2/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/lucbertin/.pyenv/versions/3.8.6/envs/localch-scraper-env/lib/python3.8/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/lucbertin/Documents/5_Project/selenium_project/karim_localch/GUIapp2/target/PyInstaller/fbs_pyinstaller_hook.py'],
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
          name='Localch-scraper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/lucbertin/Documents/5_Project/selenium_project/karim_localch/GUIapp2/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Localch-scraper')
app = BUNDLE(coll,
             name='Localch-scraper.app',
             icon='/Users/lucbertin/Documents/5_Project/selenium_project/karim_localch/GUIapp2/target/Icon.icns',
             bundle_identifier=None)
