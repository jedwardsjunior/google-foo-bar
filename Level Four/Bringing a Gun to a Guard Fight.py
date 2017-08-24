"""
Bringing a Gun to a Guard Fight.py

Author: Julia Edwards
Date: August 2017
Github: jedwardsjunior

Inspired by xphoniex's Java solution that can be found here:
https://github.com/xphoniex/Google-Foobar/blob/master/bringing_a_gun_to_a_guard_fight_answer.java




Prompt from Google foo.bar:

Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards!
Fortunately, you grabbed a beam weapon from an abandoned guardpost while you
were running through the station, so you have a chance to fight your way out.
But the beam weapon is potentially dangerous to you as well as to the elite
guard: its beams reflect off walls, meaning youll have to be very careful
where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming
too weak to cause damage. You also know that if a beam hits a corner, it will
bounce back in exactly the same direction. And of course, if the beam hits
either you or the guard, it will stop immediately (albeit painfully). 

Write a function answer(dimensions, your_position, guard_position, distance)
that gives an array of 2 integers of the width and height of the room, an
array of 2 integers of your x and y coordinates in the room, an array of 2
integers of the guard's x and y coordinates in the room, and returns an
integer of the number of distinct directions that you can fire to hit the
elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1000, 1 < y_dim <= 1000]. You
and the elite guard are both positioned on the integer lattice at different
distinct positions (x, y) inside the room such that
[0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam
can travel before becoming harmless will be given as an integer
1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with
dimensions [3, 2], you_position [1, 1], guard_position [2, 1], and a maximum
shot distance of 4, you could shoot in seven different directions to hit the
elite guard (given as vector bearings from your location):
[1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2].
As specific examples, the shot at bearing [1, 0] is the straight line
horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the
left wall and then the bottom wall before hitting the elite guard with a total
shot distance of sqrt(9), and the shot at bearing [1, 2] bounces off just the
top wall before hitting the elite guard with a total shot distance of sqrt(5).

Test cases
==========

Inputs:
    (int list) dimensions = [3, 2]
    (int list) captain_position = [1, 1]
    (int list) badguy_position = [2, 1]
    (int) distance = 4
Output:
    (int) 7

Inputs:
    (int list) dimensions = [300, 275]
    (int list) captain_position = [150, 150]
    (int list) badguy_position = [185, 100]
    (int) distance = 500
Output:
    (int) 9

"""

# Global variables shared across the various helper functions
targets = []            # The potential targets to aim for
knownCaptainHits = {}   # A dictionary where the key is a known coordinate
                        # that would hit the captain and the value is the
                        # greatest common denominator of the x and y values
captainX = 0            # The x position of the captain in the grid
captainY = 0            # The y position of the captain in the grid
guardX = 0              # The x position of the guard in the grid
guardY = 0              # The y position of the guard in the grid
_distance = 0           # The maximum distance that the beam can travel

"""
gcd():
Helper function to compute the greatest common denominator of two variables.

Inputs:
(int) x
(int) y

Output:
(int) - the greatest (positive) common denominator between x and y
"""
def gcd(x, y):
    if (y == 0):
        return abs(x)

    return gcd(y, x % y)

"""
addTarget():
Helper function  to add this target to the list of targets.

Inputs:
(int) currentX - the X location of the target in the grid
(int) currentY - the Y location of the target in the grid

Outputs:
(void)
"""
def addTarget(currentX, currentY):
    global targets
    global captainX
    global captainY
    global _distance
    
    target = (currentX, currentY)
    deltaY = currentY - captainY
    deltaX = currentX - captainX
    deltaD = (deltaY ** 2 + deltaX ** 2) ** .5
    
    if (deltaD < _distance):
        targets.append(target)


"""
addKnownCaptainHit():
Helper function to add this target to the set of targets that we know will
hit the captain.

Inputs:
(int) currentX - the X location of the target in the grid
(int) currentY - the Y location of the target in the grid

Outputs:
(void)
"""
def addKnownCaptainHit(currentX, currentY):
    global captainX
    global captainY
    global _distance
    global knownCaptainHits
    
    deltaY = currentY - captainY
    deltaX = currentX - captainX
    deltaD = (deltaY ** 2 + deltaX ** 2) ** .5
    deltaGCD = gcd(deltaX, deltaY)
    deltaX //= deltaGCD
    deltaY //= deltaGCD
    target = (deltaY, deltaX)
    
    if (deltaD < _distance):
        # If we haven't seen this target before, add it as a key
        # in knownCaptainHits with the greatest common denominator
        # as its value. This will be used later to determine whether there's
        # another target that is closer to the captain that would
        # hit the guard first.
        if target not in knownCaptainHits:
            knownCaptainHits[target] = deltaGCD

        # If we've already seen this target before, make sure we're setting
        # its value to the lowest GCD that we've found
        elif (deltaGCD < knownCaptainHits[target]):
            knownCaptainHits[target] = deltaGCD

