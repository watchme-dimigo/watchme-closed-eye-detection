from cx_Freeze import setup, Executable

base = None

executables = [Executable('main.py', base=base)]

packages = ['idna']
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name='watchme_main',
    options=options,
    version='0.0.1',
    description='',
    executables=executables
)

# python3 setup.py build
