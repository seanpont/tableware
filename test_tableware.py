__author__ = 'sean'

import random
import unittest
from tableware import *


class TestTableWare(unittest.TestCase):

    def setUp(self):
        self.sp = SeatPicker()

    def test_add_friendship(self):
        # Ability to define friendships
        self.sp.add_friendship('bob', 'kim')
        self.sp.add_friendship('bob', 'timmy')
        self.sp.add_friendship('Bob', 'James')  # case-insensitive
        self.sp.add_friendship('Timmy', 'James')
        self.sp.add_friendship('Timmy', 'Bob')  # duplicates are ignored
        self.sp.add_friendship('Bob', '')  # empty strings are ignored
        self.sp.add_friendship('James', 'james')  # narcissism is ignored

        print self.sp.friend_counter
        print self.sp.friendships

        # Bob has 4 friends and Kim has 1, so bob-kim = 1 1/3
        self.assertEqual(self.sp.value('Kim', 'Bob'), 4.0/3.0)
        # Timmy and Kim are not friends
        self.assertEqual(self.sp.value('Timmy', 'Kim'), 0)
        # James has 2 and Timmy has 2, so James-Timmy = 1
        self.assertEqual(self.sp.value('James', 'Timmy'), 1)

    def test_partition_randomly(self):
        names = list('abcdefghij')
        tables = partition_randomly(names, 3)
        print tables
        self.assertEqual(len(tables), 4)
        self.assertEqual(len(tables[0]), 3)
        self.assertEqual(len(tables[1]), 3)
        self.assertEqual(len(tables[2]), 3)
        self.assertEqual(len(tables[3]), 3)
        self.assertEqual(tables[3][1], '')
        self.assertEqual(tables[3][2], '')

    def test_score(self):
        self.sp.add_friendship('a', 'b')
        self.sp.add_friendship('b', 'c')
        self.sp.add_friendship('c', 'd')
        self.sp.add_friendship('d', 'a')
        self.sp.add_friendship('d', 'e')
        tables = [['a', 'b'], ['c', 'd', 'e']]
        total_value = self.sp.value('a', 'b') + self.sp.value('c', 'd') \
            + self.sp.value('d', 'e')
        self.assertEqual(self.sp.total_value(tables), total_value)

    def test_pick_random_indices(self):
        tables = [[1, 2, 3, 4], [5, 6, 7, 8]]
        for i in range(10):
            a, b, c, d = pick_random_indices(tables)
            self.assertIsNot((a, b), (c, d))
            self.assertLess(a, len(tables))
            self.assertLess(c, len(tables))
            self.assertLess(b, len(tables[0]))
            self.assertLess(d, len(tables[0]))

    def test_swap_seats(self):
        tables = [[1, 2, 3], [4, 5, 6]]
        swap_seats(tables, [0, 0, 1, 0])
        self.assertEqual(tables, [[4, 2, 3], [1, 5, 6]])
        swap_seats(tables, [0, 0, 1, 0])
        self.assertEqual(tables, [[1, 2, 3], [4, 5, 6]])
        swap_seats(tables, [0, 0, 0, 0])
        self.assertEqual(tables, [[1, 2, 3], [4, 5, 6]])
        swap_seats(tables, [0, 0, 0, 1])
        self.assertEqual(tables, [[2, 1, 3], [4, 5, 6]])


    def test_optimize(self):
        self.sp.add_friendship('a', 'b')
        self.sp.add_friendship('a', 'c')
        self.sp.add_friendship('a', 'd')
        self.sp.add_friendship('b', 'c')
        self.sp.add_friendship('b', 'd')
        self.sp.add_friendship('c', 'd')
        self.sp.add_friendship('e', 'f')
        self.sp.add_friendship('f', 'g')
        self.sp.add_friendship('h', 'i')

        tables = self.sp.arrange_seats(2)
        print tables


if __name__ == '__main__':
    unittest.main()
