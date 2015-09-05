import pygame
class RobotArm:
    def __init__(self, base_position, pincher_seperation, boundaries):
        self.base_width = 100
        self.base_height = 30
        self.pincher_width = 10
        self.pincher_height = 50
        self.colour = (0,0,255)
        self.base_position = base_position
        self.pincher_seperation = pincher_seperation
        self.boundaries = boundaries
        self.direction = []
        self.holding = None

    def getDirection(self, position):
        if self.base_position[0] == position[0] and self.base_position[1] == position[1]:
            self.direction = []
        else:
            self.direction.append((position[1] - self.base_position[1])/(position[0] - self.base_position[0]))
            self.direction.append(position[1] - self.direction[0]*position[0])

    def moveArm(self, position):
        self.getDirection(position)
        if self.base_position[0] == position[0] and self.base_position[1] == position[1]:
            return
        if self.base_position[0] < position[0]:
            self.base_position[0] += 1
        elif self.base_position[0] > position[0]:
            self.base_position[0] -= 1
        self.base_position[1] = self.direction[0]*self.base_position[0] + self.direction[1]

    def createBase(self):
        node_1 = self.base_position[0], self.base_position[1]
        node_2 = self.base_position[0] + self.base_width, self.base_position[1]
        node_3 = self.base_position[0] + self.base_width, self.base_position[1]-self.base_height
        node_4 = self.base_position[0], self.base_position[1] - self.base_height
        return (node_1, node_2, node_3, node_4)

    def createPinchers(self):
        #left pincher
        node_1 = (self.base_position[0], self.base_position[1],self.pincher_width, self.pincher_height)
        #right pincher
        node_2 = (self.base_position[0] + self.pincher_seperation, self.base_position[1], self.pincher_width, self.pincher_height)
        return (node_1, node_2)

    def closePinchers(self, distance = None):
        if distance == None:
            if self.pincher_seperation>self.pincher_width:
                self.pincher_seperation -= 1
        else:
            if self.pincher_seperation>distance:
                self.pincher_seperation -= 1

    def openPinchers(self):
        if self.pincher_seperation < self.base_width-self.pincher_width:
            self.pincher_seperation += 1

    def renderShape(self, surface):
        base_coord = self.createBase()
        pygame.draw.polygon(surface, self.colour, base_coord)
        pincher_coord = self.createPinchers()
        pygame.draw.rect(surface, self.colour, pincher_coord[0])
        pygame.draw.rect(surface, self.colour, pincher_coord[1])
