from config import SCALE, gl

vertex_shader_src = f"""
#version 330 core
layout (location=0) in vec2 aPos;
layout (location=1) in vec4 aColor;

uniform vec2 offset;
uniform float scale;

out vec4 vertexColor;

void main()
{{
    gl_Position = vec4((aPos + offset)*scale, 0.0, {SCALE});
    vertexColor = aColor;
}}
"""

fragment_shader_src = """
#version 330 core

uniform vec4 color;
uniform float opacity;

in vec4 vertexColor;

out vec4 FragColor;

void main(){
    vec4 finalColor = vertexColor;
    finalColor.a = opacity != 0.0 ? opacity : vertexColor.a;
    FragColor = finalColor.a > 0.0 ? finalColor : color;
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
