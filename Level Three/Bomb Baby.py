"""
Queue Bomb Baby.py

Author: Julia Edwards
Date: August 2017
Github: jedwardsjunior



Prompt from Google foo.bar:

Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it!
But in order to do so, you need to deploy special self-replicating bombs
designed for you by the brightest scientists on Bunny Planet. There are two
types: Mach bombs (M) and Facula bombs (F). The bombs, once released into
the LAMBCHOP's inner workings, will automatically deploy to all the strategic
points you've identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two
distinct processes:

Every Mach bomb retrieves a sync unit from a Facula bomb;
    for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either
produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs.
The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and
Facula bombs to destroy the LAMBCHOP device. Too few, and the device might
survive. Too many, and you might overload the mass capacitors and create a
singularity at the heart of the space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one
Mach, one Facula - aboard the ship when you arrived, so that's all you have
to start with. (Thus it may be impossible to deploy the bombs to destroy the
LAMBCHOP, but that's not going to stop you from trying!) 

You need to know how many replication cycles (generations) it will take to
generate the correct amount of bombs to destroy the LAMBCHOP. Write a
function answer(M, F) where M and F are the number of Mach and Facula bombs
needed. Return the fewest number of generations (as a string) that need to
pass before you'll have the exact number of bombs necessary to destroy the
LAMBCHOP, or the string "impossible" if this can't be done! M and F will be
string representations of positive integers no larger than 10^50. For example,
if M = "2" and F = "1", one generation would need to pass, so the answer would
be "1". However, if M = "2" and F = "4", it would not be possible.

Test cases
==========

Inputs:
    (string) M = "2"
    (string) F = "1"
Output:
    (string) "1"

Inputs:
    (string) M = "4"
    (string) F = "7"
Output:
    (string) "4"
"""

def answer(m, f):
    m = int(m)
    f = int(f)

    generationCount = 0
    # Once either m or f are less than 1, we know we've hit a point where we
    # can either 1.) say that this combination is impossible or 2.) finish up
    # the calculation of the generation count
    while(m > 1 and f > 1):
        # If m < f, we know we got to this m by adding f to (m - f)
        if (m < f):
            # Short cut to avoid having to calculate each m - f
            generationCount += f // m
            f %= m
        # If f < m, we know we got to this f by adding m to (f - m)
        else:
            # Short cut to avoid having to calculate each f - m
            generationCount += m // f
            m %= f

    # If either one is less than 1 at this point, then we know it's an
    # invalid combination
    if (m < 1 or f < 1):
        return "infinity"

    # At this point, if either m or f are greater than 1 then add the number
    # of generations equal to m - 1 or f - 1 (because we start with one of each
    # bomb, and we can only get to m or f by replicating the other bomb that
    # number of times)
    if (m > 1):
        generationCount += m - 1
    elif (f > 1):
        generationCount += f - 1
        
    return str(generationCount)

def main():
    m1 = "2"
    f1 = "1"
    # Should print "1"
    print(answer(m1, f1))

    m2 = "4"
    f2 = "7"
    # SHould print "4"
    print(answer(m2, f2))

main()
