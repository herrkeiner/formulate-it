#!/usr/bin/python
'''
    ...
'''

import database_connection as dbcModule
import json, re

def score(expr):
    """
    Calculates the score for a given expression according to some criteria:
    - shortness( shortness(int) ) // Done
    - is an exact power( is_exact_power(int) ) // Done
    - is prime( is_prime(int) ) // Done
    - is factorial( is_factorial(int) ) // Done
    - is palindromic( is_palindromic(str/number) ) // Done
    - has repeated digits( has_repeated(int) ) // Done
    - has sequential digits( has_sequential(int) ) // Done
    """
    score = 0
    if type(expr) is int:  # if it is a number
        if is_palindromic(expr):
            score += 5
        return score/len(str(expr))
    elif type(expr) is str:
        #mObj = re.match(r'(\d)\s*(\*|/|+|-)\s*(\d)', expr)
        return score/len(str(expr))

class PrimeIterator:
    '''
        Iterator that generates prime numbers on the fly!
        :D
    '''

    def __init__(self):
        # Set the fundamental global variables
        self.primes_list = []
        self.availableRecords = 0
        self.counter = 0
        # Access the db in order to get the first 1000 primes
        cnx = dbcModule.connect()
        if cnx:
            cursor = cnx.cursor()
            # How many prime records are therein the database?
            cursor.execute("SELECT COUNT(id) FROM math_is_fun WHERE is_prime")
            self.availableRecords = cursor.fetchone()[0]
            # Retrive the records if the quantity is more than 2
            if self.availableRecords >= 2:
                cursor.execute("SELECT id FROM math_is_fun WHERE is_prime LIMIT 1000")
                for id in cursor:
                    self.primes_list.append(id[0])
            else:
                # if there are less than the two prime numbers in the #
                # Add them into the DB #
                q = "INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, %s, %s, %s)"
                cursor.execute(q, (2, True, True, json.dumps({'2': 1})))
                cursor.execute(q, (3, True, True, json.dumps({'3': 3})))
                cnx.commit()
                self.primes_list = [2, 3]
            cursor.close()
            cnx.close()
        # If the connection with the database fails, #
        # Set a list with the two first prime numbers #
        else: self.primes_list = [2, 3]

    def __iter__(self):
        # Set the first prime candidate
        self.prime_candidate = self.primes_list[-1] + 2
        return self

    def __next__(self):
        # If the prime list isn't exausted then
        # send the next prime number.
        if self.counter < len(self.primes_list):
            self.counter += 1
            return self.primes_list[self.counter-1]
        # Ok, It is exausted, try now to retrive more prime numbers from
        # the database
        elif self.availableRecords > len(self.primes_list):
            cnx = dbcModule.connect()
            if cnx:
                cursor = cnx.cursor()
                l = len(self.primes_list) + 1
                cursor.execute("SELECT id FROM math_is_fun WHERE is_prime LIMIT %s, %s", (l, l + 1000))
                for record in cursor:
                    self.primes_list.append(record[0])
                cursor.close()
                cnx.close()
                return self.primes_list[self.counter]
            # If the connection with the database was not successful #
            # Then set the flag to not retrive more records #
            else: self.availableRecords = 0
        # It seems that we have exhausted the number primes #
        # From both the loaded list and the database #
        # Then Let's start to generate prime number on the fly #
        while True:
            for p in self.primes_list[1:]:
                # Is it divisible by p?
                if self.prime_candidate % p == 0:
                    break;

            # Have we exhausted the primes list? and haven't we found \\
            # any number which        # Set the first prime candidate
            # Therefore we've found a new prime number
            if self.prime_candidate % p != 0:
                self.primes_list.append(self.prime_candidate)
                # Insert the discovered prime number into the DB #
                cnx = dbcModule.connect()
                if cnx:
                    cursor = cnx.cursor()
                    cursor.execute("INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, %s, %s, %s)", (self.primes_list[-1], True, is_palindromic(self.primes_list), json.dumps({self.primes_list[-1]: 1})))
                    cursor.close()
                    cnx.commit()
                    cnx.close()
                return self.prime_candidate

            # Generate a new prime candidate
            self.prime_candidate += 2

    # Return primes list
    def primeList(self):
        return self.primes_list

