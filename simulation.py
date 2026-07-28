import random

class Node():
    def __init__(self, radius, children, bodies, totalMass, centreOfMass):
        pass




def addBodies(numberOfBodies: int, height: int, width: int) -> list[tuple(int, int, float)]:
    allBodies = []
    for i in range(numberOfBodies):
        allBodies.append((random.randint(0, height), random.randint(0, width), random.random()))

    print ("BODIES MADE")

    return allBodies