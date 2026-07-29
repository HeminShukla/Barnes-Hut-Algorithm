import pygame
import simulation


#Initalise Pygame
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Barnes-Hut")

#First we will add all the bodies
allBodies = simulation.addBodies(10, 800, 800)
mainBody = simulation.Body(400, 400, 10) #This is the main body on whom the net force needs to be calculated

#Create the quadtree
rootNode = simulation.Node(800, 0, 0, allBodies)
allNodes = [rootNode]

def generateQuadrants(currentNode: simulation.Node) -> list[simulation.Node]:
    """
    Recursive function which adds all nodes to the global variable allNodes to be drawn on.
    """
    if currentNode.children != []:
        for child in currentNode.children:
            allNodes.append(child)
            generateQuadrants(child)

generateQuadrants(rootNode)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))


    #Drawing all of the quadrants in the quadtree onto the graphic
    for quadrant in allNodes:
        pygame.draw.rect(screen, (255, 255, 255), (quadrant.left, quadrant.top, quadrant.length, quadrant.length), 1)

    for body in allBodies:
            pygame.draw.circle(screen, (211, 211, 211), (body.x, body.y), int(body.mass * 10))
            pygame.draw.circle(screen, (255, 100, 100), (body.x, body.y), int(body.mass * 9))

    
    #Draw the main body on whom the net force needs to be calculated
    pygame.draw.circle(screen, (255, 0, 0), (mainBody.x, mainBody.y), mainBody.mass)

    pygame.display.flip()




pygame.quit()