from mygraphics import MyGraphics, GRID_ENABLED
from time import sleep
import random
import uuid
import string
from enum import Enum

#################### > Neuron

#################### > Genome
GENOME_LENGTH = 5
GENOME_LIST = [
    # Movements
    "MW",  # Move West
    "ME",  # Move East
    "MS",  # Move South
    "MN",  # Move North
    "MSW",  # Move South West
    "MSE",  # Move South East
    "MNW",  # Move North West
    "MNE",  # Move North East
    # Behaviours
    "CTR",  # Center
    "KL",  # Kill
    "MR",  # Move Randomly
    "MJ",  # Move jump
    "NAM",  # Navigate Around Map
    # Charspecs
    "CLR",  # Color
]
#################### > World
WORLD_SPEED = 15
FRAMES_PER_GEN = 100
GENERATIONS = 5000
POPULATION = 1000
####################


class Neuron(object):
    def __init__(self):
        # TODO
        pass


class Genome(object):
    def __init__(self, length=None):
        self.__genome_length = length
        # First startup create random genome
        self.__genome = self.__create_random_genome()

    def __str__(self):
        return self.self.__genome

    def __repr__(self):
        return f"Genome(length=None)"

    def __create_random_genome(self):
        # Create a dictionary to map genomes to 2-byte hex values
        self.__genome_to_hex_map = {
            genome: format(i, "02x") for i, genome in enumerate(GENOME_LIST)
        }

        # Check if num_picks is greater than the length of the original list
        if self.__genome_length > len(GENOME_LIST):
            print("Error: Number of picks exceeds the length of the original list.")
        else:
            # Create a smaller list with non-repeated random picks
            random_picks = random.sample(GENOME_LIST, self.__genome_length)

            # Create a list of chosen genomes in hex format
            genomes_in_hex = [
                self.__genome_to_hex_map[genome] for genome in random_picks
            ]

            return random_picks, genomes_in_hex

    def get_genome_hex(self):
        return str("".join(self.__genome[1]))

    def get_genome_str(self):
        return str(self.__genome[0])


class Creature(object):
    def __init__(self):
        # Generate a random UUID (version 4)
        self.__uuid = uuid.uuid4()
        self.__genome = Genome(GENOME_LENGTH)

    def base_init(self, get_pos):
        self.getpos = get_pos

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
    def genome_MR(self):
        movement_methods = [
            self.genome_ME,
            self.genome_MW,
            self.genome_MN,
            self.genome_MS,
            self.genome_MNE,
            self.genome_MSE,
            self.genome_MNW,
            self.genome_MSW,
        ]
        random_movement = random.choice(movement_methods)
        random_movement(jumpFactor=0)

    # Movements genomes \ [linked graphics: done][created graphics: yes]
    def genome_MW(self, jumpFactor=0):
        self.moveright(self.__uuid, jumpFactor)

    def genome_MN(self, jumpFactor=0):
        self.moveup(self.__uuid, jumpFactor)

    def genome_MS(self, jumpFactor=0):
        self.movedown(self.__uuid, jumpFactor)

    def genome_ME(self, jumpFactor=0):
        self.moveleft(self.__uuid, jumpFactor)

    def genome_MNW(self, jumpFactor=0):
        self.movediagru(self.__uuid, jumpFactor)

    def genome_MSW(self, jumpFactor=0):
        self.movediagrd(self.__uuid, jumpFactor)

    def genome_MNE(self, jumpFactor=0):
        self.movediaglu(self.__uuid, jumpFactor)

    def genome_MSE(self, jumpFactor=0):
        self.movediagld(self.__uuid, jumpFactor)

    #

    #
    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, new_uuid):
        self.__uuid = new_uuid

    def get_genome(self):
        return self.__genome.get_genome_hex()

    def get_pos(self):
        return self.getpos(self.__uuid)


###
class MyWorld(object):
    creatures_count = 0

    def __init__(self, world_title="World"):
        self.mygraphics = MyGraphics(world_title)
        # Params
        # Use a dictionary to store creatures with UUIDs as keys
        self.__creatures = {}
        self.__currentPopulation = 0
        self.__creature_id_counter = 0  # Incremented to generate unique UUIDs
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

        creature_obj.base_init(get_pos=self.mygraphics.get_circle_pos)

    ##
    def spawn_creature(self):
        creature = Creature()
        circle_uuid = (
            self.mygraphics.spawnCircle()
        )  # Get the UUID of the spawned circle
        creature.uuid = circle_uuid  # Pass the circle UUID to the creature
        self.__creature_ginit(creature)
        self.__creatures[creature.uuid] = creature
        self.__currentPopulation += 1

    def spawn_creatures(self, n):
        for _ in range(0, n):
            self.spawn_creature()

    def kill_creature(self, creature_uuid):
        if creature_uuid in self.__creatures:
            self.mygraphics.killCircle(
                creature_uuid
            )  # Use creature_uuid to kill the circle
            del self.__creatures[creature_uuid]
            self.__currentPopulation -= 1

    def kill_creatures(self, n):
        for _ in range(n):
            if self.__currentPopulation > 0:
                self.kill_creature(0)  # Kill the first creature in the list

    def refresh_creatures(self):
        self.mygraphics.refreshCircles()

    def apply_natural_selection(self):
        # Calculate the left half width of the map
        left_half_width = 1080 // 2

        # Create a list to store the IDs of creatures to be killed
        creature_ids_to_kill = []

        # Identify creatures to be killed and store their IDs
        for creature_uuid, creature in self.__creatures.items():
            x, _ = self.mygraphics.get_circle_pos(creature_uuid)
            if x < left_half_width:
                creature_ids_to_kill.append(creature_uuid)

        # Kill the selected creatures
        for creature_uuid in creature_ids_to_kill:
            self.kill_creature(creature_uuid)

    ##
    def main_loop(self):
        try:
            generation = 1
            frame = 1
            done = True
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

                    for creature_uuid in list(self.__creatures.keys()):
                        creature = self.__creatures[creature_uuid]
                        creature.genome_MR()

                    if done:
                        self.apply_natural_selection()
                        done = False
                    # self.apply_natural_selection()
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
