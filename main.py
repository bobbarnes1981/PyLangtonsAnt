"""Langton's Ant in Python"""
import pygame
import random

WIDTH = 800
HEIGHT = 600

CELL_SIZE = 2
CELL_WIDTH = CELL_SIZE
CELL_HEIGHT = CELL_SIZE

GRID_WIDTH = WIDTH//CELL_WIDTH
GRID_HEIGHT = HEIGHT//CELL_HEIGHT

NUM_ANTS = 10

CELL_COLOURS = [
    (0xff, 0x00, 0x00),
    (0xff, 0xff, 0xff)
]

FACE = [
    "N",
    "E",
    "S",
    "W"
]

class Cell:
    """A cell on the toroidal grid"""
    def __init__(self, state: int):
        self.__state = state
    def getState(self) -> int:
        """Get the cell state"""
        return self.__state
    def setState(self, state: int) -> None:
        """Set the cell state"""
        self.__state = state

class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Ant:
    DEFAULT_STEP_SIZE = 1
    def __init__(self, location: Location):
        self.__location = location
        self.__face = 0
    def getLocation(self) -> Location:
        return self.__location
    def __move(self, step: int, grid: list[list[Cell]]):
        # move
        if self.__face == 0:
            self.__location.y += step
        elif self.__face == 1:
            self.__location.x += step
        elif self.__face == 2:
            self.__location.y -= step
        elif self.__face == 3:
            self.__location.x -= step
        else:
            raise Exception(f"Invalid face {self.__face}")
        # wrap
        if self.__location.x < 0:
            self.__location.x += len(grid[0])
        elif self.__location.x > len(grid[0])-1:
            self.__location.x -= len(grid[0])
        if self.__location.y < 0:
            self.__location.y += len(grid)
        elif self.__location.y > len(grid)-1:
            self.__location.y -= len(grid)
    def moveLeft(self, grid:list[list[Cell]]):
        """Turn the ant left and step forward"""
        # turn
        self.__face -= 1
        # wrap
        if self.__face < 0:
            self.__face = 3
        # move
        self.__move(self.DEFAULT_STEP_SIZE, grid)
    def moveRight(self, grid:list[list[Cell]]):
        """Turn the ant right and step forward"""
        # turn
        self.__face += 1
        # wrap
        if self.__face > 3:
            self.__face = 0
        # move
        self.__move(self.DEFAULT_STEP_SIZE, grid)

# init pygame
pygame.init()
pygame.display.set_caption("langton's ant ('p' to pause)")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# init grid
grid = []
for y in range(0, GRID_HEIGHT):
    row = []
    for x in range(0, GRID_WIDTH):
        row.append(Cell(0))
    grid.append(row)

# init ants
ants = []
for a in range(0, NUM_ANTS):
    x = random.randint(0, GRID_WIDTH-1)
    y = random.randint(0, GRID_HEIGHT-1)
    ants.append(Ant(Location(x, y)))

# init game
paused = False
steps = 0
elapsed = 0

screen.fill((0x00, 0x00, 0xff))

# game loop
while True:
    elapsed = clock.tick()
    fps = clock.get_fps()
    num_steps = 1

    # handle events
    quit_game = False
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            quit_game = True
        # pause game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_ESCAPE:
                quit_game = True
    if quit_game is True:
        pygame.quit()
        raise SystemExit

    # draw cells
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            # get state/colour
            state = grid[y][x].getState()
            if state == 0:
                colour = CELL_COLOURS[state]
            elif state == 1:
                colour = CELL_COLOURS[state]
            else:
                raise Exception(f"Invalid state {state}")
            # draw
            left = x * CELL_WIDTH
            top = y * CELL_HEIGHT
            pygame.draw.rect(screen, colour, (left, top, CELL_WIDTH, CELL_HEIGHT))

    # draw all ants
    for ant in ants:
        # get location
        location = ant.getLocation()
        # get colour
        colour = (0x00, 0x00, 0x00)
        # draw
        left = location.x * CELL_WIDTH
        top = location.y * CELL_HEIGHT
        pygame.draw.rect(screen, colour, (left, top, CELL_WIDTH, CELL_HEIGHT))

    # move all ants
    if paused is False:
        for i in range(0, num_steps):
            steps += 1
            # game logic
            for ant in ants:
                # get location
                location = ant.getLocation()
                # get state, set state, move ant
                cell_state = grid[location.y][location.x].getState()
                if cell_state == 0:
                    grid[location.y][location.x].setState(1)
                    ant.moveLeft(grid)
                elif cell_state == 1:
                    grid[location.y][location.x].setState(0)
                    ant.moveRight(grid)
                else:
                    raise Exception(f"Invalid state {state}")

    # draw text
    text = f"Steps: {steps}\nFPS: {fps:.2f}\nElapsed: {elapsed}ms"
    text_img = font.render(text, True, (0x00, 0x00, 0x00))
    screen.blit(text_img, (0, 0))

    pygame.display.flip()
