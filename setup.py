import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['img', 'praat-scripts', 'sendpraat.exe', 'LICENSE', 'settings.ini']

packages = ['os', 'configparser', 'psutil', 'sys', 'subprocess', 're', 'time']
build_exe_options = {"packages": packages, "include_files":includefiles}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
  base = "Win32GUI"

setup(name = "SISII-Autómata",
  version = "2.2",
  description = "Revisar y corregir TextGrids",
  options = {"build_exe": build_exe_options},
  executables = [Executable("textgrid-transcriber.py", base=base, target_name='TextGrid-transcriber', icon=r'img\logo.ico')])