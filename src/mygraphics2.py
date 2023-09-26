import pygame
import sys
import random
from enum import Enum
import uuid

WHITE = (229, 229, 229)
BLACK = (0, 0, 0)
##
# COLLISON_RESOLVER_ENABLED = False
GRID_ENABLED = True
# INTEGRITY_CHECKER_ENABLED = False
# Screen params
MAIN_WINDOW_BG_COLOR = WHITE
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
GRID_COLOR = BLACK
GRID_SIZE = 12
##
JUMP_FACTOR_MAX = 10

class Circle(object):
    circles_counter = 0
    def __init__(self, x, y, radius, color):
        self.__uuid = uuid.uuid4()
        
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__color = color
        
    def __del__(self):
        pass
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, (self.__x, self.__y), self.__radius)
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        
    @property
    def uuid(self):
        return self.__uuid

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, newVal):
        self.__x = newVal
        
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, newVal):
        self.__y = newVal
        
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, newVal):
        self.__color = newVal
        
    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, newVal):
        self.__radius = newVal 
    
    @classmethod
    def set_circles_count(cls, newVal):
        Circle.circles_counter = newVal
        
    @classmethod   
    def get_circles_count(cls, newVal):
        return Circle.circles_counter
        
class MyGraphics(object):
    class MovingDirection(Enum):
        RIGHT = 1
        LEFT = 2
        UP = 3
        DOWN = 4
        DIAGRU = 5
        DIAGLU = 6
        DIAGRD = 7
        DIAGLD = 8
    
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
    
    def __init__(self, window_title):
        self.__graphics_init(window_title)
        #
        self.__circles = {}
        
        # Grid System
        self.__gridCenters = set(self.__calculateGridCentersInit())
        self.__gridSize = len(self.__gridCenters)
        self.__lockedGrids = set()
        self.__unlockedGrids = set(self.__gridCenters)

        # Sim Tick
        self.clock = pygame.time.Clock()  # Create a clock object for controlling FPS

        # Initialize Pygame
        pygame.init()
        
    ##
    def __graphics_init(self, window_title):
        # Create a Pygame window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(MAIN_WINDOW_BG_COLOR)
        pygame.display.flip()  # Swap buffers
        pygame.display.update()
        pygame.display.set_caption(window_title)
    
    def __calculateGridCentersInit(self):
        centers = []
        for x in range(GRID_SIZE // 2, SCREEN_WIDTH, GRID_SIZE):
            for y in range(GRID_SIZE // 2, SCREEN_HEIGHT, GRID_SIZE):
                centers.append((x, y))
        return centers
    
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
             
    def __addCircle(self, spawn_x, spawn_y, radius, color):
        if len(self.__unlockedGrids) > 0:
            # Create a Circle object with a UUID
            circle = Circle(spawn_x, spawn_y, radius, color)

            self.__circles[circle.uuid] = circle

            return circle.uuid
        else:
            print("No unlocked grids available to spawn a circle.")
              
    def __moveCircle(self, circle_uuid=None, moving_dir: MovingDirection=None, jumpFactor=1):
        if circle_uuid in list(self.__circles.keys()):
            circle_obj = self.__circles[circle_uuid]
            
        if circle_obj is not None:
            if moving_dir in MyGraphics.directions:
                dx, dy = MyGraphics.directions[moving_dir]

                if jumpFactor < 1:
                    jumpFactor = 1
                if jumpFactor > JUMP_FACTOR_MAX:
                    jumpFactor = JUMP_FACTOR_MAX

                # Calculate the new position with the jump factor
                new_x = circle_obj.x + (dx * jumpFactor)
                new_y = circle_obj.y + (dy * jumpFactor)

                # Ensure the circle stays within the screen boundaries
                new_x = max(GRID_SIZE // 2, min(new_x, SCREEN_WIDTH - GRID_SIZE // 2))
                new_y = max(GRID_SIZE // 2, min(new_y, SCREEN_HEIGHT - GRID_SIZE // 2))

                # Check if the new position is in an unlocked grid
                new_grid_pos = (
                    round(new_x / GRID_SIZE) * GRID_SIZE,
                    round(new_y / GRID_SIZE) * GRID_SIZE,
                )
                if new_grid_pos in self.__unlockedGrids:
                    self.__unlockGrid((round(circle_obj.x), round(circle_obj.y)))
                    self.__lockGrid(new_grid_pos)
                circle_obj.move(new_x, new_y)
                return True
            else:
                raise Exception(f"Invalid moving direction [{moving_dir}]") 
        else:  
            raise Exception(f"Cannot move circle with invalid object [{circle_obj}]") 
    
    #
    def clearScreen(self):
        # Clear the screen
        self.screen.fill(MAIN_WINDOW_BG_COLOR)

    def refreshScreen(self):
        pygame.display.flip()
        pygame.display.update()
        
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
    
    def drawGrid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
    
    def move_left(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.LEFT, jumpFactor)

    def move_right(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.RIGHT, jumpFactor)

    def move_up(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.UP, jumpFactor)

    def move_down(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.DOWN, jumpFactor)

    def move_diagru(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.DIAGRU, jumpFactor)

    def move_diagrd(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.DIAGRD, jumpFactor)

    def move_diaglu(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.DIAGLU, jumpFactor)

    def move_diagld(self, circle_uuid, jumpFactor=1):
        self.__moveCircle(circle_uuid, MyGraphics.MovingDirection.DIAGLD, jumpFactor)
    
    def getRandomColorRGB(self) -> tuple:
        return (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    
    def spawnCircle(self):
        if len(self.__unlockedGrids) > 0:
            # Generate a random index
            random_value = random.choice(list(self.__unlockedGrids))

            spawn_x, spawn_y = random_value

            return self.__addCircle(
                spawn_x, spawn_y, ((GRID_SIZE // 2) - 1), self.getRandomColorRGB()
            )
        else:
            print("No unlocked grids available to spawn a circle.")
            
    def refreshCircles(self):
        for circle in list(self.__circles.values()):
            circle.draw(self.screen)
    
    def killCircle(self, circle_uuid):
        if circle_uuid in list(self.__circles.keys()):
            self.__unlockGrid((self.__circles[circle_uuid].x, self.__circles[circle_uuid].y))
            del self.__circles[circle_uuid]
        else:
            raise Exception(f"Cannon kill circle [{circle_uuid}]")
        
    def get_circle_pos(self, circle_uuid):
        return (self.__circles[circle_uuid].x, self.__circles[circle_uuid].y)
    
    ##