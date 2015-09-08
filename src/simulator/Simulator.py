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
        for i in range(0,4):
            rand_shape = r.choice(self.shape)
            rand_colour = r.choice(self.colour)
            rand_size = r.choice(self.size)
            width = shape_vars[rand_shape][0] + size_vars[rand_size][0]
            height = shape_vars[rand_shape][1] + size_vars[rand_size][1]
            colour = colour_vars[rand_colour]
            block_shape = Shape(rand_shape, (width, height))
            position = [r.randint(0,500), r.randint(0,300)]
            self.blocks.append(Block(i,block_shape, colour, rand_size, position, self.boundaries[0]))

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

    def armCollide(self):
        (lpx, lpy, lpw, lph), (rpx, rpy, rpw, rph) = self.arm.pincher_positions
        abx, aby = self.arm.base_position
        abw, abh = (self.arm.base_width, self.arm.base_height)
        for block in self.blocks:
            bx, by = block.position
            bw, bh = block.shape.dimensions
            if block.shape.shape == "Prism":
                (l_m, l_c), (r_m, r_c) = self.prismBlockCollision(block)
                if self.arm.base_rect.colliderect(block.rect):
                    # base touching the tip
                    pass
                elif self.arm.lp_rect.colliderect(block.rect):
                    # left pincher pushing or pulling
                    pass
                elif self.arm.rp_rect.colliderect(block.rect):
                    # right pincher pushing or pulling
                    pass
                print "Prism"
            else:
                if self.arm.base_rect.colliderect(block.rect):
                    if by < aby+abh:
                        self.arm.move("Up")
                elif self.arm.lp_rect.colliderect(block.rect):
                    if by > lpy+lph-bh/16:
                        self.arm.move("Up")
                    elif bx+bw >= lpx and bx < lpx:
                        block.move("Left")
                        self.arm.move("Right")
                    elif bx <= lpx+lpw and bx+bw > lpx:
                        self.arm.move("Left")
                        block.move("Right")
                elif self.arm.rp_rect.colliderect(block.rect):
                    if by > rpy+rph-bh/16:
                        self.arm.move("Up")
                    elif rpx + rpw >= bx and rpx < bx:
                        self.arm.move("Left")
                        block.move("Right")
                    elif bx + bw >= rpx and bx < rpx:
                        self.arm.move("Right")
                        block.move("Left")
    def prismBlockCollision(self, block):
        (lpx, lpy, lpw, lph), (rpx, rpy, rpw, rph) = self.arm.pincher_positions
        abx, aby = self.arm.base_position
        abw, abh = (self.arm.base_width, self.arm.base_height)
        bx, by = block.position
        bw, bh = block.shape.dimensions
        #left line
        left_m = 2*bh/bw
        left_c = (by+bh) - left_m*bx
        #right line
        right_m = -2*bh/bw
        right_c = (by+bh) - right_m*(bx+bw)
        return ((left_m, left_c), (right_m, right_c))

    def avoidBoundaries(self):
        for block in self.blocks:
            bx, by = block.position
            if by + block.shape.height > self.table:
                block.move("Up")
            elif bx <= 1:
                block.move("Right")
            elif bx + block.shape.width >= self.wall:
                block.move("Left")

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
        falling = self.topBlockIsFalling(block1, block2)
        b1_on_right = self.b1OnRight(block1, block2)
        b2_on_right = self.b2OnRight(block1, block2)
        if falling == True:
            if b1_on_right == True:
                block1.move("Right")
                block2.move("Left")
            elif b2_on_right == True:
                block1.move("Left")
                block2.move("Right")
        else:
            if b1y == b2y:
                if (b1x + block1.shape.width) > b2x and b1x <= b2x:
                    block1.move("Left")
                    block2.move("Right")
                elif (b2x + block2.shape.width) > b1x and b2x <= b1x:
                    block2.move("Left")
                    block1.move("Right")
                else:
                    block2.move("Left")
                    block1.move("Right")

    def topAndBottomBlock(self, block1, block2):
        b1x, b1y = block1.position
        b2x, b2y = block2.position
        if b1y < b2y:
            topBlock = block1
            bottomBlock = block2
        elif b1y > b2y:
            topBlock = block2
            bottomBlock = block1
        else:
            topBlock = None
            bottomBlock = None
        return (topBlock, bottomBlock)

    def topBlockIsFalling(self, block1, block2):
        topBlock, bottomBlock = self.topAndBottomBlock(block1, block2)
        if topBlock != None and bottomBlock != None:
            b1x, b1y = topBlock.position
            b2x, b2y = bottomBlock.position
            if bottomBlock.shape.shape == "Prism":
                return True
            else:
                if topBlock.shape.width < bottomBlock.shape.width:

                    b1_on_right = self.b1OnRight(topBlock, bottomBlock)
                    if b1_on_right:
                        thrs = float(b2x - b1x + block2.shape.width)/float(block1.shape.width)
                    else:
                        thrs = float(b1x + block1.shape.width -b2x)/float(block1.shape.width)
                    if thrs > 0.5:
                        return False
                    else:
                        return True
                else:
                    t_mid = b1x + topBlock.shape.width/2
                    b_mid = b2x + bottomBlock.shape.width/2
                    thrs = abs(t_mid - b_mid)/float(bottomBlock.shape.width)
                    if thrs < 0.10:
                        return False
                    else:
                        return True
        else:
            return False

    def b2OnRight(self, block1, block2):
        b1x, b1y = block1.position
        b2x, b2y = block2.position
        b1w, b1h = block1.shape.dimensions
        b2w, b2h = block2.shape.dimensions
        if (b1x + float(b1w)/2.0) < (b2x + float(b2w)/2.0):
            return True
        else:
            return False

    def b1OnRight(self,block1, block2):
        b1x, b1y = block1.position
        b2x, b2y = block2.position
        b1w, b1h = block1.shape.dimensions
        b2w, b2h = block2.shape.dimensions
        if (b1x + float(b1w)/2.0) >= (b2x + float(b2w)/2.0) :
            return True
        else:
            return False

    def avoidCollisions(self):
        if len(self.colliding_blocks) > 0:
            for block_pairs in self.colliding_blocks:
                block1, block2 = block_pairs
                topBlock, bottomBlock = self.topAndBottomBlock(block1, block2)
                if topBlock != None and bottomBlock != None:
                    self.moving_logic(topBlock, bottomBlock)
                else:
                    self.moving_logic(block1, block2)

    def getConfiguration(self):
        config = []
        for block in self.blocks:
            bx, by = block.position
            if by + block.shape.height == self.table:
                config.append(-1)
            else:
                for dest_block in self.blocks:
                    dx, dy = dest_block.position
                    if block.index != dest_block.index:
                        if dy-1 <= by+block.shape.height:
                            if bx + block.shape.width/2 > dx and bx + block.shape.width/2 < dx + dest_block.shape.width:
                                config.append(dest_block.index)
                                break
        return config
    def armControl(self):
        armx, army = self.arm.base_position
        """
        Temporary control of arm. For testing and debugging purposes only.
        Real arm must be automated and not require user input.
        """
        if armx > 1 and armx + self.arm.base_width < self.wall:
            if army > 1 and army + self.arm.base_height + self.arm.pincher_height < self.table:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] == 1:
                    self.arm.move("Left")
                if keys[pygame.K_RIGHT] == 1:
                    self.arm.move("Right")
                if keys[pygame.K_UP] == 1:
                    self.arm.move("Up")
                if keys[pygame.K_DOWN] == 1:
                    self.arm.move("Down")
                if keys[pygame.K_a] == 1:
                    self.arm.grab("Close")
                if keys[pygame.K_s] == 1:
                    self.arm.grab("Open")
            elif army <= 1:
                self.arm.move("Down")
            elif army + self.arm.base_height + self.arm.pincher_height >= self.table:
                self.arm.move("Up")
        elif armx <= 1:
            self.arm.move("Right")
        elif armx + self.arm.base_width >= self.wall:
            self.arm.move("Left")



    def on_loop(self):
        self.blockOverlapCheck()
        self.avoidCollisions()
        self.avoidBoundaries()
        self.naturalFall()
        self.armControl()
        self.armCollide()
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
