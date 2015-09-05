# Simulator module
import pygame
import time
import random as r
from Shape import Shape
from Block import Block
from RobotArm import RobotArm
from RuleBox import RuleBox
from Screen import Screen
class BlocksWorld:
    def __init__(self):
        self.screen = Screen(1024, 768)
        self.blocks = []
        self.shape = ("Prism", "Cube", "Cuboid")
        self.colour = ("Red", "Blue", "Green")
        self.size = ("Small" , "Medium", "Large")
        self.boundaries = [((0,402), (1024,402)),((700,0),(700,400))]
        self.table = 402
        self.wall = 700
        self.arm = RobotArm([300,300], 50, self.boundaries)
        self.position = []
        self.colliding_blocks = []

    def makeRandomBlocks(self):
        shape_vars = {"Prism": [30,30], "Cube":[30,30], "Cuboid" : [60,30]}
        size_vars = {"Small": [-5,-5], "Medium": [0,0],"Large": [30, 30]}
        colour_vars = {"Red": (255,0,0), "Green":(0,255,0), "Blue":(0,0,255)}
        #for i in range(0,4):
        rand_shape = "Cube"#r.choice(self.shape)
        rand_colour = "Blue"#r.choice(self.colour)
        rand_size = "Medium"#r.choice(self.size)
        width = shape_vars[rand_shape][0] + size_vars[rand_size][0]
        height = shape_vars[rand_shape][1] + size_vars[rand_size][1]
        colour = colour_vars[rand_colour]
        block_shape = Shape(rand_shape, (width, height))
        position = [485,100]#[r.randint(0,500), r.randint(0,300)]
        self.blocks.append(Block(0,block_shape, colour, rand_size, position, self.boundaries[0]))

        rand_shape = "Cuboid"#r.choice(self.shape)
        rand_colour = "Red"# r.choice(self.colour)
        rand_size = "Large"#r.choice(self.size)
        width = shape_vars[rand_shape][0] + size_vars[rand_size][0]
        height = shape_vars[rand_shape][1] + size_vars[rand_size][1]
        colour = colour_vars[rand_colour]
        block_shape = Shape(rand_shape, (width, height))
        position = [500,300]#[r.randint(0,500), r.randint(0,300)]
        self.blocks.append(Block(1,block_shape, colour, rand_size, position, self.boundaries[0]))

        self.position = [r.randint(100,600), r.randint(100,400)]
        for block in self.blocks:
            block.getDirection(self.position)

    def blockOverlapCheck(self):
        """Do not show this to anyone"""
        self.colliding_blocks = []
        for block in self.blocks:
            for another_block in self.blocks:
                if block.index != another_block.index:
                    if block.rect.colliderect(another_block.rect):
                        if not self.colliding_blocks:
                            if block.index < another_block.index:
                                self.colliding_blocks.append((block, another_block))
                            else:
                                self.colliding_blocks.append((another_block, block))
                        else:
                            for t in self.colliding_blocks:
                                if block != t[0] and block != t[1]:
                                    if another_block != t[0] and another_block != t[1]:
                                        if block.index < another_block.index:
                                            self.colliding_blocks.append((block, another_block))
                                        else:
                                            self.colliding_blocks.append((another_block, block))

    def avoidBoundaries(self):
        for block in self.blocks:
            bx, by = block.position
            if by + block.shape.height > self.table:
                block.move("Up")

    def naturalFall(self):
        for block in self.blocks:
            bx, by = block.position
            if by + block.shape.height < self.table:
                block.move("Down")
                block.move("Down")
                block.move("Down")

    def moving_logic(self, block1, block2):
        b1x, b1y = block1.position
        b2x, b2y = block2.position
        # if the block1 is directly above
        print(b1x, b2x)
        print (b1y, b2y)
        if b1y + block1.shape.height > b2y and b1y < b2y:
            block1.move("Up")
            block1.move("Up")
            block1.move("Up")
            block2.move("Down")
        elif b1y < b2y+block2.shape.height and b1y > b2y:
            block2.move("Up")
            block2.move("Up")
            block2.move("Up")
            block1.move("Down")
        # if block 1 is left of 2
        thrs1 = float(b1x + block1.shape.width -b2x)/float(block1.shape.width)
        thrs2 = float(b1x -b2x)/float(block1.shape.width)
        print (thrs1, thrs2)
        if b1x + block1.shape.width > b2x and b1x < b2x and thrs1 < 0.55:
            block2.move("Right")
            block1.move("Left")
        elif b1x < b2x + block2.shape.width and b1x > b2x and thrs2 < 0.55:
            block1.move("Right")
            block2.move("Left")
        # Check if teh percentage of top block is above some threshold to see if it will fall
        # if 1 is right of 2
        # if 1 is left of 2
    def avoidCollisions(self):
        if len(self.colliding_blocks) > 0:
            for block_pairs in self.colliding_blocks:
                block1, block2 = block_pairs
                print (block1.index, block2.index)
                self.moving_logic(block1, block2)

    def on_loop(self):
        self.blockOverlapCheck()
        self.avoidCollisions()
        self.avoidBoundaries()
        self.naturalFall()
        # self.arm.moveArm(self.position)
        # self.arm.closePinchers()
    def on_execute(self):
        self.screen.on_init()
        self.makeRandomBlocks()
        self.screen.on_render(self.blocks, self.arm, self.boundaries)
        while(self.screen.running):
            for event in pygame.event.get():
                self.screen.on_event(event)
            self.on_loop()
            self.screen.on_render(self.blocks, self.arm, self.boundaries)
            pygame.time.wait(5)
        self.screen.on_cleanup()

if __name__ == "__main__":
    display = BlocksWorld()
    display.on_execute()
