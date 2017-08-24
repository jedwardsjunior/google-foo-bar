"""
Please Pass the Coded Messages.py

Author: Julia Edwards
Date: August 2017
Github: jedwardsjunior



Prompt from Google foo.bar:

Please Pass the Coded Messages
==============================

You need to pass a message to the bunny prisoners, but to avoid detection,
the code you agreed to use is... obscure, to say the least. The bunnies are
given food on standard-issue prison plates that are stamped with the numbers
0-9 for easier sorting, and you need to combine sets of plates to create the
numbers in the code. The signal that a number is part of the code is that it
is divisible by 3. You can do smaller numbers like 15 and 45 easily, but
bigger numbers like 144 and 414 are a little trickier. Write a program to
help yourself quickly create large numbers for use in the code, given a
limited number of plates to work with.

You have L, a list containing some digits (0 to 9). Write a function answer(L)
which finds the largest number that can be made from some or all of these
digits and is divisible by 3. If it is not possible to make such a number,
return 0 as the answer. L will contain anywhere from 1 to 9 digits.
The same digit may appear multiple times in the list, but each element in
the list may only be used once.

Test cases
==========

Inputs:
    (int list) l = [3, 1, 4, 1]
Output:
    (int) 4311

Inputs:
    (int list) l = [3, 1, 4, 1, 5, 9]
Output:
    (int) 94311
"""


"""
digitsAddToMultipleOfThree()

This function does two things:
    1.) It sums up the elements that are passed in via l, a sorted list of ints
    2.) It concatenates these elements into the largest number that these digits
        can make

Inputs:
    (int list) l - a sorted list of digits

Output:
    A tuple, with the first element being a boolean that reflects whether or
    not the second element - the largest number that the digits in l can make -
    is divisible by 3.

"""
def digitsAddToMultipleOfThree(l):
    sum = 0
    concatenatedDigits = ""
    for element in l:
        sum += element
        concatenatedDigits += str(element)
    return (sum % 3 == 0, int(concatenatedDigits))

"""
answer()

This function finds the largest number that can be made from some or all of
the digits in l and is divisible by 3.

Inputs:
    (int list) l - a list of digits

Output:
    The largest number that is divisible by 3, or 0 if there is none.
"""
def answer(l):
    l.sort(reverse=True)
    
    # While we haven't removed all the digits from l...
    while len(l) > 0:

        # Iterate over the digits, removing one at a time (except for the
        # first pass through, where we try all of them) to see if the number
        # they make is divisble by 3
        for i in range(len(l), 0, -1):

            digitsToTry = l[0:i]
            if (i + 1 < len(l)):
                digitsToTry += l[i+1:]

            # A number that is divisible by 3 has all of its digits add to a multiple of 3
            isDivisibleByThree, number = digitsAddToMultipleOfThree(digitsToTry)
            if isDivisibleByThree:
                return number

        # Remove the smallest digit from l
        l.pop()

    return 0

def main():
    test1 = l = [3, 1, 4, 1]
    # Should print 4311
    print(answer(test1))
    test2 = [3, 1, 4, 1, 5, 9]
    # Should print 94311
    print(answer(test2))

main()
