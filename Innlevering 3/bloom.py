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
    for f in hashing_functions:
        hash_value = f(new_pass)
        bloom_filter_array[hash_value] = 1

    return bloom_filter_array

# Method to create a new bloom filter


def bloom_filter_array():
    n = parameters_dictionary.get("n")
    return [0] * n

# DO NOT CHANGE THIS METHOD
# Reads all the passwords one by one simulating a stream and calls the method bloom_filter(new_password)
# for each password read

# Method to encode a string and assign it a numerical value


def encode_string(s):
    enc = []
    for char in s:
        enc.append(ord(char))
    return (enc)


def read_data(file, hashing_functions, array):
    time_sum = 0
    pass_read = 0
    with file.open(encoding='cp437') as f:
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
    for q in range(h):
        cont = True
        while cont:
            # Generate a random number in the range [lower_bound, upper_bound]
            p = random.randint(0, 10000)

            # Check if the number is prime and different from the previous primes chosen
            if is_prime(p) & p not in primes:
                cont = False
                primes.append(p)

    for l in range(h):
        p = primes[l]

        def hash_function(s, p=p):
            num = 0
            s = encode_string(s)
            for i in range(len(s)):
                num += s[i] * p ** i
            return num % n
        hash_functions.append(hash_function)

    return hash_functions


# Method to check if a password may be in the bloom filter
def check_password(password, hash_functions, bloom_filter):
    present = []
    for f in hash_functions:
        hash_value = f(password)
        if bloom_filter[hash_value] == 1:
            present.append(1)
        else:
            present.append(0)
    if 0 in present:
        return False
    else:
        return True


if __name__ == '__main__':
    # Reading the parameters
    read_parameters()

    # Creating the hash functions
    hashing_functions = hash_functions()

    array = bloom_filter_array()

    # Reading the data
    print("Stream reading...")
    data_file = (data_main_directory /
                 parameters_dictionary['data']).with_suffix('.csv')
    passwords_read, times_sum = read_data(data_file, hashing_functions, array)
    print(passwords_read, "passwords were read and processed in average", times_sum / passwords_read,
          "sec per password\n")

    # A list of passwords we know are not in the passwords.csv file
    passwords_not_in_passwords_csv_file = ['07886819', '0EDABE59B', '0BFE0815B', '01058686E', '09DFB6D3F', '0F493202C', '0CA5E8F91', '0C13EC1D9', '05EF96537', '03948BA8F', '0D19FB394', '0BF3BD96C', '0D3665974', '0BBDF91E9', '0A6083B64', '0D76EF8EC', '096CD1830', '04000DE73', '025C442BA', '0FD6CAA0A', '06CC18905', '0998DDE00', '02BAACDC4', '0D58264FC', '0CB8911AA', '0CF9E0BDC', '007B7F82F', '0948FD17A', '058BB08DB', '02EDBE8CA', '0D6F02EFD', '09C9797FB', '0F8CB3DA5', '0C2825430', '038BE7E61', '03F69C0F5', '07EB08903', '0917C741D', '0D01FEE8F', '01B09A600', '0BD197525', '06B6A2E60', '0B72DEF61', '095B17373', '0B6E0EEB1', '0078B3053', '08BD9D53F', '01995361F', '0F0B50CAE',
                                           '0B5D2887E', '004EB658C', '0D2C77EDB', '07221E24D', '0E8A4CC90', '00E947367', '0DBE190BB', '0D8726592', '06C02D59D', '0462B8BC6', '0F85122F8', '0FA1961EB', '035230553', '04CDFB216', '0356DB0AD', '0FD947DA3', '053BB206F', '0D1772CC1', '00DB759F5', '072FB4E7A', '0B47CB62D', '0616B627F', '0F3E153BC', '0F3AC7DEE', '01286192B', '009F3C478', '07D89E83E', '007CAFDE6', '0ABC9E80B', '091D1CDA5', '0BFC208A1', '0957D4C84', '00AAF260A', '09CF00D7C', '0D1C66C72', '0EA20CA23', '07D6BE324', '05B264527', '0D48C41F6', '081E31BF5', '0A1DC7455', '07BB493D8', '050036F1B', '00E73A1EC', '0C2D93CC0', '0FF47B30C', '0313062DE', '0E1BEFA3F', '0A24D069F', '02A984386', '0367F7405']

    false_positive_count = 0

    for password in passwords_not_in_passwords_csv_file:
        if check_password(password, hashing_functions, array):
            false_positive_count += 1
    print("Number of false positives using a test set of passwords not found in the database: ",
          false_positive_count)

    # h = parameters_dictionary.get("h")
    # print("Number of hash functions: ", h)

    # n = parameters_dictionary.get("n")
    # print("Size of Bloom Filter: ", n)
