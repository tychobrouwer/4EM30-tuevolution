import unittest
from TUEvolution import creatures, utils

class TestCreature(unittest.TestCase):

    def setUp(self):
        self.creature = creatures.Creature(radius=10,
                                           speed=5,
                                           stamina=100,
                                           color=utils.color('red'))
        
    def test_initialization(self):
        self.assertEqual(self.creature.radius, 10, 'Radius not initialized correctly')
        self.assertEqual(self.creature.speed, 5, 'Speed not initialized correctly')
        self.assertEqual(self.creature.stamina, 100, 'Stamina not initialized correctly')
        self.assertEqual(self.creature.color, utils.color('red'), 'Color not initialized correctly')
        self.assertEqual(self.creature.power, 25000, 'Power not initialized correctly')
        self.assertEqual(self.creature.energy, 32000, 'Energy not initialized correctly') 
        self.assertEqual(self.creature.step, 5, 'Step not initialized correctly')
        self.assertEqual(self.creature.food, 0, 'Food not initialized correctly') 
        self.assertEqual(self.creature.status, creatures.Status.EXPLORING, 'Status not initialized correctly')

if __name__ == '__main__':
    unittest.main()