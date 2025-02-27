import pygame, numpy, numpy.random
import TUEvolution.utils as utils

class World:
    """
    A class to represent the world in which creatures live.
    """

    def __init__(self, center, radius, homes_width, day):
        """
        Initialize a World object.

        Parameters:
        center (tuple): The center of the world.
        radius (int): The radius of the world.
        homes_width (int): The width of the homes area.
        day (int): The duration of a day in the world.
        """
        self.radius = radius
        self.center = numpy.array(center)
        self.homes_width = homes_width
        self.day = day
        self.time = 0

    def end_of_day(self):
        """
        Check if the current time is the end of the day.

        Returns:
        bool: True if it is the end of the day, False otherwise.
        """
        return self.time==self.day
    
    def next_day(self):
        """
        Reset the time to the start of the next day.
        """
        self.time = 0

    def increment_time(self):
        """
        Increment the current time by one unit.
        """
        self.time += 1

    def assign_homes(self, creatures):
        """
        Assign homes to the creatures.

        Parameters:
        creatures (list): A list of Creature objects.
        """
        for c in range(len(creatures)):
            θ = 2*numpy.pi*c/len(creatures)
            r = self.radius-self.homes_width//2
            position = numpy.round(self.center+r*numpy.array([numpy.cos(θ),numpy.sin(θ)])).astype(int)
            creatures[c].set_state(position, θ+numpy.pi)

    def get_food_locations(self, n_food):
        """
        Generate random food locations within the world.

        Parameters:
        n_food (int): The number of food locations to generate.

        Returns:
        list: A list of food locations as numpy arrays.
        """
        θs = 2*numpy.pi*numpy.random.rand(n_food)
        rs = (self.radius-self.homes_width)*numpy.sqrt(numpy.random.rand(n_food))
        return [numpy.round(self.center+r*numpy.array([numpy.cos(θ),numpy.sin(θ)])).astype(int) for θ, r in zip(θs,rs)]

    def touches_edge(self, creature):
        """
        Check if a creature touches the edge of the world.

        Parameters:
        creature (Creature): The creature to check.

        Returns:
        bool: True if the creature touches the edge, False otherwise.
        """
        return sum((creature.position-self.center)**2)>(self.radius-creature.radius)**2

    def draw(self, screen):
        """
        Draw the world on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        pygame.draw.circle(screen, utils.color('dimgray'), self.center, self.radius)

        r_inner = self.radius-self.homes_width//3
        r_outer = self.radius-2*(self.homes_width//3)
        for fraction in numpy.arange(60)/60:
            if fraction > self.time/self.day:
                continue
            dial = utils.orientation_vector((-0.5+2*fraction)*numpy.pi)
            pygame.draw.line(screen, utils.color('lightgray'), self.center+r_inner*dial, self.center+r_outer*dial, 2)
        pygame.draw.circle(screen, utils.color('lightgray'), self.center, self.radius-self.homes_width)

class Food:
    """
    A class to represent food in the world.

    Attributes:
    position (numpy.ndarray): The position of the food.
    radius (int): The radius of the food.
    color (tuple): The RGB color of the food.
    available (bool): Whether the food is available.
    """

    def __init__(self, position, radius, color):
        """
        Initialize a Food object.

        Parameters:
        position (tuple): The position of the food.
        radius (int): The radius of the food.
        color (tuple): The RGB color of the food.
        """
        self.position = numpy.array(position)
        self.radius = max(radius,2)
        self.color = color
        self.available = True

    def is_available(self):
        """
        Check if the food is available.

        Returns:
        bool: True if the food is available, False otherwise.
        """
        return self.available

    def draw(self, screen):
        """
        Draw the food on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        pygame.draw.circle(screen, self.color, self.position, self.radius)