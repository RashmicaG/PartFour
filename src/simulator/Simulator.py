# Simulator module
import pygame
import time
import random as r
from Shape import Shape
from Block import Block
from Screen import Screen
class BlocksWorld:
    def __init__(self):
        self.screen = Screen(1024, 768)
        self.blocks = []
        self.shape = ("Prism", "Cube", "Cuboid")
        self.colour = ("Red", "Blue", "Green")
        self.size = ("Small" , "Medium", "Large")
        self.arm = None
        self.position = []
    def makeRandomBlocks(self):
        #  shape, colour, size, position
        shape_vars = {"Prism": [30,30], "Cube":[30,30], "Cuboid" : [60,30]}
        size_vars = {"Small": [-15,-15], "Medium": [0,0],"Large": [30, 30]}
        colour_vars = {"Red": (255,0,0), "Green":(0,255,0), "Blue":(0,0,255)}
        for i in range(0,4):
            rand_shape = r.choice(self.shape)
            rand_colour = r.choice(self.colour)
            rand_size = r.choice(self.size)
            width = shape_vars[rand_shape][0] + size_vars[rand_size][0]
            height = shape_vars[rand_shape][1] + size_vars[rand_size][1]
            colour = colour_vars[rand_colour]
            block_shape = Shape(rand_shape, (width, height))
            self.blocks.append(Block(block_shape, colour, rand_size, [100+100*i, 400]))

        self.position = [r.randint(100,600), r.randint(100,400)]
        for block in self.blocks:
            block.getDirection(self.position)
    def on_loop(self):
        for block in self.blocks:
            block.moveBlock(self.position)

    def on_execute(self):
        self.screen.on_init()
        self.makeRandomBlocks()
        self.blocks[1].getDirection(self.position)

        while(self.screen.running):
            for event in pygame.event.get():
                self.screen.on_event(event)
            # self.on_loop()
            self.screen.on_render(self.blocks)
            #pygame.display.flip()
            pygame.time.wait(5)

        self.screen.on_cleanup()

if __name__ == "__main__":
    display = BlocksWorld()
    display.on_execute()
