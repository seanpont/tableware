__author__ = 'sean'

from collections import defaultdict
import math
import random
import itertools


def _friendship(name1, name2):
    return tuple(sorted([name1, name2]))


def pad_names(names, n):
    """
    If len(names) is not divisible by n, returns a list padded with
    empty strings that is evenly divisible by n. Else, returns names.
    """
    padding = len(names) % n
    if padding > 0:
        return names + [''] * (n-padding)
    return names


def partition(names, n):
    """ Partitions names into n sub-lists """
    assert len(names) % n == 0, 'pad names before partitioning'
    return [names[i:i+n] for i in range(0, len(names), n)]


def partition_randomly(names, n):
    """Partitions the names into groups of at most n names randomly"""
    random.shuffle(names)
    return partition(names, n)


def pick_random_indices(tables):
    max_table = len(tables) - 1
    max_seat = len(tables[0]) - 1
    t1, t2 = random.randint(0, max_table), random.randint(0, max_table)
    while t1 == t2:
        t1, t2 = random.randint(0, max_table), random.randint(0, max_table)
    s1, s2 = random.randint(0, max_seat), random.randint(0, max_seat)
    return t1, s1, t2, s2


def swap_seats(tables, indices):
    tables[indices[0]][indices[1]], tables[indices[2]][indices[3]], = \
        tables[indices[2]][indices[3]], tables[indices[0]][indices[1]]


def acceptance_probability(score, last_score, temp):
    """As temperature decreases, the probability that a worse state will
    be accepted decreases."""
    if score > last_score:
        return 1
    return math.exp(float(score - last_score) / temp)


class SeatPicker(object):

    def __init__(self):
        # key = name, value = number of friendships
        self.friend_counter = defaultdict(int)
        # values are name tuples, sorted alphabetically.
        self.friendships = set()

    def run(self):
        pass

    def add_friendship(self, name1, name2):
        """Adds a reciprocal relationship between name1 and name2
        if name1 is not empty and name 2 is empty and name1 has not
        yet been named, name1 will be recorded but associated with 0 friends"""
        name1, name2 = name1.lower(), name2.lower()
        if (not name1 and not name2) or name1 == name2:
            return
        if not name1 or not name2:
            if name1 and name1 not in self.friend_counter:
                self.friend_counter[name1] = 0
            return
        friendship = _friendship(name1, name2)
        if friendship not in self.friendships:
            self.friend_counter[name1] += 1
            self.friend_counter[name2] += 1
            self.friendships.add(friendship)

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

    def simulate_annealing(self, chairs_per_table, iterations=3, temp=1000, cooling_rate=.0005):
        """
        Returns n lists of names (in alphabetical order) such that total value
        is maximized and no list has more than m names.
        """
        assert 0 < cooling_rate < 1
        names = pad_names(self.friend_counter.keys(), chairs_per_table)
        if len(names) <= chairs_per_table:
            return names
        best_tables, best_score = None, 0
        for i in range(iterations):
            tables = partition_randomly(names, chairs_per_table)
            self._anneal(tables, float(temp), cooling_rate)
            score = self.total_value(tables)
            if score > best_score:
                best_tables, best_score = tables, score
                print 'new high score:', score
        return best_tables

    def _anneal(self, tables, temp, cooling_rate):
        """Simulated annealing"""
        last_score = self.total_value(tables)
        while temp > 1:
            indices = pick_random_indices(tables)
            swap_seats(tables, indices)
            score = self.total_value(tables)
            p = acceptance_probability(score, last_score, temp)
            if p < 1 and p < random.random():
                swap_seats(tables, indices)  # switch them back
            temp *= (1 - cooling_rate)
        return tables

    def brute_force(self, chairs_per_table):
        names = pad_names(self.friend_counter.keys(), chairs_per_table)
        best_tables, best_score = None, 0
        for perm_names in itertools.permutations(names):
            tables = partition(perm_names, chairs_per_table)
            score = self.total_value(tables)
            if score > best_score:
                print 'new high score:', score, tables
                best_tables, best_score = tables, score
        return best_tables, best_score

    def hill_climb(self, chairs_per_table):
        """
        Swaps seats until no move will increase the score.
        Always take the best move available
        """
        names = pad_names(self.friend_counter.keys(), chairs_per_table)
        tables = partition_randomly(names, chairs_per_table)
        num_tables = len(tables)
        pinnacle_score = 0
        while True:
            best_indices, best_score = [], 0
            for t1, t2 in itertools.combinations(range(num_tables), 2):
                for s1, s2 in itertools.combinations(range(chairs_per_table), 2):
                    indices = [t1, s1, t2, s2]
                    swap_seats(tables, indices)
                    score = self.total_value(tables)
                    if score > best_score:
                        best_score = score
                        best_indices = indices
                    swap_seats(tables, indices)
            if best_score > pinnacle_score:
                pinnacle_score = best_score
                swap_seats(tables, best_indices)
            else:
                return tables, pinnacle_score

    def import_friend_list(self, filename):
        f = open(filename)
        for line in f:
            names = [s.strip() for s in line.split(',')]
            if len(names) == 1:
                names += ['']
            self.add_friendship(names[0], names[1])
        f.close()

    def areFriends(self, name1, name2):
        return _friendship(name1, name2) in self.friendships


if __name__ == '__main__':
    SeatPicker().run()
