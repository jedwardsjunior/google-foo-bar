"""
Queue To Do.py

Author: Julia Edwards
Date: August 2017
Github: jedwardsjunior



Prompt from Google foo.bar:

Queue To Do
===========

You're almost ready to make your move to destroy the LAMBCHOP doomsday device,
but the security checkpoints that guard the underlying systems of the LAMBCHOP
are going to be a problem. You were able to take one down without tripping any
alarms, which is great! Except that as Commander Lambda's assistant, you've
learned that the checkpoints are about to come under automated review, which
means that your sabotage will be discovered and your cover blown - unless you
can trick the automated review system.

To trick the system, you'll need to write a program to return the same security
checksum that the guards would have after they would have checked all the
workers through. Fortunately, Commander Lambda's desire for efficiency won't
allow for hours-long lines, so the checkpoint guards have found ways to quicken
the pass-through rate. Instead of checking each and every worker coming through,
the guards instead go over everyone in line while noting their security IDs,
then allow the line to fill back up. Once they've done that they go over the
line again, this time leaving off the last worker. They continue doing this,
leaving off one more worker from the line each time but recording the security
IDs of those they do check, until they skip the entire line, at which point
they XOR the IDs of all the workers they noted into a checksum and then take
off for lunch. Fortunately, the workers' orderly nature causes them to always
line up in numerical order without any gaps.

For example, if the first worker in line has ID 0 and the security checkpoint
line holds three workers, the process would look like this:
0 1 2 /
3 4 / 5
6 / 7 8 <- 1000         0 = 0000, 1 = 0001, 2 = 0010 3 - 0011
                        
                        
where the guards' XOR (^) checksum is 0^1^2^3^4^6 == 2.

Likewise, if the first worker has ID 17 and the checkpoint holds four workers,
the process would look like:
17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32
which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.

All worker IDs (including the first worker) are between 0 and 2,000,000,000
inclusive, and the checkpoint line will always be at least 1 worker long.

With this information, write a function answer(start, length) that will cover
for the missing security checkpoint by outputting the same checksum the guards
would normally submit before lunch. You have just enough time to find out the
ID of the first worker to be checked (start) and the length of the line (length)
before the automatic review occurs, so your program must generate the proper
checksum with just those two values.

Test cases
==========

Inputs:
    (int) start = 0
    (int) length = 3
Output:
    (int) 2

Inputs:
    (int) start = 17
    (int) length = 4
Output:
    (int) 14
"""

maxWorkerId = 2000000000

def answer(start, length):
    # Edge case: the length of the line starts at 1, so just return
    # the start value
    if (length < 2):
        return start
    
    # Since the largest workerId will be 2,000,000,000,
    # we will need 31 bits (up to 2^30 == 1,073,741,824)
    # to represent the range of possible values
    xOrBits = [0 for x in range(31)]
    xOrDivider = 1

    # We will only process a number of lines equal to length,
    # as after that the guards will take off for lunch 
    for line in range(length):
        offset = start + (line * length)
        startRange = offset
        
        # If startRange is greater than 2,000,000,000, then we
        # know that no other workers will be in line so we can break
        if (startRange > maxWorkerId):
            break
        
        endRange = offset + length - line
        # If endRange is greater than 2,000,000,000, then cut the line
        # off at 2,000,000,000 since we know there won't be any workers
        # after that
        if (endRange > maxWorkerId):
            endRange = maxWorkerId + 1       

        # Iterate over all the bits (in reverse order, since the 30th
        # index corresponds to the "1"-value bit) to figure out if we
        # need to flip any
        for xOrIndex in range(30, -1, -1):
            x = endRange % (xOrDivider * 2) - xOrDivider
            y = startRange % (xOrDivider * 2) - xOrDivider
            xOrDivider *= 2
            
            # The 1-bit index is a special case, since 1 is the only
            # odd power of two
            if (xOrIndex == 30):
                if ((endRange // 2 - startRange // 2) % 2 == 1):
                    xOrBits[xOrIndex] ^= 1
                    continue

            # If x and y are both less than 0, it means that we start and
            # end on a 0 and have an even number of 1s for this bit
            if (x < 0 and y < 0):
                continue

            x = 0 if x < 0 else x
            y = 0 if y < 0 else y
            # If there are an odd number of 1s for this bit value in
            # this range, then flip the bit
            if ((x + y) % 2 == 1):
                xOrBits[xOrIndex] ^= 1

        xOrDivider = 1

    # Concatenate xOrBits into a string         
    xor = ''.join(map(str, xOrBits))
    return int(xor, 2)

def main():
    start1 = 0
    length1 = 3
    # Should print 2
    print(answer(start1, length1))

    start2 = 17
    length2 = 4
    # Should print 14
    print(answer(start2, length2))

main()
    
