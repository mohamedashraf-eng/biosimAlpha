from mygraphics import MyGraphics, GRID_ENABLED
from time import sleep
import random

####################
WORLD_SPEED = 12
FRAMES_PER_GEN = 500
GENERATIONS = 5000
POPULATION = 100
####################


class Creature(object):
    def __init__(self, creatureIdx):
        self.__idx = creatureIdx
        self.__uuid = 0  # TODO
        self.__genome = "NaN"  # TODO

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

    # drunk genome \ [linked graphics: done][created graphics: yes]
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
        random_movement(jumpFactor=0)

    # navigate genome \ [linked graphics: x][created graphics: no]
    def behaviour_navigate(self):
        pass

    # kill genome \ [linked graphics: x][created graphics: no]
    def behaviour_kill(self):
        pass

    # kill jump \ [linked graphics: x][created graphics: no]
    def behaviour_jump(self):
        pass

    # Movements genomes \ [linked graphics: done][created graphics: yes]
    def move_right(self, jumpFactor=0):
        self.moveright(self.__idx, jumpFactor)

    def move_up(self, jumpFactor=0):
        self.moveup(self.__idx, jumpFactor)

    def move_down(self, jumpFactor=0):
        self.movedown(self.__idx, jumpFactor)

    def move_left(self, jumpFactor=0):
        self.moveleft(self.__idx, jumpFactor)

    def move_diagru(self, jumpFactor=0):
        self.movediagru(self.__idx, jumpFactor)

    def move_diagrd(self, jumpFactor=0):
        self.movediagrd(self.__idx, jumpFactor)

    def move_diaglu(self, jumpFactor=0):
        self.movediaglu(self.__idx, jumpFactor)

    def move_diagld(self, jumpFactor=0):
        self.movediagld(self.__idx, jumpFactor)


###
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
        """ Initialize the creature graphics usage """
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

    def spawn_creature(self):
        creature = Creature(MyWorld.creatures_id)
        self.__creature_ginit(creature)
        self.mygraphics.spawnCircle()
        self.__creatures.append(creature)

        MyWorld.creatures_id += 1

    def spawn_creatures(self, n):
        for _ in range(0, n):
            self.spawn_creature()

    def kill_creature(self, creatureIdx):
        self.mygraphics.killCircle(creatureIdx)

    def kill_creatures(self, n):
        for id in range(n):
            self.kill_creature(id)

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
                    sleep((10.0 // WORLD_SPEED))  # FPS RELEASE \ CPU UTIL LOAD

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
                    print(f"[COUT>]: ([Frame]: {frame})")
                generation += 1
                frame = 0
                print(
                    f"[COUT>]: ([Generation]: {generation} -- [Population]: {self.__currentPopulation})"
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
