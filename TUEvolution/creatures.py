import pygame
import enum
import numpy
import numpy.random
import numpy.linalg
import TUEvolution.utils as utils

# Random walk parameters
walk_distance = 40  # Average distance between destinations
walk_turn = 4  # Variability in orientation (0 is completely random, ∞ is completely fixed)


# Power function
def power(radius, speed):
    """
    Calculate the power consumption based on the radius and speed of the creature.

    Parameters:
    radius (int): The radius of the creature.
    speed (int): The speed of the creature.

    Returns:
    int: The power consumption.
    """
    return (radius**3) * speed**2


# Energy consumption of smallest creature per step
unit_speed = 1
unit_time = walk_distance // unit_speed
unit_energy = unit_time * power(radius=2, speed=1)


# Creature status enumeration
class Status(enum.Enum):
    EXPLORING = "exploring"
    RETURNING = "returning"
    HOME = "home"
    PERISHED = "perished"
    TARGETING = "targeting"


# Creature class
class Creature:
    def __init__(self, size_evo_data, speed_evo_data, sense_evo_data, stamina, color):
        """
        Initialize a Creature object.

        Parameters:
        radius (int): The radius of the creature.
        speed (int): The speed of the creature.
        sense (int): The sense range of the creature.
        stamina (int): The stamina of the creature.
        color (tuple): The RGB color of the creature.
        """

        self.radius = max(size_evo_data["init"] // 2, 2)
        self.size_evo_data = size_evo_data
        self.speed = max(speed_evo_data["init"], 1)
        self.speed_evo_data = speed_evo_data
        self.sense = max(sense_evo_data["init"] // 2, 2)
        self.sense_evo_data = sense_evo_data
        self.power = power(self.radius, self.speed)
        self.stamina = stamina
        self.energy = stamina * unit_energy
        self.color = color
        self.targeting = False

        # Initialization
        self.step = self.speed
        self.food = 0
        self.status = Status.EXPLORING

    def set_state(self, position, orientation):
        """
        Set the state of the creature.

        Parameters:
        position (numpy.ndarray): The position of the creature.
        orientation (float): The orientation of the creature.
        """
        self.position = position
        self.position0 = position.copy()
        self.orientation = orientation

        # Initialize destination
        if not hasattr(self, 'destination'):
            self.update_destination(reorient=False)

    def home_out_of_reach(self, world):
        """
        Check if the creature's home is out of reach.

        Parameters:
        world (World): The world object.

        Returns:
        bool: True if the home is out of reach, False otherwise.
        """
        range = self.speed * self.energy / self.power
        max_distance = world.radius + world.homes_width // 2
        if range > max_distance:
            return False
        return max_distance - numpy.linalg.norm(self.position - world.center) > range

    def call_home(self, world):
        """
        Set the creature's destination to its home.

        Parameters:
        world (World): The world object.
        """
        r = world.radius - world.homes_width // 2
        p = self.position - world.center
        self.destination = world.center + r / numpy.linalg.norm(p) * p
        self.orientation = numpy.arctan2(*numpy.flip(numpy.array(self.destination) - numpy.array(self.position)))
        self.status = Status.RETURNING

    def update_destination(self, reorient=True):
        """
        Update the creature's destination.

        Parameters:
        reorient (bool): Whether to reorient the creature.
        """
        # Dont random walk if targeting
        if self.targeting is False:
            if reorient:
                self.orientation += numpy.random.vonmises(0, walk_turn)

            distance = numpy.random.poisson(walk_distance)
            self.destination = self.position + distance * utils.orientation_vector(self.orientation)

    def is_exploring(self):
        """
        Check if the creature is exploring.

        Returns:
        bool: True if the creature is exploring, False otherwise.
        """
        return self.status == Status.EXPLORING

    def is_home(self):
        """
        Check if the creature is home.

        Returns:
        bool: True if the creature is home, False otherwise.
        """
        return self.status == Status.HOME

    def perish(self):
        """
        Set the creature's status to perished.
        """
        self.status = Status.PERISHED

    def has_perished(self):
        """
        Check if the creature has perished.

        Returns:
        bool: True if the creature has perished, False otherwise.
        """
        return self.status == Status.PERISHED

    def is_alive(self):
        """
        Check if the creature is alive.

        Returns:
        bool: True if the creature is alive, False otherwise.
        """
        return not self.has_perished()

    def is_hungry(self):
        """
        Check if the creature is hungry.

        Returns:
        bool: True if the creature is hungry, False otherwise.
        """
        return self.food < 2

    def reincarnate(self):
        """
        Reincarnate the creature.

        Returns:
        Creature: A new creature with the same attributes.
        """
        return Creature(self.size_evo_data, self.speed_evo_data, self.sense_evo_data, self.stamina, self.color)

    def reproduce(self):
        """
        Reproduce a new creature with slight variations.

        Returns:
        Creature: A new creature with slightly varied attributes.
        """

        new_size_evo_data = self.mutate(self.size_evo_data)
        new_speed_evo_data = self.mutate(self.speed_evo_data)
        new_sense_evo_data = self.mutate(self.sense_evo_data)

        return Creature(new_size_evo_data, new_speed_evo_data, new_sense_evo_data, self.stamina, self.color)

    def mutate(self, attribute_data):
        """Helper function to mutate a given attribute."""
        mutation = numpy.random.choice(attribute_data["variations"], p=attribute_data["probabilities"])
        return {
            "init": max(attribute_data["init"] + int(mutation), 0),
            "variations": attribute_data["variations"],
            "probabilities": attribute_data["probabilities"],
        }

    def move(self, step=None):
        """
        Move the creature toward its destination.

        Parameters:
        step (int, optional): The step size. Defaults to None.
        """

        # Calculate direction and distance to destination
        direction = self.destination - self.position
        distance = numpy.linalg.norm(direction)

        step = self.step if step is None else step

        if distance <= step:  # Reached destination
            self.energy -= self.power * (distance / self.speed)
            self.position = self.destination.copy()
            self.targeting = False

            if self.status == Status.EXPLORING:
                self.color = (255, 0, 0)
                self.update_destination()

                if distance < step:  # Remainder of step
                    self.move(step - distance)

            elif self.status == Status.RETURNING:
                self.status = Status.HOME
                self.color = (0, 255, 0)

        else:  # Not reached destination
            self.energy -= self.power * (step / self.speed)
            direction = direction.astype(float) / distance
            self.position += numpy.round(step * direction).astype(int)

    def sense_surroundings(self, predators, food):
        """
        Sense the surroundings for predators and food.

        Parameters:
        predators (list): The list of predators.
        food (list): The list of food.
        """
        self.energy -= self.sense/5

        # Always run from predators regardless of food or status
        for p in predators:
            distance = numpy.linalg.norm(p.position - self.position)

            # Preditor is self, so ignore
            if distance == 0:
                continue

            if distance <= self.sense and self.radius < 1.2 * p.radius and (not p.is_home()):
                # Run in opposite direction of predator
                run_direction = (self.position - p.position) / distance
                # Run distance is the remaining distance such that the predator is at the edge of the sense range
                run_distance = self.sense - distance

                self.destination = self.position + run_distance * run_direction
                self.targeting = True
                return True

        # If targeting food or predator, continue targeting
        if self.targeting is True and self.status == Status.EXPLORING:
            distance_target = numpy.linalg.norm(self.destination - self.position)

            # If target is out of range, stop targeting
            if distance_target > self.sense:
                self.targeting = False
                return False
            
            return True
        
        # Target food if hungry and in range
        for f in food:
            distance = numpy.linalg.norm(f.position - self.position)

            if distance <= self.sense and self.is_hungry():
                self.destination = f.position
                self.targeting = True
                return True

        return False


    def draw(self, screen):
        """
        Draw the creature on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        sense_surface = pygame.Surface((self.sense * 2, self.sense * 2), pygame.SRCALPHA)
        pygame.draw.circle(sense_surface, (173, 216, 230, 128), (self.sense, self.sense), self.sense)
        screen.blit(sense_surface, self.position - numpy.array([self.sense, self.sense]))

        pygame.draw.circle(screen, self.color, self.position, self.radius)
        charge = max(self.energy / (self.stamina * unit_energy), 0)
        fill_color = (charge * numpy.array(self.color) + (1 - charge) * numpy.array(utils.color('white'))).astype(int)
        pygame.draw.circle(screen, fill_color, self.position, self.radius - 1)
