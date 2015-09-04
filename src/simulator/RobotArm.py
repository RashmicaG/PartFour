class RobotArm:
    def __init__(self, width, height, position):
        self.base_width = 100
        self.base_height = 30
        self.pincher_width = 50
        self.position = position
        self.direction = []
        self.holding = None
    def getDirection(self, postion):
        if self.position == position:
            self.direction = []
        else:
            self.direction[0] = (position[1] - self.position[1])/(position[0] - self.position[0])
            self.direction[1] = position[1] - self.direction[0]*self.position[0]

    def moveBlock(self, position):
        if self.position[0] == position[0] and self.position[1] == position[1]:
            return
        if self.position[0] < position[0]:
            self.position[0] += 1
        elif self.position[0] > position[0]:
            self.position[0] -= 1
        self.position[1] = self.direction[0]*self.position[0] + self.direction[1]

    def createBase(self):
        node_1 = self.position[0], self.position[1]
        node_2 = self.position[0] + self.base_width, self.position[1]
        node_3 = self.position[0] + self.base_width, self.position[1]-self.base_height
        node_4 = self.position[0], self.position[1] - self.base_height
    def renderShape(self, surface):

        pygame.draw.polygon(surface, self.colour, (node_1, node_2, node_3, node_4), 2)