"""
fillRow():
Helper function to go through each row in the map and generate targets to aim
for or avoid (if isCaptain is True) that are within the laser's range.

Inputs:
(int) currentX         - the X location of the target in the grid
(int) currentY         - the Y location of the target in the grid
(int) verticalDistance - the number of ghost grids above/below the real grid
                         that we can hit with the laser distance
(int) lateralDistance  - the number of ghost grids to the right/left of the
                         real grid that we can hit with the laser distance
(int[]) dimensions     - the dimensions of the grid
(bool) isCaptain       - whether or not the target would hit the captain

Output:
(void)
"""
def fillRow(currentX, currentY, verticalDistance, lateralDistance, dimensions, isCaptain):
    global captainX, guardX
    right = currentX
    left = currentX

    # If this is the captain, use her coordinates. Otherwise, we'll use the guard's
    # coordinates
    if (isCaptain):
        rightMargin = dimensions[0] -  captainX
        leftMargin = captainX
    else:
        rightMargin = dimensions[0] -  guardX
        leftMargin = guardX

    # For each ghost grid that the laser can hit...
    for i in range(1, lateralDistance + 1):
        # In the ghost grid, the corresponding position that will hit the
        # captain (if isCaptain == True) or the guard (if isCaptain == False)
        # flips back and forth between being the equivalent of the margin from
        # the right/left and the current x coordinate
        right += rightMargin * 2
        left -= leftMargin * 2
        rightMargin = dimensions[0] - rightMargin
        leftMargin = dimensions[0] - leftMargin

        if (isCaptain):
            addKnownCaptainHit(right, currentY)
            addKnownCaptainHit(left, currentY)
        else:
            addTarget(right, currentY)
            addTarget(left, currentY)

        fillColumn(right, currentY, verticalDistance, dimensions, isCaptain)
        fillColumn(left, currentY, verticalDistance, dimensions, isCaptain)

"""
fillColumn():
Helper function to go through each column in the map and generate targets to aim
for or avoid (if isCaptain is True) that are within the laser's range.

Inputs:
(int) currentX         - the X location of the target in the grid
(int) currentY         - the Y location of the target in the grid
(int) verticalDistance - the number of ghost grids above/below the real grid
                         that we can hit with the laser distance
(int) lateralDistance  - the number of ghost grids to the right/left of the
                         real grid that we can hit with the laser distance
(int[]) dimensions     - the dimensions of the grid
(bool) isCaptain       - whether or not the target would hit the captain

Output:
(void)
"""
def fillColumn(currentX, currentY, verticalDistance, dimensions, isCaptain):
    global captainY, guardY
    top = currentY
    bottom = currentY

    # If this is the captain, use her coordinates. Otherwise, we'll use the guard's
    # coordinates
    if (isCaptain):
        topMargin = dimensions[1] - captainY
        downMargin = captainY
    else:
        topMargin = dimensions[1] - guardY
        downMargin = guardY

    # For each ghost grid that the laser can hit...
    for i in range(1, verticalDistance + 1):
        # In the ghost grid, the corresponding position that will hit the
        # captain (if isCaptain == True) or the guard (if isCaptain == False)
        # flips back and forth between being the equivalent of the margin from
        # the top/bottom and the current y coordinate
        top += topMargin * 2
        bottom -= downMargin * 2
        topMargin = dimensions[1] - topMargin
        downMargin = dimensions[1] - downMargin

        if (isCaptain):
            addKnownCaptainHit(currentX, top)
            addKnownCaptainHit(currentX, bottom)
        else:
            addTarget(currentX, top)
            addTarget(currentX, bottom)

"""
generateTargets():
Helper method to generate all the targets to aim for.

Inputs:
(int) guardX           - the X location of the guard in the grid
(int) guardY           - the Y location of the guard in the grid
(int) verticalDistance - the number of ghost grids above/below the real grid
                         that we can hit with the laser distance
(int) lateralDistance  - the number of ghost grids to the right/left of the
                         real grid that we can hit with the laser distance
(int[]) dimensions     - the dimensions of the grid
(bool) isCaptain       - whether or not the target would hit the captain

Outputs:
(void)
"""
def generateTargets(guardX, guardY, verticalDistance, lateralDistance, dimensions):
    fillColumn(guardX, guardY, verticalDistance, dimensions, False)
    fillRow(guardX, guardY, verticalDistance, lateralDistance, dimensions, False)

