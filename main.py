import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import simulation
import math



#Initalise Pygame
pygame.init()

#Set up the main display
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Barnes-Hut")

#Set up the slider and the display for the textbox
thetaSlider = Slider(screen, 900, 100, 400, 50, min=0, max=2, step=0.05, colour=(211, 211, 211), handleColour=(64, 64, 64), initialValue=1.0)
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
#allBodies = simulation.addCluster(50, 800, 800, 5, 10)
mainBody = simulation.Body(400, 400, 2) #This is the main body on whom the net force needs to be calculated

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

    #Create the quadtree, needs to be done every frame since the bodies are going to be moving around, and the quadtree needs to be updated to reflect this
    rootNode = simulation.Node(800, 0, 0, allBodies)

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
            if not simulation.outOfBounds(body, 800, 800):
                pygame.draw.circle(screen, (211, 211, 211), (body.x, body.y), int(body.mass * 10))
                pygame.draw.circle(screen, (255, 255, 255), (body.x, body.y), int(body.mass * 9))

    #Calculating the total force acting on the main body, and drawing lines to show the forces acting on it
    totalForce = (0, 0) #This will be a tuple, representing the total force in the x and y direction as a vector

    forceOnBodies = {} #This will be a dictionary mapping each body to the total force acting on it
    for currentBody in allBodies:
        forceOnBodies[currentBody] = (0, 0) #This will be a tuple, representing the total force in the x and y direction as a vector
        
    for sourceOfForce in simulation.allNodes:
        #Each value in allNodes shows a source of a force that will be acting on the main body
        #So we want to constantly draw a line from that point where the force is acting to the main body
        try:
            if set.intersection(set(sourceOfForce.children), set(simulation.allNodes)) == set()  and sourceOfForce.bodies != [] and sourceOfForce != rootNode: 
                #Checking that no node whose children are already being counted is also being counted and ensuring the root node is not counted twice
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
                if not allForcesToggle and sourceOfForce.totalMass != 0:
                    pygame.draw.line(screen, (64, 64, 150),currentMousePosition, sourceOfForce.centreOfMass)

        except MemoryError:
            pass #This is because we need to multiply by 10^13 to make the forces visible, but this can cause a memory error if the force is too large

    #Now we will calculate the total force acting on each body, and store it in the dictionary forceOnBodies            
    for currentBody in allBodies:
        if not simulation.outOfBounds(currentBody, 800, 800): 
            #We do not want to calculate the force acting on a body from itself, since this is not physically possible
            simulation.generateQuadrants(rootNode, (currentBody.x, currentBody.y))
            for sourceOfForce in simulation.allNodes:
                if currentBody not in sourceOfForce.bodies:
                    distanceOnBody = math.hypot(sourceOfForce.centreOfMass[0] - currentBody.x, sourceOfForce.centreOfMass[1]-currentBody.y)
                    if distanceOnBody > 0.3: #This is because if they get too close, they will simply collide, we can treat this as them merging them in a sense, since they will now just not react  to each other and stay close
                        forceOnBody = simulation.calculateForce(sourceOfForce, currentBody) #We do not times this by 10^13, since we want to see the actual forces acting on the bodies, not just a visual representation of them
                        angleOnBody = math.atan2(sourceOfForce.centreOfMass[1] - currentBody.y, sourceOfForce.centreOfMass[0]-currentBody.x)
                        totalForceOnBody = (forceOnBody * math.cos(angleOnBody), forceOnBody * math.sin(angleOnBody))
                        forceOnBodies[currentBody] = (forceOnBodies[currentBody][0] + totalForceOnBody[0], forceOnBodies[currentBody][1] + totalForceOnBody[1])

        

    #Now to move the bodies to reflect this movement
    for body in allBodies:
        #Firstly the body's position will be updated, using t he speed
        magnitude = 10**9
        acceleration = (magnitude * forceOnBodies[body][0] / body.mass, magnitude * forceOnBodies[body][1] / body.mass)
        #The velocity will be updated, derived from v = u + at, assuming t = 1 (per frame)
        body.speed = (body.speed[0] + acceleration[0], body.speed[1] + acceleration[1])
        body.x += body.speed[0]
        body.y += body.speed[1]
        
    

    """for body in allBodies:
        found = False
        for node in simulation.allNodes:
            if body in node.bodies:
                found = True
                break
        if found == False:
            pygame.draw.circle(screen, (255, 0, 0), (body.x, body.y), int(body.mass * 10))
            pygame.draw.circle(screen, (255, 255, 255), (body.x, body.y), int(body.mass * 9))

    allNodeCheck = [rootNode]
    simulation.allNodeCheckFunc(rootNode, allNodeCheck)
    neglectedNodes = (neglectedNode for neglectedNode in allNodeCheck if neglectedNode not in simulation.allNodes)
    for neglectedNode in neglectedNodes:
        pygame.draw.circle(
                            screen,
                            (255, 0, 0),
                            (int(neglectedNode.centreOfMass[0]+1), int(neglectedNode.centreOfMass[1]+1)),
                            3
                        )"""
    
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