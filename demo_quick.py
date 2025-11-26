"""
Demo rápido - Visualização de triângulo rotativo
Testa a instalação básica sem executar benchmarks completos
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

def demo_quick():
    """Demonstração rápida de 5 segundos"""
    print("=== DEMO: Triângulo Rotativo ===")
    print("Renderizando por 5 segundos...")
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5)
    
    rotation = 0
    clock = pygame.time.Clock()
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desenhar triângulo
        glPushMatrix()
        glRotatef(rotation, 0, 1, 0)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 1, 0)
        glColor3f(0, 1, 0)
        glVertex3f(-1, -1, 0)
        glColor3f(0, 0, 1)
        glVertex3f(1, -1, 0)
        glEnd()
        glPopMatrix()
        
        pygame.display.flip()
        rotation += 2
        clock.tick(60)
        frame_count += 1
    
    elapsed = time.time() - start_time
    print(f"\nFrames: {frame_count}")
    print(f"FPS médio: {frame_count / elapsed:.2f}")
    pygame.quit()


if __name__ == "__main__":
    demo_quick()

