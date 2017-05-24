from cx_Freeze import setup, Executable
import os.path

setup(
    name = "Tester_AKB",
    version = "1.1",
    description = "Tester_AKB",
    executables = [Executable( os.path.abspath('Tester_AKB.py'))]
)

#C:\Python34\python.exe setup.py build
#C:\Python34\python.exe setup.py bdist_msi
