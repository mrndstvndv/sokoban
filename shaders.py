from OpenGL.GL import *

vertex_shader_src = """
#version 330 core
layout (location=0) in vec2 aPos;

uniform vec2 offset;

void main()
{
    gl_Position = vec4(aPos + offset, 0.0, 5.0);
}
"""

fragment_shader_src = """
#version 330 core

out vec4 FragColor;
uniform vec4 color;

void main(){
    FragColor = color; // dito po
}
"""


def compile_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())

    return shader


def create_shader_program():
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_src)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_src)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program).decode())

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