"""
generateKnownCaptainHits():
Helper method to generate all the targets to aim for.

Inputs:
(int) captainX         - the X location of the guard in the grid
(int) captainY         - the Y location of the guard in the grid
(int) verticalDistance - the number of ghost grids above/below the real grid
                         that we can hit with the laser distance
(int) lateralDistance  - the number of ghost grids to the right/left of the
                         real grid that we can hit with the laser distance
(int[]) dimensions     - the dimensions of the grid
(bool) isCaptain       - whether or not the target would hit the captain

Outputs:
(void)
"""
def generateKnownCaptainHits(captainX, captainY, verticalDistance, lateralDistance, dimensions):
    fillColumn(captainX, captainY, verticalDistance, dimensions, True)
    fillRow(captainX, captainY, verticalDistance, lateralDistance, dimensions, True)

"""
answer():
Calculates the number of distinct directions that you can fire to hit the
guard, given the dimensions of the room, your position in it, the guard's
position in it, and the distance the laser can travel.

Inputs:
(int[]) dimensions        - an array of 2 integers of the width and height
                           of the room
(int[]) captain_position  - an array of 2 integers of the captain's x and 
                           y coordinates in the room
(int[]) guard_position    - an array of 2 integers of the guard's x and y
                           coordinates in the room
(int) distance            - the maximum distance that the beam can travel

Outputs:
(int) - the number of distinct directions that you can fire to hit the
        elite guard, given the maximum distance that the beam can travel
"""
def answer(dimensions, captain_position, guard_position, distance):
    global targets, knownCaptainHits, captainX, captainY, guardX, guardY, _distance

    # Assign this test case's values to our global variables
    _distance = distance
    captainX = captain_position[0]
    captainY = captain_position[1]
    guardX = guard_position[0]
    guardY = guard_position[1]

    # This will keep track of the known guard hits for this test case
    guardHits = set()

    # Handle the direct hit
    directY = guardY - captainY
    directX = guardX - captainX
    deltaGCD = gcd(directX, directY)
    deltaD = (directY ** 2 + directX ** 2) ** .5
    directY //= deltaGCD
    directX //= deltaGCD

    # If the laser can't reach the guard via a direct hit, just
    # return 0
    if (_distance - deltaD < 0):
        return 0

    # Initialize count to 1 to account for the direct hit, and mark
    # it as seen
    count = 1
    guardHits.add((directY, directX))

    # We'll take the approach of looking for targets within "ghost" grids
    #  - grids that are parallel to ours - since unfolding the trajectory
    # of the laser gives you a coordinate in a ghost grid that would be
    # hit.
    #
    # lateralDistance and verticalDistance determine the number of ghost
    # grids that we can reach with the given laser distance, and are used
    # to help us iterate over target coordinates in these grids.
    lateralDistance = _distance // dimensions[0] + 1
    verticalDistance = _distance // dimensions[1] + 1
    
    generateTargets(guardX, guardY, verticalDistance, lateralDistance, dimensions)
    # Generate all the known captain hits to NOT aim for
    generateKnownCaptainHits(captainX, captainY, verticalDistance, lateralDistance, dimensions)
    
    # Iterate over each target, checking whether we've already accounted for
    # this hit (via an earlier target) or whether it will hit the captain before
    # the guard. If it will hit the guard first, increment the count.
    for i in range(len(targets)):    
        m = targets[i]

        deltaY = m[1] - captainY
        deltaX = m[0] - captainX
        deltaGCD = gcd(deltaX,deltaY)
        deltaX /= deltaGCD
        deltaY /= deltaGCD
    		    
        # We've already accounted for this hit via an earlier target (i.e.
        # (6, 4) is the same target as (3,2)), so go on to the next target
        if ((deltaY, deltaX) in guardHits):
            continue

        knownCaptainHitDistance = knownCaptainHits[(deltaY, deltaX)] if (deltaY, deltaX) in knownCaptainHits else None 
        # If shooting for the target won't hit the captain, we've found a valid
        # hit! Increment the count, mark it as seen, and go on to the next target
        if (not knownCaptainHitDistance):
            count += 1
            guardHits.add((deltaY, deltaX))
        else:
            # If we'll hit the guard before we'd hit ourselves, then this is
            # also a valid hit! Increment the count, mark it as seen, and go
            # on to the next target
            if (deltaGCD < knownCaptainHitDistance):
                count += 1
                guardHits.add((deltaY, deltaX))

    # Clear targets and knownCaptainHits to prepare them for the next test case
    targets = []
    knownCaptainHits = {}
    
    return count


def main():
    dimensions_1 = [3, 2]
    captain_position_1 = [1, 1]
    badguy_position_1 = [2, 1]
    distance_1 = 4
    # Should print 7
    print(answer(dimensions_1, captain_position_1, badguy_position_1, distance_1))

    dimensions_2 = [300, 275]
    captain_position_2 = [150, 150]
    badguy_position_2 = [185, 100]
    distance_2 = 500
    # Should print 9
    print(answer(dimensions_2, captain_position_2, badguy_position_2, distance_2))

main()
