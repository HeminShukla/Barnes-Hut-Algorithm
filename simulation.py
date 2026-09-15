import random
import math

class Body():
    def __init__(self, x, y, mass, speed=(0,0)):
        self.x = x
        self.y = y
        self.mass = mass
        self.speed = speed

class Node():
    def __init__(self, length, left, top, bodies: list[Body], totalMass=0, centreOfMass=(0, 0)):
        """Class representing nodes. 
        Recursively creates children nodes from the initial node until all required nodes are created. 
        """
        self.length = length
        self.left = left
        self.top = top
        self.children = []
        self.bodies = bodies
        self.totalMass = totalMass
        self.centreOfMass = centreOfMass

        if len(self.bodies) > 1: #Only need to create children nodes from here if the number of bodies in this node is greater than 1. Else, the node is small enough
            #We need to create 4 nodes for the four children from this node
            #To do that we first need to create the list of bodies that belong in each node from here
            #The four children nodes will be referred to as nw, ne, sw and se
            midX = left + length / 2
            midY = top + length / 2
            nwBodies = [body for body in self.bodies if 0 <= body.x <= midX and 0 <= body.y <= midY]
            neBodies = [body for body in self.bodies if 800 >= body.x >= midX and 0 <= body.y <= midY]
            swBodies = [body for body in self.bodies if 0 <= body.x <= midX and 800 >= body.y >= midY]
            seBodies = [body for body in self.bodies if 800 >= body.x >= midX and 800 >= body.y >= midY]

            nw = Node(length / 2, self.left, self.top, nwBodies)
            ne = Node(length/2, self.left + self.length / 2, self.top, neBodies)
            sw = Node(length / 2, self.left, self.top + self.length / 2, swBodies)
            se = Node(length/2, self.left + self.length / 2, self.top + self.length / 2, seBodies)
            self.children = [nw, ne, sw, se]

    def update(self):
        """
        Update the node's properties based on its children and bodies, 
        allowing for the entire node to be treated as a single body.
        """
        #Bodies will be in the format (x, y, mass) 
        
        if len(self.bodies) == 0:
            self.totalMass = 0
            self.centreOfMass = (self.left,self.top)
        else:
            self.totalMass = sum(body.mass for body in self.bodies)
            self.centreOfMass = (sum(body.x * body.mass for body in self.bodies) / self.totalMass, sum(body.y * body.mass for body in self.bodies) / self.totalMass)




def addBodies(numberOfBodies: int, height: int, width: int) -> list[Body]:
    """
    Function that adds a specified number of bodies to the simulation, each with random positions and masses.
    """
    allBodies = []
    for i in range(numberOfBodies):
        allBodies.append(Body(random.randint(0, width), random.randint(0, height), 0.3))

    return allBodies

def addCluster(numberOfBodies: int, height: int, width: int, numberOfClusters: int, clusterRadius: int) ->  list[Body]:
    """
    Function that adds a specified number of bodies to the simulation, within a specified number of clusters
    """
    allBodies = []
    clusterList = []
    for i in range(numberOfClusters): #Create the coordinates for the clusters around which the bodies will form
        clusterList.append((random.randint(0, width), random.randint(0, height)))

    #Now for each generated body, we will generate it a random distance away from a random cluster, at a random angle
    for i in range(numberOfBodies):
        currentCluster = random.choice(clusterList)
        distance = random.randint(0, clusterRadius)
        angle = random.randint(0, 360)
        bodyCoordinates = (currentCluster[0] + distance * math.cos(angle), currentCluster[1] + distance * math.sin(angle))
        allBodies.append(Body(bodyCoordinates[0], bodyCoordinates[1], 0.3))

    return allBodies


def allNodeCheckFunc(rootNode: Node, nodesToAdd: list[Node]) -> None:
    if rootNode.children != []:
        for child in rootNode.children:
            allNodeCheckFunc(child, nodesToAdd)
    else:
        nodesToAdd.append(rootNode)


allNodes = [] #Global variable to store all nodes in the quadtree for drawing purposes
theta = 1 #Global variable to store the value of theta, which will be updated by the user through the main program
def generateQuadrants(currentNode: Node, currentPos: tuple[int, int]) -> list[Node]:
    """
    Recursive function which adds all nodes to the global variable allNodes to be drawn on.
    """
    currentNode.update()
    if currentNode.children != [] and calculateQuotient(currentNode, currentPos) > theta:
        for child in currentNode.children:
            if child not in allNodes:
                allNodes.append(child)
                generateQuadrants(child, currentPos)


def calculateQuotient(currentNode: Node, currentPos: tuple[int, int]) -> float:
    """
    Function that calculates the quotient s/d for a particular node to determine if its children need to be examined.
    """
    try:
        s = currentNode.length
        d = math.hypot(currentNode.centreOfMass[0] - currentPos[0], currentNode.centreOfMass[1] - currentPos[1])
        return s / d
    except ZeroDivisionError:
        return 0

def calculateForce(currentNode: Node, body: Body) -> float:
    try:
        distanceToSource = math.hypot(abs(body.x - currentNode.centreOfMass[0]), abs(body.y - currentNode.centreOfMass[1]))
        force = 6.67 * (10 ** -11) * body.mass * currentNode.totalMass / (distanceToSource ** 2)
        return force
    except (ZeroDivisionError, MemoryError):
        return 0.0

def calculateBodyForce(bodyOne: Body, bodyTwo: Node) -> float:
    try:
        distanceToSource = math.hypot(abs(bodyOne.x - bodyTwo.centreOfMass[0]), abs(bodyOne.y - bodyTwo.centreOfMass[1]))
        force = 6.67 * (10 ** -11) * bodyOne.mass * bodyTwo.totalMass / (distanceToSource ** 2)
        return force
    except (ZeroDivisionError, MemoryError):
        return 0.0


def outOfBounds(body: Body, width: int, height: int) -> bool:
    """
    Function that checks if a body is out of bounds of the simulation area.
    """
    if body.x < 0 or body.x >= width or body.y < 0 or body.y >= height:
        return True
    else:
        return False