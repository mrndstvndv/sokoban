from config import SCALE, gl

vertex_shader_src = f"""
#version 330 core
layout (location=0) in vec2 aPos;

uniform vec2 offset;
uniform float scale;

void main()
{{
    gl_Position = vec4((aPos + offset)*scale, 0.0, {SCALE});
}}
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
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:
        raise RuntimeError(gl.glGetShaderInfoLog(shader).decode())

    return shader


def create_shader_program(vertex_shader_src: str, fragment_shader_src: str):
    vertex_shader = compile_shader(gl.GL_VERTEX_SHADER, vertex_shader_src)
    fragment_shader = compile_shader(gl.GL_FRAGMENT_SHADER, fragment_shader_src)

    shader_program = gl.glCreateProgram()
    gl.glAttachShader(shader_program, vertex_shader)
    gl.glAttachShader(shader_program, fragment_shader)
    gl.glLinkProgram(shader_program)

    if gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS) != gl.GL_TRUE:
        raise RuntimeError(gl.glGetProgramInfoLog(shader_program).decode())

    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return shader_program

