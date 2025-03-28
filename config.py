import importlib

try:
    android = importlib.import_module("android")
    gl = importlib.import_module("OpenGL.GLES3")
except ImportError:
    gl = importlib.import_module("OpenGL.GL")
