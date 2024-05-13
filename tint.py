# TINT 1.0 - Made By Nick Kipshidze 10/02/2023 #
# TINT 2.0 - Made by Nick Kipshidze 05/12/2024 #

# Terminal  #
# INTerface #

import os

class Interface(object):
    def __init__(self, width: int, height: int, position: str = "center,center") -> None:
        self.surf_width = width
        self.surf_height = height
        self.fill(".")

        # top,left    top,center,   top,right
        # center,left center,center center,right
        # bottom,left bottom,center bottom,right
        self.position = position

        self.sprites = {} # "name": ["", ""]

        self.update_terminal_size()

    # Update

    def update_terminal_size(self) -> None:
        self.columns, self.rows = os.get_terminal_size()
    
    # Backend
 
    def move(self, x, y):
        print("\033[%d;%dH" % (y, x))

    def process_surface(self, surface: list) -> str:
        position = self.position.split(",")
        
        marginY = self.rows - self.surf_height - 2
        marginX = self.columns - self.surf_width - 1
        
        if position[1] == "left":
            for y in range(self.surf_height): 
                surface[self.surf_width * y] = "\n"+surface[self.surf_width * y]
        if position[1] == "center":
            for y in range(self.surf_height): 
                surface[self.surf_width * y] = "\n"+" "*(marginX//2)+surface[self.surf_width * y]
        if position[1] == "right":
            for y in range(self.surf_height): 
                surface[self.surf_width * y] = "\n"+" "*marginX+surface[self.surf_width * y]

        if position[0] == "top":
            surface = surface + ["\n" * marginY]
        if position[0] == "center":
            surface = ["\n" * (marginY//2)] + surface + ["\n" * (marginY//2)]
        if position[0] == "bottom":
            surface = ["\n" * marginY] + surface
        
        return "".join(map(str, surface))

    def make_sprite(self, name: str, sprite: list = None, file: str = None) -> None:
        if sprite:
            self.sprites[name] = sprite
        if file:
            self.sprites[name] = open(file).read().split("\n")

    # Draw

    def fill(self, character: str = ".") -> None:
        self.surface = [character for _ in range(self.surf_width * self.surf_height)]
    
    def draw_char(self, x: int, y: int, character: str = "#") -> None:
        if x < 0 or y < 0 or x > self.surf_width-1 or y > self.surf_height-1:
            return -1
        else:
            self.surface[self.surf_width * int(y) + int(x)] = character

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, character: str = "#") -> None:
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) > abs(dy):
            xmin, xmax = sorted([x1, x2])
            ratio = 0 if dx == 0 else dy / dx
            for x in range(xmin, xmax):
                y = y1 + (x - x1) * ratio
                self.draw_char(int(x), int(y), character)

        else:
            ymin, ymax = sorted([y1, y2])
            ratio = 0 if dy == 0 else dx / dy
            for y in range(ymin, ymax):
                x = x1 + (y - y1) * ratio
                self.draw_char(int(x), int(y), character)

    def draw_sprite(self, x: int, y: int, name: str):
        for row in range(len(self.sprites[name])):
            for col in range(len(self.sprites[name][row])):
                self.draw_char(col+x, row+y, self.sprites[name][row][col])

    def stdout(self) -> None:
        self.move(0, 0)
        print(self.process_surface(self.surface.copy()), end = "")
