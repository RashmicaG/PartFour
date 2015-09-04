import pygame
class Block:
    def __init__(self, shape, colour, size, position):
        self.shape = shape
        self.colour = colour
        self.size = size
        self.position = position
        self.direction = []
    def getShape(self):
        return self.shape

    def updatePosition(self, position):
        self.position = position

    def getDirection(self, position):
        if self.position == position:
            self.direction = []
        else:
            self.direction.append((position[1] - self.position[1])/(position[0] - self.position[0]))
            self.direction.append(position[1] - self.direction[0]*self.position[0])

    def moveBlock(self, position):
        if self.position[0] == position[0] and self.position[1] == position[1]:
            return
        if self.position[0] < position[0]:
            self.position[0] += 1
        elif self.position[0] > position[0]:
            self.position[0] -= 1
        self.position[1] = self.direction[0]*self.position[0] + self.direction[1]

    def renderShape(self, surface):
        node_1 = self.position[0],self.position[1]
        node_2 = self.position[0]+self.shape.width, self.position[1]
        if self.shape.shape == "Prism":
            node_3 = self.position[0]+self.shape.width/2, self.position[1] - self.shape.height
            pygame.draw.polygon(surface, self.colour,(node_1, node_2, node_3), 2)
        else:
            node_3 = self.position[0]+self.shape.width, self.position[1] - self.shape.height
            node_4 = self.position[0], self.position[1] - self.shape.height
            pygame.draw.polygon(surface, self.colour, (node_1, node_2, node_3, node_4), 2)
