import os
from distutils.sysconfig import get_python_lib
import platform


DEBUG_FLAG = False
if os.getenv('UMA_DEBUG') == 'true':
    DEBUG_FLAG = True

datas = [('./data', 'data'),
        ('./lib/blockly', 'lib/blockly'),
        ('./lib/closure-library', 'lib/closure-library'),
        ('./lib/editor', 'lib/editor'),
        ('./qt/win/qt.conf', '.')]

a = Analysis(['./main.py'],
        pathex=['./'],
        binaries=None,
        datas=datas,
        hiddenimports=[],
        hookspath=['./hooks',],
        runtime_hooks=None,
        excludes=None,
        win_no_prefer_redirects=None,
        win_private_assemblies=None,
        cipher=None)

# Additional DLLs
tmp = []
arch = platform.architecture()[0]
if arch=='32bit':
    dll_path = os.path.join('dll', 'x86')
else:
    dll_path = os.path.join('dll', 'x64')

for dir_path, dir_names, file_names in os.walk(dll_path):
    for file_name in file_names:
        tmp.append(
                (
                    file_name,
                    os.path.join(os.getcwd(), dir_path, file_name),
                    'BINARY'
                    )
                )

# For conda
conda_dll_path = os.path.join(os.environ.get('CONDA_PREFIX'), 'Library', 'bin')
for dir_path, dir_names, file_names in os.walk(conda_dll_path):
    for file_name in file_names:
        if os.path.splitext(file_name)[1]=='.dll':
            tmp.append(
                    (
                        file_name,
                        os.path.join(dir_path, file_name),
                        'BINARY'
                        )
                    )

# TODO: Check if needed
# For Numpy MKL
# blacklist = ['mkl_rt.dll', 'tbb.dll', 'libmmd.dll', 'libifcoremd.dll']
# a.binaries = list(filter(lambda t:t[0] not in blacklist, a.binaries))
# numpy_dll_path = os.path.join(get_python_lib(), 'numpy', 'core')
# for dir_path, dir_names, file_names in os.walk(numpy_dll_path):
#     for file_name in file_names:
#         if os.path.splitext(file_name)[1]=='.dll':
#             tmp.append(
#                     (
#                         file_name,
#                         os.path.join(dir_path, file_name),
#                         'BINARY'
#                         )
#                     )

# TODO: Check if needed
# For Numpy OpenBLAS
# numpy_dll_path = os.path.join(get_python_lib(), 'numpy', '.libs')
# for dir_path, dir_names, file_names in os.walk(numpy_dll_path):
#     for file_name in file_names:
#         if os.path.splitext(file_name)[1]=='.dll':
#             tmp.append(
#                     (
#                         file_name,
#                         os.path.join(dir_path, file_name),
#                         'BINARY'
#                         )
#                     )

# For Scipy
scipy_dll_path = os.path.join(get_python_lib(), 'scipy', 'extra-dll')
for dir_path, dir_names, file_names in os.walk(scipy_dll_path):
    for file_name in file_names:
        if os.path.splitext(file_name)[1]=='.dll':
            tmp.append(
                    (
                        file_name,
                        os.path.join(dir_path, file_name),
                        'BINARY'
                        )
                    )

a.binaries += tmp

# Override QtWebEngineProcess.exe
for i, binary in enumerate(a.binaries):
    if r'QtWebEngineProcess.exe' in binary[1]:
        a.binaries[i] = (r'QtWebEngineProcess.exe', binary[1], 'BINARY')

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
        a.scripts,
        name='UMATracker-FilterGenerator',
        debug=DEBUG_FLAG,
        strip=None,
        upx=True,
        exclude_binaries=True,
        console=DEBUG_FLAG, icon='./icon/icon.ico')

coll = COLLECT(exe,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='UMATracker-FilterGenerator',
        debug=DEBUG_FLAG,
        strip=None,
        upx=True,
        console=DEBUG_FLAG, icon='./icon/icon.ico')
