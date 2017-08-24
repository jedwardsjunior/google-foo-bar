"""
Prepare the Bunnies' Escape.py

Author: Julia Edwards
Date: August 2017
Github: jedwardsjunior



Prompt from Google foo.bar:

Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing
Commander Lambda's bunny prisoners, but once they're free of the prison blocks,
the bunnies are going to need to escape Lambda's space station via the escape
pods as quickly as possible. Unfortunately, the halls of the space station are
a maze of corridors and dead ends that will be a deathtrap for the escaping
bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling
project that will give you the opportunity to make things a little easier for
the bunnies. Unfortunately (again), you can't just remove all obstacles between
the bunnies and the escape pods - at most you can remove one wall per escape
pod path, both to maintain structural integrity of the station and to avoid
arousing Commander Lambda's suspicions. 

You have maps of parts of the space station, each starting at a prison exit and
ending at the door to an escape pod. The map is represented as a matrix of 0s
and 1s, where 0s are passable space and 1s are impassable walls. The door out
of the prison is at the top left (0,0) and the door into an escape pod is at
the bottom right (w-1,h-1).

Write a function answer(map) that generates the length of the shortest path
from the prison door to the escape pod, where you are allowed to remove one
wall as part of your remodeling plans. The path length is the total number of
nodes you pass through, counting both the entrance and exit nodes. The starting
and ending positions are always passable (0). The map will always be solvable,
though you may or may not need to remove a wall. The height and width of the
map can be from 2 to 20. Moves can only be made in cardinal directions; no
diagonal moves are allowed.

Test cases
==========

Inputs:
    (int) maze = [
    [0, 1, 1, 0]
    [0, 0, 0, 1]
    [1, 1, 0, 0]
    [1, 1, 1, 0]
]

Output:
    (int) 7

Inputs:
    (int) maze = [
    [0, 0, 0, 0, 0, 0]
    [1, 1, 1, 1, 1, 0]
    [0, 0, 0, 0, 1, 0]
    [0, 1, 1, 1, 0, 1]
    [0, 1, 1, 1, 0, 1]
    [0, 0, 1, 1, 0, 0]
]

Output:
    (int) 13
"""

"""
The Node class represents a space in the maze (via its x and y coordinates)
as well whether or not the space has been accessed via a path with a
demolished wall in it. This means that every space can potentially be
represented by two Nodes - one where canDestroyWall is True (meaning this
Node is not in a path with a demolished wall) and the other where
canDestroyWall is False.
"""
class Node:
    """
    Constructor for the class.
    """
    def __init__(self, x, y, canDestroyWall, maze):
        self.x = x
        self.y = y
        self.canDestroyWall = canDestroyWall
        self.maze = maze

    """
    Since we're defining a custom __eq__ function, we also need to define
    a custom __hash__ function (since the default one using the address of
    the object in memory goes away). We can just return the x coordinate
    XORed with the y coordinate, since two equal Nodes will always have the
    same x and y coordinates.
    """
    def __hash__(self):
        return self.x ^ self.y

    """
    Overwrite the default __eq__ function such that two Nodes evaluate as
    equal if they share the same x and y coordinates and the same value of
    canDestroyWall.
    """
    def __eq__(self, otherNode):
        return self.x == otherNode.x and\
               self.y == otherNode.y and\
               self.canDestroyWall == otherNode.canDestroyWall

    """
    Getter for the x coordinate.
    """
    def getX(self):
        return self.x

    """
    Getter for the y coordinate.
    """
    def getY(self):
        return self.y

    """
    The getNeighbors method returns all accessible neighbors from this
    space. If the neighbor is a wall, it is only returned in the list of
    neighbors if canDestroyWall is True for this space (that is, the path
    to this space does not yet include a demolished wall).
    """
    def getNeighbors(self):
        width = len(self.maze[0])
        height = len(self.maze)
        neighbors = []

        if (self.x > 0):
            neighborIsWall = self.maze[self.y][self.x - 1] == 1
            if (neighborIsWall):
                if (self.canDestroyWall):
                    neighbors.append(Node(self.x - 1, self.y, False, self.maze))
            else:
                neighbors.append(Node(self.x - 1, self.y, self.canDestroyWall, self.maze))
                
        if (self.y > 0):
            neighborIsWall = self.maze[self.y - 1][self.x] == 1
            if (neighborIsWall):
                if (self.canDestroyWall):
                    neighbors.append(Node(self.x, self.y - 1, False, self.maze))
            else:
                neighbors.append(Node(self.x, self.y - 1, self.canDestroyWall, self.maze))
                
        if (self.x < width - 1):
            neighborIsWall = self.maze[self.y][self.x + 1] == 1
            if (neighborIsWall):
                if (self.canDestroyWall):
                    neighbors.append(Node(self.x + 1, self.y, False, self.maze))
            else:
                neighbors.append(Node(self.x + 1, self.y, self.canDestroyWall, self.maze))
                
        if (self.y < height - 1):
            neighborIsWall = self.maze[self.y + 1][self.x] == 1
            if (neighborIsWall):
                if (self.canDestroyWall):
                    neighbors.append(Node(self.x, self.y + 1, False, self.maze))
            else:
                neighbors.append(Node(self.x, self.y + 1, self.canDestroyWall, self.maze))

        return neighbors       

"""
answer(maze) - This function generates the length of the shortest path
from the prison door to the escape pod, where at most one wall is allowed
to be removed along the way.

Inputs:
    (int) maze - a 2D array representing the map from the prison cell to the
                 escape pod

Output:
    (int) - the length of the shortest path from the prison cell to the escape pod.
"""
def answer(maze):
    # The prison cell is always at address (0, 0) and is always passable
    prisonCell = Node(0, 0, True, maze)
    escapePodX = len(maze[0]) - 1
    escapePodY = len(maze) - 1
    # Maintain the distance traveled to this Node in a dictionary
    distances = {prisonCell: 1}

    # Since we're only counting the number of nodes traversed from the prison
    # cell to the escape pod (as in, there aren't edges in this graph with
    # different weights), we can find the shortest path via a breadth-first
    # search starting from the prison cell.
    queue = []
    queue.append(prisonCell) 
    while queue:
        currentNode = queue.pop(0)
        for neighbor in currentNode.getNeighbors():
            distanceToNeighbor = distances[currentNode] + 1
            # Success! We've found the shortest path to the escape pod!
            if neighbor.getX() == escapePodX and neighbor.getY() == escapePodY:
                return distanceToNeighbor

            # If we haven't seen this Node before, we know this is the shortest
            # distance to it (since we're doing BFS) so add it to distances
            if (neighbor) not in distances:
                distances[neighbor] = distanceToNeighbor
                queue.append(neighbor)

    # We shouldn't ever get here, but if the maze were unsolvable we
    # would want to return infinity (which you need a float to represent)
    return float('inf')


def main():
    maze1 = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
    # Should print 7
    print(answer(maze1))

    maze2 = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0]]
    # Should print 13
    print(answer(maze2))
    
main()
