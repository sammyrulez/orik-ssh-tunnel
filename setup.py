from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Sam Reghenzi'

APP = ['orik_ssh.py']
DATA_FILES = ['dwarf-helmet.png', 'dwarf-helmet.icns']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'paramiko', 'cffi', 'cryptography', 'sshtunnel'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