def is_exact_power(number):
    '''
        Returns True if arg is an exact power of a certain number.
        Otherwise returns False.
    '''

    if not type(number) is int:
        return None

    # Gets its absolute number
    number = abs(number)
    # Let's check if we arelady have the prime factorization in the database
    cnx = dbcModule.connect()
    if cnx:
        cursor = cnx.cursor()
        cursor.execute("SELECT is_prime, factorization FROM math_is_fun WHERE id = %s", (number,))
        # Does the record exists?
        nData = cursor.fetchone()
        if nData:
            # Is it a prime number ?
            if nData[0]:
                return False
            # Does the number has only one prime factor?
            if len(json.loads(nData[1])) == 1:
                return True
            else: return False
        cursor.close()
        cnx.close()

    pIterator = PrimeIterator()

    pFact = [{}, number]
    # Let's ascertain if it's an exact power
    for p in pIterator:
        # Okay, is the number disivible by p?
        if number % p == 0:
            # Sets the key as the divisor, and the power counter of our number
            pFact[0][p] = 0
            # Let's divide the number and check if it has another prime factor
            while number != 1:
                # Okay, the number is not 1
                # Does the next division by p has a remainder?
                if number % p:
                    return False
                number /= p
                pFact[0][p] += 1
            # Okay we have divided the number for only one prime number
            # And the final result is 1
            # As it has only one prime number divisor
            # And it IS NOT a prime number
            # Therefore it is an exact power
            break;
    # Okay, the number is an exact power, so let's record it in the database
    cnx = dbcModule.connect()
    if cnx:
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, False, %s, %s)", (pFact[1], is_palindromic(pFact[1]), json.dumps(pFact[0])))
        cnx.commit()
        cursor.close()
        cnx.close()
    return True

def is_factorial(number):
    '''
        If the arg is a number returns either True or False based on the condition if the number is a factorial.
        Otherwise return None.
    '''

    if not type(number) is int:
        return None

    (factorial, factorial_result) = (1, 1)

    while number > factorial_result:
        factorial += 1
        factorial_result *= factorial

    if number == factorial_result:
        return True
    else: return False

def is_palindromic(number):
    '''
        Syntax: is_palindromic(arg1)

        Returns True if arg1 is a palindromic number.
    '''

    if type(number) != 'str':
        number = str(number)

    if number == number[::-1]:
        return True
    else:
        return False

def is_prime(number):
    '''
        If arg is an integer number, returns either True or False based on if it is a prime number.
        Otherwise returns None.
    '''
    if not type(number) is int:
        return None

    # Get its absolute number
    number = abs(number)

    if len(prime_fact(number)) == 1:
        return True
    else: return False

def has_repeated(number):
    '''
        If arg is an intenger, returns either True or False if it has repeated digits.
        Otherwise returns None.
    '''

    if not type(number) is int:
        return None

    number = str(abs(number))

    return False if number != (number[0] * len(number)) else True


def has_sequential(number):
    '''
        If arg is an integer number, returns the length of the group of digits which are in sequence.
        The higher the value returned, the more common is the ocurrances of that kind.
        Returns False otherwise.
    '''

    if not type(number) is int:
        return None

    # Gets its absolute number
    number = abs(number)

    # If the number has only one digit, then it has no sequence.
    if number < 11:
        return False

    number = str(number)
    length = len(number)
    # Gets the max group length of the possible sequence
    max = length // 2

    while max:
        p = int(number[:max])

        number_length = length
        sequence = ''
        i = 0

        while number_length > 0:
            sequence += str(p + i)
            number_length -= len(str(p + i))
            i += 1

        if number == sequence: return 1.5 ** (length // max)
        else:
            p = int(number[-max:])

            sequence = ''
            number_length = length
            i = 0

            while number_length > 0:
                sequence = str(p + i) + sequence
                number_length -= len(str(p + i))
                i += 1

            if number == sequence: return 1.5 ** (length // max)

        max -= 1
    # Have we exhausted all the possible lengths?
    return False

def prime_fact(number):
    '''
        Syntax: prime_fact(arg)

        If the arg is a integer, returns the factorization within a dictionary.
        Otherwise ValueError exception is raised.
    '''
    # Argument must be an integer.
    if not type(number) is int:
        raise ValueError

    # Set var number to its absolute value.
    number = abs(number)

    factors_dic = dict()

    # abs(number) must not be zero and it must be > |1|.
    if number <= 1:
        return factors_dic

    primes_baby = PrimeIterator()

    # Factorization of the number
    for factor_candidate in primes_baby:
        # Checks if our number is divisible for the last retrieved prime
        if number % factor_candidate == 0:
            factors_dic[factor_candidate] = 0
            # Hm, It is, bitch! Therefore, let's see how many times it is divisible
            while number % factor_candidate == 0:
                number /= factor_candidate
                factors_dic[factor_candidate] += 1

        # Have we finished our factorization?
        if number == 1:
            return factors_dic

def shortness(number):
    '''
        If arg is an intenger number, returns a number which corresponds to
        1.75 to the power of the amount of digits which arg has - 1.
        Otherwise returns None.
    '''
    if not type(number) is int:
        return None

    return 1.75 ** (len(str(number)) - 1)

if __name__ == "__main__":
    score('123 * 123')
    pass
