import pygame
import simulation


#Initalise Pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Barnes-Hut")

#First we will add all the bodies
allBodies = simulation.addBodies(10, 800, 600)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for body in allBodies:
        pygame.draw.circle(screen, (255, 255, 255), (body[0], body[1]), 5)

    
    pygame.display.flip()




pygame.quit()