import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import simulation
import math



#Initalise Pygame
pygame.init()

#Set up the main display
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Barnes-Hut")

#Set up the slider and the display for the textbox
thetaSlider = Slider(screen, 900, 100, 400, 50, min=0, max=2, step=0.05, colour=(211, 211, 211), handleColour=(64, 64, 64), initialValue=1.5)
font = pygame.font.SysFont(None, 50)

#Set up all of the buttons to toggle different features on and off
#First we will set up the subprograms and global variables that they will edit
treeToggle, netForceToggle, allForcesToggle, centresOfMassToggle = False, False, False, False

def toggleTree():
    global treeToggle
    treeToggle = not treeToggle

def toggleNetForce():
    global netForceToggle
    netForceToggle = not netForceToggle

def toggleAllForces():
     global allForcesToggle
     allForcesToggle = not allForcesToggle

def toggleCentresOfMass():
    global centresOfMassToggle
    centresOfMassToggle = not centresOfMassToggle

quadTreeButton = Button(screen, 900, 400, 400, 50, text="Show Quadtree", fontSize=50, inactiveColour=(128, 128, 128), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), onClick=toggleTree)
netForceButton = Button(screen, 900, 500, 400, 50, text="Show Net Force", fontSize=50, inactiveColour=(128, 128, 128), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), onClick=toggleNetForce)
allForcesButton = Button(screen, 900, 600, 400, 50, text="Show All Forces", fontSize=50, inactiveColour=(128, 128, 128), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), onClick=toggleAllForces)
centresOfMassButton = Button(screen, 900, 700, 400, 50, text="Show Centres of Mass", fontSize=45, inactiveColour=(128, 128, 128), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), onClick=toggleCentresOfMass)

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

    #Creating the slider allowing for theta to be changed by the user
    simulation.theta = round(thetaSlider.getValue(), 2)
    sliderOutput = font.render(f"{simulation.theta:.2f}", True, (255, 255, 255))
    thetaLabel = font.render("θ", True, (255, 255, 255))
    screen.blit(thetaLabel, (1100, 50))
    screen.blit(sliderOutput,(1075, 200))


    #Draw the main body on whom the net force needs to be calculated
    currentMousePosition = pygame.mouse.get_pos()
    mainBody.x, mainBody.y = currentMousePosition[0], currentMousePosition[1]
    pygame.draw.circle(screen, (255, 0, 0), currentMousePosition, mainBody.mass)

    #Drawing all of the quadrants in the quadtree onto the graphic
    simulation.allNodes = [rootNode]
    simulation.generateQuadrants(rootNode, currentMousePosition)
    if not treeToggle:
        for quadrant in simulation.allNodes:
            pygame.draw.rect(screen, (255, 255, 255), (quadrant.left, quadrant.top, quadrant.length, quadrant.length), 1)

    #Drawing all the individual bodies in
    for body in allBodies:
            pygame.draw.circle(screen, (211, 211, 211), (body.x, body.y), int(body.mass * 10))
            pygame.draw.circle(screen, (255, 255, 255), (body.x, body.y), int(body.mass * 9))

    totalForce = (0, 0) #This will be a tuple, representing the total force in the x and y direction as a vector
    for sourceOfForce in simulation.allNodes:
        #Each value in allNodes shows a source of a force that will be acting on the main body
        #So we want to constantly draw a line from that point where the force is acting to the main body
        try:
            if not centresOfMassToggle:
                pygame.draw.circle(
                                    screen,
                                    (0, 255, 0),
                                    (int(sourceOfForce.centreOfMass[0]), int(sourceOfForce.centreOfMass[1])),
                                    3
                                )
            currentForce = simulation.calculateForce(sourceOfForce, mainBody) * 10 ** 13 #We multiply by 10^13 almost arbitratily, to ensure it is visible to the user 
            angle = math.atan2(sourceOfForce.centreOfMass[1] - currentMousePosition[1], sourceOfForce.centreOfMass[0]-currentMousePosition[0])
            distance = math.hypot(sourceOfForce.centreOfMass[0] - currentMousePosition[0], sourceOfForce.centreOfMass[1]-currentMousePosition[1])
            totalForce = (totalForce[0] + currentForce * math.cos(angle), totalForce[1] + currentForce * math.sin(angle))
            if not allForcesToggle:
                pygame.draw.line(screen, (64, 64, 150),currentMousePosition, sourceOfForce.centreOfMass)
        except MemoryError:
            pass #This is because we need to multiple by 10^13 to make the forces visible, but this can cause a memory error if the force is too large

    #Now to draw the total force acting on the main body
    #This will be an arrow, and will be a different colour to differentiate it from the other lines showing forces that are influencing the main body
    tip = (currentMousePosition[0] + totalForce[0], currentMousePosition[1] + totalForce[1])
    if not netForceToggle:
        pygame.draw.line(screen, (255, 0, 0), currentMousePosition, tip)
        angle = math.atan2(tip[1] - currentMousePosition[1], tip[0]-currentMousePosition[0])
        left = (
            tip[0] - 15 * math.cos(angle - math.radians(25)),
            tip[1] - 15 * math.sin(angle - math.radians(25))
        )
    
        right = (
            tip[0] - 15 * math.cos(angle + math.radians(25)),
            tip[1] - 15 * math.sin(angle + math.radians(25))
        ) 
        pygame.draw.polygon(screen, (255, 0, 0), (tip, left, right))

    


    pygame_widgets.update(events)
    pygame.display.flip()



pygame.quit()