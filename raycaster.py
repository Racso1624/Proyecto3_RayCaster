import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *

pygame.init()

screen = pygame.display.set_mode(
    (1600, 1200),
    pygame.OPENGL | pygame.DOUBLEBUF
)


vertex_shader = """
#version 460
layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0f);
}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)
glUseProgram(shader)


vertex_data = numpy.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0,
], dtype=numpy.float32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * 4,
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)





running = True

glClearColor(0.5, 1.0, 0.5, 1.0)

while running:
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False