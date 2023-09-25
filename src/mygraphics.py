import pygame
import sys
import random
from enum import Enum
from llist import sllist

WHITE = (229, 229, 229)
BLACK = (0, 0, 0)
##
COLLISON_RESOLVER_ENABLED = False
GRID_ENABLED = False
INTEGRITY_CHECKER_ENABLED = False

# Screen params
MAIN_WINDOW_BG_COLOR = WHITE
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
GRID_COLOR = BLACK
GRID_SIZE = 12
GRID_SIZE_TO_CIRCLE_RADIUS_FACTOR = 0.01
# __SIM_SPEED__ = 30  # FPS
##

# Circle class
class Circle:
    def __init__(self, x, y, radius, color):
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.__color, (self.__x, self.__y), self.__radius)

    def move(self, dx, dy):
        self.__x = dx
        self.__y = dy

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x_val=0):
        self.__x = new_x_val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y_val=0):
        self.__y = new_y_val

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, new_radius_val=0):
        self.__radius = new_radius_val

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color_val=0):
        self.__color = new_color_val

    def getPos(self):
        return (self.x, self.y)


# Graphics class
class MyGraphics(object):
    """ Main Graphics Lib """

    # Enum for moving directions
    class MovingDirection(Enum):
        RIGHT = 1
        LEFT = 2
        UP = 3
        DOWN = 4
        DIAGRU = 5
        DIAGLU = 6
        DIAGRD = 7
        DIAGLD = 8

    #
    circle_counter_q = 0
    directions = {
        MovingDirection.RIGHT: (GRID_SIZE, 0),
        MovingDirection.LEFT: (-GRID_SIZE, 0),
        MovingDirection.UP: (0, -GRID_SIZE),
        MovingDirection.DOWN: (0, GRID_SIZE),
        MovingDirection.DIAGRU: (GRID_SIZE, -GRID_SIZE),
        MovingDirection.DIAGLU: (-GRID_SIZE, -GRID_SIZE),
        MovingDirection.DIAGRD: (GRID_SIZE, GRID_SIZE),
        MovingDirection.DIAGLD: (-GRID_SIZE, GRID_SIZE),
    }

    runSimulation = True

    def __init__(self, screen_title="Obj1"):
        # Create a Pygame window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(MAIN_WINDOW_BG_COLOR)
        pygame.display.flip()  # Swap buffers
        pygame.display.set_caption(screen_title)

        self.__circles = []  # List to store circle objects

        # Grid System
        self.__gridCenters = set(self.__calculateGridCentersInit())
        self.__gridSize = len(self.__gridCenters)
        self.__lockedGrids = set()
        self.__unlockedGrids = set(self.__gridCenters)

        # Sim Tick
        self.clock = pygame.time.Clock()  # Create a clock object for controlling FPS

        # Initialize Pygame
        pygame.init()

        # Enter the main loop
        # self.main_loop()

    #
    def clearScreen(self):
        # Clear the screen
        self.screen.fill(MAIN_WINDOW_BG_COLOR)

    def refreshScreen(self):
        pygame.display.flip()

    #
    def isSimulationDestroyed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MyGraphics.runSimulation = False

    def destorySimulation(self):
        # Quit Pygame
        pygame.quit()
        sys.exit()

    def setTimerTick(self, fps):
        # Control the FPS
        self.clock.tick(fps)

    #
    def __checkCollision(self, circleIdx):
        if 0 <= circleIdx < len(self.__circles):
            circle_obj = self.__circles[circleIdx]

            for other_circle in self.__circles:
                if other_circle != circle_obj:
                    distance = (
                        (circle_obj.x - other_circle.x) ** 2
                        + (circle_obj.y - other_circle.y) ** 2
                    ) ** 0.5
                    if distance < (circle_obj.radius + other_circle.radius):
                        return True
        return False

    def __resolveCollisions(self):
        for i, circle_obj in enumerate(self.__circles):
            if self.__checkCollision(i):
                # If a collision is detected, move the circle in a random direction
                randomMove = random.choice(
                    [self.move_right, self.move_left, self.move_up, self.move_down]
                )
                randomMove(i)

    def __integrityChecker(self):
        #####>#[X]# Integrity Analysis
        # Find the intersection of the two sets
        intersection = self.__lockedGrids.intersection(self.__unlockedGrids)
        # Check if there is any intersection
        if intersection:
            print("Collison detected:")
            for shared_tuple in intersection:
                print(shared_tuple)
            # if COLLISON_RESOLVER_ENABLED:
            # self.__resolveCollisions()
        else:
            print("No collison detected")

    def __calculateGridCentersInit(self):
        centers = []
        for x in range(GRID_SIZE // 2, SCREEN_WIDTH, GRID_SIZE):
            for y in range(GRID_SIZE // 2, SCREEN_HEIGHT, GRID_SIZE):
                centers.append((x, y))
        return centers

    def __gridRelative2Physical(self, relative_x, relative_y):
        physical_x = relative_x
        physical_y = relative_y
        return physical_x, physical_y

    def __lockGrid(self, grid_pos: tuple = None):
        if grid_pos is not None:
            self.__lockedGrids.add(grid_pos)
            if grid_pos in self.__unlockedGrids:
                self.__unlockedGrids.remove(grid_pos)

    def __unlockGrid(self, grid_pos: tuple = None):
        if grid_pos is not None:
            self.__unlockedGrids.add(grid_pos)
            if grid_pos in self.__lockedGrids:
                self.__lockedGrids.remove(grid_pos)

    def drawGrid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def __addCircle(self, respawn_x, respawn_y, radius, color):
        if len(self.__circles) < self.__gridSize:
            self.__lockGrid((respawn_x, respawn_y))
            #
            circle = Circle(respawn_x, respawn_y, radius, color)
            self.__circles.append(circle)
            MyGraphics.circle_counter_q += 1

    def __drawCircle(self, circleIdx):
        if 0 <= circleIdx < len(self.__circles):
            self.__circles[circleIdx].draw(self.screen)

    def __moveCircle(self, circleIdx, moving_dir: MovingDirection):
        if 0 <= circleIdx < len(self.__circles):
            circle_obj = self.__circles[circleIdx]

            if moving_dir in MyGraphics.directions:
                dx, dy = MyGraphics.directions[moving_dir]

                # Calculate the new position
                new_x = circle_obj.x + dx
                new_y = circle_obj.y + dy

                # Ensure the circle stays within the screen boundaries
                new_x = max(GRID_SIZE // 2, min(new_x, SCREEN_WIDTH - GRID_SIZE // 2))
                new_y = max(GRID_SIZE // 2, min(new_y, SCREEN_HEIGHT - GRID_SIZE // 2))

                if (new_x, new_y) in self.__unlockedGrids:
                    self.__unlockGrid((circle_obj.x, circle_obj.y))
                    self.__lockGrid((new_x, new_y))
                    circle_obj.move(new_x, new_y)
            else:
                pass
        else:
            pass

    def __getRandomGridPos(self):
        return random.choice(self.__gridCenters)

    ####

    def move_left(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.LEFT)

    def move_right(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.RIGHT)

    def move_up(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.UP)

    def move_down(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.DOWN)

    def move_diagru(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.DIAGRU)

    def move_diagrd(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.DIAGRD)

    def move_diaglu(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.DIAGLU)

    def move_diagld(self, circle_index):
        self.__moveCircle(circle_index, MyGraphics.MovingDirection.DIAGLD)

    def getRandomColorRGB(self) -> tuple:
        return (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

    def spawnCircle(self):
        if len(self.__unlockedGrids) > 0:
            # Generate a random index
            random_value = random.choice(list(self.__unlockedGrids))

            spawn_x, spawn_y = random_value  # Extract the (x, y) tuple
            spawn_x, spawn_y = self.__gridRelative2Physical(spawn_x, spawn_y)

            self.__addCircle(
                spawn_x, spawn_y, ((GRID_SIZE // 2) - 1), self.getRandomColorRGB()
            )
        else:
            print("No unlocked grids available to spawn a circle.")

    def refreshCircles(self):
        for circle in self.__circles:
            circle.draw(self.screen)

    def killCircle(self, circleIdx):
        if 0 <= circleIdx < len(self.__circles):
            circle_obj = self.__circles[circleIdx]

            if (circle_obj.x, circle_obj.y) in self.__lockedGrids:
                self.__unlockGrid((circle_obj.x, circle_obj.y))
            del circle_obj
            MyGraphics.circle_counter_q -= 1