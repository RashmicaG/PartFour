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
        self.disp_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_render(self, blocks, arm, boundaries): #, rule_box):
        self.disp_surf.fill(self.background)
        for boundary in boundaries:
            pygame.draw.line(self.disp_surf, (0,0,0),boundary[0], boundary[1], 4)
        for block in blocks:
            block.renderShape(self.disp_surf)
        arm.renderShape(self.disp_surf)
        # rule_box.renderShape(self.disp_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
