__author__ = 'sean'

from collections import defaultdict
import math
import random
import itertools


def _friendship(name1, name2):
    return tuple(sorted([name1, name2]))


def partition_randomly(names, n):
    """Partitions the names into groups of at most n names randomly"""
    random.shuffle(names)
    padding = len(names) % n
    if padding > 0:
        names = names + [''] * (n-padding)
    return [names[i:i+n] for i in range(0, len(names), n)]


def pick_random_indices(tables):
    max_table = len(tables) - 1
    max_seat = len(tables[0]) - 1
    return random.randint(0, max_table), random.randint(0, max_seat), random.randint(0, max_table), random.randint(0, max_seat)


def swap_seats(tables, indices):
    tables[indices[0]][indices[1]], tables[indices[2]][indices[3]], = \
        tables[indices[2]][indices[3]], tables[indices[0]][indices[1]]



class SeatPicker(object):

    def __init__(self):
        # key = name, value = number of friendships
        self.friend_counter = defaultdict(int)
        # values are name tuples, sorted alphabetically.
        self.friendships = set()

    def run(self):
        pass

    def add_friendship(self, name1, name2):
        name1, name2 = name1.lower(), name2.lower()
        if not name1 or not name2 or name1 == name2:
            return
        friendship = _friendship(name1, name2)
        if friendship not in self.friendships:
            self.friend_counter[name1] += 1
            self.friend_counter[name2] += 1
            self.friendships.add(friendship)

    def arrange_seats(self, chairs_per_table):
        """
        Returns n lists of names (in alphabetical order) such that total value
        is maximized and no list has more than m names.
        """
        names = list(self.friend_counter.keys())
        if len(names) < chairs_per_table:
            return names
        tables = partition_randomly(names, chairs_per_table)
        self.anneal(tables)
        return tables

    def value(self, name1, name2):
        name1, name2 = name1.lower(), name2.lower()
        if not name1 or not name2 or name1 == name2:
            return 0
        friendship = _friendship(name1, name2)
        if friendship in self.friendships:
            return 1.0/self.friend_counter[name1] + 1.0/self.friend_counter[name2]
        return 0

    def total_value(self, tables):
        """
        Calculates the cumulative value of all friendships at all tables.
        TODO: this could be optimized
        """
        total_value = 0
        for table in tables:
            for name1, name2 in itertools.combinations(table, 2):
                total_value += self.value(name1, name2)
        return total_value

    def anneal(self, tables):
        """Simulated annealing"""
        last_score = self.total_value(tables)
        for t in range(1000):
            indices = pick_random_indices(tables)
            swap_seats(tables, indices)
        return tables


if __name__ == '__main__':
    SeatPicker().run()
