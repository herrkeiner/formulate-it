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
        return score*1.0/len(str(expr))
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
                q = "INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, %s, %s, %s)"
                cursor.execute(q, (2, True, True, json.dumps({'2': 1})))
                cursor.execute(q, (3, True, True, json.dumps({'3': 3})))
                cnx.commit()
                self.primes_list = [2, 3]
            cursor.close()
            cnx.close()
        else: self.primes_list = [2, 3]

    def __iter__(self):
        self.prime_candidate = self.primes_list[-1] + 2
        return self

    def __next__(self):
        if self.counter < len(self.primes_list):
            self.counter += 1
            return self.primes_list[self.counter-1]
        elif self.availableRecords > len(self.primes_list):
            cnx = dbcModule.connect()
            if cnx:
                cursor = cnx.cursor()
                print(self.primes_list)
                l = len(self.primes_list) + 1
                cursor.execute("SELECT id FROM math_is_fun WHERE is_prime LIMIT %s, %s", (l, l + 1000))
                for record in cursor:
                    self.primes_list.append(record[0])
                print(self.primes_list)
                cursor.close()
                cnx.close()
                return self.primes_list[self.counter]
            else: self.availableRecords = 0
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
                cnx = dbcModule.connect()
                if cnx:
                    cursor = cnx.cursor()
                    cursor.execute("INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, %s, %s, %s)", (self.primes_list[-1], True, is_palindromic(self.primes_list), json.dumps({self.primes_list[-1]: 1})))
                    cursor.close
                    cnx.commit()
                    cnx.close()
                return self.prime_candidate

            # Generate a new prime candidate
            self.prime_candidate += 2

    # Return primes list
    def primeList(self):
        return self.primes_list

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
    pass
