from mygraphics import MyGraphics, GRID_ENABLED
from time import sleep
import random

####################
WORLD_SPEED = 25
FRAMES_PER_GEN = 60
GENERATIONS = 5000
POPULATION = 100
####################

class Creature(object):
    def __init__(self, creatureIdx):
        self.__idx = creatureIdx
        self.__uuid = 0 #TODO
        self.__genome = "NaN" #TODO

    def movement_init(
        self,
        moveright,
        moveleft,
        moveup,
        movedown,
        movediagru,
        movediagrd,
        movediaglu,
        movediagld,
    ):
        self.moveright = moveright
        self.moveleft = moveleft
        self.moveup = moveup
        self.movedown = movedown
        self.movediagru = movediagru
        self.movediagrd = movediagrd
        self.movediagld = movediagld
        self.movediaglu = movediaglu

    def behaviour_init(self):
        pass

    # Behaviours
    def behaviour_randmove(self):
        movement_methods = [
            self.move_right,
            self.move_left,
            self.move_up,
            self.move_down,
            self.move_diagru,
            self.move_diagrd,
            self.move_diaglu,
            self.move_diagld,
            # Add other movement methods here
        ]
        random_movement = random.choice(movement_methods)
        random_movement()

    def behaviour_nav(self):
        pass
    
    # Movements
    def move_right(self):
        self.moveright(self.__idx)

    def move_up(self):
        self.moveup(self.__idx)

    def move_down(self):
        self.movedown(self.__idx)

    def move_left(self):
        self.moveleft(self.__idx)

    def move_diagru(self):
        self.movediagru(self.__idx)

    def move_diagrd(self):
        self.movediagrd(self.__idx)

    def move_diaglu(self):
        self.movediaglu(self.__idx)

    def move_diagld(self):
        self.movediagld(self.__idx)


class MyWorld(object):
    creatures_id = 0

    def __init__(self, world_title="World"):
        self.mygraphics = MyGraphics(world_title)
        # Params
        self.__creatures = []
        self.__currentPopulation = POPULATION
        #
        # sysinit
        self.spawn_creatures(POPULATION)
        #
        self.main_loop()

    ##
    def __creature_ginit(self, creature_obj):
        #
        creature_obj.movement_init(
            moveright=self.mygraphics.move_right,
            moveleft=self.mygraphics.move_left,
            moveup=self.mygraphics.move_up,
            movedown=self.mygraphics.move_down,
            movediagru=self.mygraphics.move_diagru,
            movediagrd=self.mygraphics.move_diagrd,
            movediaglu=self.mygraphics.move_diaglu,
            movediagld=self.mygraphics.move_diagld,
        )
        #
        creature_obj.behaviour_init()

    ##
    def creatureByIdx(self, index):
        if 0 <= index < len(self.__creatures):
            return self.__creatures[index]
        else:
            raise IndexError("Creature index out of range")

    def spawn_creatures(self, n):
        for i in range(0, n):
            creature = Creature(i)
            self.__creature_ginit(creature)
            self.mygraphics.spawnCircle()
            self.__creatures.append(creature)

            MyWorld.creatures_id += 1

    def refresh_creatures(self):
        self.mygraphics.refreshCircles()

    ##
    def main_loop(self):
        try:
            generation = 1
            frame = 1
            while generation <= GENERATIONS:
                while (frame <= FRAMES_PER_GEN) and self.mygraphics.runSimulation:
                    #
                    sleep((10.0 // WORLD_SPEED))
                    
                    self.mygraphics.isSimulationDestroyed()

                    self.mygraphics.clearScreen()

                    # Draw the grid
                    if GRID_ENABLED:
                        self.mygraphics.drawGrid()

                    self.refresh_creatures()
                    #
                    ####################################################################################################################################
                    for id in range(POPULATION):
                        self.creatureByIdx(id).behaviour_randmove()
                        
                    ####################################################################################################################################
                    #
                    # Swap buffers
                    self.mygraphics.refreshScreen()
                    #
                    self.mygraphics.setTimerTick(WORLD_SPEED)
                    #
                    frame += 1
                    print(f"Frame: {frame}")
                generation += 1
                frame = 0
                print(
                    f"Generation: {generation} -- Population: {self.__currentPopulation}"
                )
                #
                if not self.mygraphics.runSimulation:
                    self.mygraphics.destorySimulation()
        except Exception as e:
            # Display an error message on the screen
            print(f"An error occurred: {e}")
            if not self.mygraphics.runSimulation:
                self.mygraphics.destorySimulation()


myworld = MyWorld(world_title="My World - A1.0.0")
