import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import simulation



#Initalise Pygame
pygame.init()

screen = pygame.display.set_mode((1050, 800))
pygame.display.set_caption("Barnes-Hut")


thetaSlider = Slider(screen, 850, 100, 50, 600, min=0, max=2, step=0.05, colour=(211, 211, 211), handleColour=(64, 64, 64), initialValue=1.5, vertical=True, reverse=False)
sliderOutput = TextBox(screen, 950, 350, 50, 50, fontSize=15)
sliderOutput.disable()

#First we will add all the bodies
allBodies = simulation.addBodies(100, 800, 800)
mainBody = simulation.Body(400, 400, 2) #This is the main body on whom the net force needs to be calculated

#Create the quadtree
rootNode = simulation.Node(800, 0, 0, allBodies)


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    simulation.theta = round(thetaSlider.getValue(), 2)
    sliderOutput.setText(simulation.theta)

    #Draw the main body on whom the net force needs to be calculated
    currentMousePosition = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 0, 0), currentMousePosition, mainBody.mass)

    #Drawing all of the quadrants in the quadtree onto the graphic
    simulation.allNodes = [rootNode]
    simulation.generateQuadrants(rootNode, currentMousePosition)
    for quadrant in simulation.allNodes:
        pygame.draw.rect(screen, (255, 255, 255), (quadrant.left, quadrant.top, quadrant.length, quadrant.length), 1)

    for body in allBodies:
            pygame.draw.circle(screen, (211, 211, 211), (body.x, body.y), int(body.mass * 10))
            pygame.draw.circle(screen, (255, 100, 100), (body.x, body.y), int(body.mass * 9))

    

    pygame_widgets.update(events)
    pygame.display.flip()



pygame.quit()