# This is the code for the Bloom Filter project of TDT4305

import configparser  # for reading the parameters file
from pathlib import Path  # for paths of files
import time  # for timing
import random

# Global parameters
parameter_file = 'default_parameters.ini'  # the main parameters file
# the main path were all the data directories are
data_main_directory = Path('data')
# dictionary that holds the input parameters, key = parameter name, value = value
parameters_dictionary = dict()


# DO NOT CHANGE THIS METHOD
# Reads the parameters of the project from the parameter file 'file'
# and stores them to the parameter dictionary 'parameters_dictionary'
def read_parameters():
    config = configparser.ConfigParser()
    config.read(parameter_file)
    for section in config.sections():
        for key in config[section]:
            if key == 'data':
                parameters_dictionary[key] = config[section][key]
            else:
                parameters_dictionary[key] = int(config[section][key])


# TASK 2
def bloom_filter(new_pass, hashing_functions, bloom_filter_array):

    # implement your code here
    n = parameters_dictionary.get("n")

    # password = new_pass.h
    return 0


def bloom_filter_array():
    n = parameters_dictionary.get("n")
    return [0] * n

# DO NOT CHANGE THIS METHOD
# Reads all the passwords one by one simulating a stream and calls the method bloom_filter(new_password)
# for each password read


def read_data(file, hashing_functions):
    time_sum = 0
    pass_read = 0
    array = bloom_filter_array()
    with file.open() as f:
        for line in f:
            pass_read += 1
            new_password = line[:-3]
            ts = time.time()
            bloom_filter(new_password, hashing_functions, array)
            te = time.time()
            time_sum += te - ts

    return pass_read, time_sum

# Helper method to check if number is prime


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0:
            return False
        if n % (f+2) == 0:
            return False
        f += 6
    return True

# TASK 1
# Created h number of hash functions


def hash_functions():

    # implement your code here
    h = parameters_dictionary.get("h")
    n = parameters_dictionary.get("n")
    primes = []
    hash_functions = []

    for i in range(h):
        cont = True
        while cont:
            # Generate a random number in the range [lower_bound, upper_bound]
            p = random.randint(0, 10000)

            # Check if the number is prime
            if is_prime(p) & p not in primes:
                cont = False
                primes.append(p)

        def hash_function(s):
            num = 0
            for i in range(len(s)):
                num += s[i] * p ** i
            return num % n
        hash_functions.append(hash_function)

    return hash_functions


if __name__ == '__main__':
    # Reading the parameters
    read_parameters()

    # Creating the hash functions
    hashing_functions = hash_functions()

    # Reading the data
    print("Stream reading...")
    data_file = (data_main_directory /
                 parameters_dictionary['data']).with_suffix('.csv')
    passwords_read, times_sum = read_data(data_file, hashing_functions)
    print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")
