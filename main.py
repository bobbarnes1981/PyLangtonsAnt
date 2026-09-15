import pygame

WIDTH = 800
HEIGHT = 600

CELL_WIDTH = 10
CELL_HEIGHT = 10

GRID_WIDTH = WIDTH//CELL_WIDTH
GRID_HEIGHT = HEIGHT//CELL_HEIGHT

FACE = [
    "N",
    "E",
    "S",
    "W"
]

class Cell:
    def __init__(self, state:int):
        self.__state = state
    def getState(self) -> int:
        return self.__state
    def setState(self, state:int) -> None:
        self.__state = state

class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Ant:
    def __init__(self, location: Location):
        self.__location = location
        self.__face = 0
    def getLocation(self) -> Location:
        return self.__location
    def __move(self, grid: list[list[Cell]]):
        # move
        if self.__face == 0:
            self.__location.y+=1
        elif self.__face == 1:
            self.__location.x+=1
        elif self.__face == 2:
            self.__location.y-=1
        elif self.__face == 3:
            self.__location.x-=1
        else:
            raise Exception("Invalid face %i", self.__state)
        # wrap
        if self.__location.x < 0:
            self.__location.x = len(grid[0])
        elif self.__location.x > len(grid[0]):
            self.__location.x = 0
        if self.__location.y < 0:
            self.__location.y = len(grid)
        elif self.__location.y > len(grid):
            self.__location.y = 0
    def moveLeft(self, grid:list[list[Cell]]):
        # turn
        self.__face -= 1
        # wrap
        if self.__face < 0:
            self.__face = 3
        # move
        self.__move(grid)
    def moveRight(self, grid:list[list[Cell]]):
        # turn
        self.__face += 1
        # wrap
        if self.__face > 3:
            self.__face = 0
        # move
        self.__move(grid)

pygame.init()

pygame.display.set_caption("langton's ant ('p' to pause)")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

steps = 0

# init grid
grid = []
for y in range(0, GRID_HEIGHT):
    row = []
    for x in range(0, GRID_WIDTH):
        row.append(Cell(0))
    grid.append(row)

# init ants
ants = []
ants.append(Ant(Location(GRID_WIDTH//2, GRID_HEIGHT//2)))

paused = False

def quit():
    pygame.quit()
    raise SystemExit

while True:
    # handle events
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            quit()
        # pause game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_ESCAPE:
                quit()

    screen.fill("black")

    # naive approach, redraw all cells
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            # get state/colour
            state = grid[y][x].getState()
            if state == 0:
                colour = (0xff, 0x00, 0x00)
            elif state == 1:
                colour = (0xff, 0xff, 0xff)
            else:
                raise Exception("Invalid state %i", state)
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

        if paused == False:
            steps += 1
            # game logic
            cell_state = grid[location.y][location.x].getState()
            if cell_state == 0:
                grid[location.y][location.x].setState(1)
                ant.moveLeft(grid)
            elif cell_state == 1:
                grid[location.y][location.x].setState(0)
                ant.moveRight(grid)
            else:
                raise Exception("Invalid state %i", state)

    # draw text
    text = font.render(f"Steps: {steps}", True, (0x00, 0x00, 0x00))
    screen.blit(text, (0, 0))

    pygame.display.flip()
    clock.tick(60)