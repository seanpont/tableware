tableware
=========

Seating arrangement optimizer

From school lunch tables to weddings, making seating charts is hard. 
This simple command-line program attempts to optimize your seating arrangement
by maximizing the cumulative number of relationships at all tables.

### Specifically:

Friendships are considered to be bidirectional edges between nodes. 
Because some people may have lots of friends and others few, it weights the edges
such that the sum of all edges from a given node is 1. The weight of an edge
from A to B is 1/E_a + 1/E_b where E_x is the number of edges connected to x.

For example: Alex has 3 friends: Brandon, Cedric, and Darin. Brandon is also
friends with Cedric. Since Alex has 3 friends and Cedric 2, the Alex-Brandon
friendship is valued at 1/3 + 1/2 = 5/6.

TODO: 
-----

* Test SA algorithm with larger groups, tune parameters
* Implement data import
* Implement other graph partitioning strategies
* Make a nicer UI
* Monetize

