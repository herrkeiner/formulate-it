'''
    ...
'''

import database_connection as dbcModule
import json

def score(expr):
    """"
    Calculates the score for a given expression according to some criteria:
    - shortness
    - is an exact power
    - is prime
    - is factorial
    - is palindromic
    - has repeated digits
    - has sequential digits
    """
    score = 0
    if type(expr) == 'int':  # if it is a number
        if is_palindromic(expr):
            score += 5
        return score/len(str(expr))
    else:  # if it is a complex expression
        # parse expression into numbers
        # sum score of each number

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
    """
        Returns True if arg is a exact power of a certain number.
        Otherwise returns False.
    """

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

def prime_fact(number):
    '''
        Syntax: prime_fact(arg)

        If the arg is a integer returns the factorization within a dictionary.
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

    #cnx = dbcModule.connect()
    #if cnx:
    #    cursor = cnx.cursor()
    #    cursor.execute("SELECT factorization FROM math_is_fun WHERE id = %s", number)
    #    factors_dic = json.loads(cursor.next())
    #    if len(factors_dic):
    #        cursor.close()
    #        cnx.close()
    #        return factors_dic

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

if __name__ == "__main__":
    print(is_exact_power(4))
    print(is_exact_power(128))
    print(is_exact_power(1024))
    print(is_exact_power(64))
    print(is_exact_power(2))
    print(is_exact_power(-15))
