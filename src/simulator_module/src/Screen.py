import pygame
class Screen:
    """Handles display."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.running = True
        self.disp_surf = None
        self.background = (255,255,255)

    def on_init(self):
        pygame.init()
        print pygame.display.get_init()
        self.disp_surf = pygame.display.set_mode(self.size)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_render(self, blocks, arm, boundaries, string): #, rule_box):
        self.disp_surf.fill(self.background)
        for boundary in boundaries:
            pygame.draw.line(self.disp_surf, (0,0,0),boundary[0], boundary[1], 4)
        for block in blocks:
            block.renderShape(self.disp_surf)

        arm.renderShape(self.disp_surf)
        # rule_box.renderShape(self.disp_surf)
        font = pygame.font.SysFont("monospace", 15)
        label = [0,0]
        label[0] = font.render(string[0], 1, (0,255,0))
        label[1] = font.render(string[1], 1, (0,255,0))
        for i, st in enumerate(label):
            self.disp_surf.blit(st, (720, 50*i))
        pygame.display.update()
    def on_cleanup(self):
        pygame.quit()
