import importlib

import pygame

try:
    android = importlib.import_module("android")
    gl = importlib.import_module("OpenGL.GLES3")
    context = pygame.GL_CONTEXT_PROFILE_ES
except ImportError:
    gl = importlib.import_module("OpenGL.GL")
    context = pygame.GL_CONTEXT_PROFILE_CORE

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
SCALE = 10
