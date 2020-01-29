import numpy as np
from matplotlib import pyplot as plt

DATA_SET = "12" # Data set number
NB_MEASURES = 999 # Number of measures
KEY_LENGTH = 32 # Length of the key
E = 65537 # e parameter of the RSA algorithm
FILE_FORMAT = ".txt" # File format used for measures and results output
MSG_TITLE = "msg_" # File name format for messages
TRACE_TITLE = "curve_" # File name format for traces
N_FILE_PATH = "N" + FILE_FORMAT # File path for the parameter N
PATH = "./EMSE/etudiant - " + DATA_SET + "/" # Path of the data set used
KEY_PATH = "./d_" + DATA_SET + FILE_FORMAT # Path of the output key file

def prime_factors(n):
    """
    Compute the prime factors of the given number
    :param n: Number you want to compute the prime factors (intger)
    :return: Prime factors of the given number (list of integer)
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def extended_gcd(a, b):
    """
    Get the gcd of the given numbers
    :param a: First number (integer)
    :param b: Second number (integer)
    :return: gcd of a and b (integer)
    """
    x, lastx, y, lasty = 0, 1, 1, 0
    while b != 0:
       a, (quotient, b) = b, divmod(a, b)
       x, lastx = lastx - quotient * x, x
       y, lasty = lasty - quotient * y, y
    return a, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)


def invmod(a, m):
    """
    Compute the modular mutliplicative inverse
    of the given number mod the second number
    :param a: Number you want to know the mod inverse (integer)
    :param m: mod (integer)    print("d (bin) =", bin(d))
    :return: the modular inverse (integer)
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
       raise ValueError
    return x % m

def getModulo(file_path):
    """
    Retrieve the n parameter of the RSA algorithm from
    the specified text file
    :param file_path: Path of the mod file (string)
    :return: The modulus N (integer)
    """
    f = open(file_path, 'r')
    N = f.read()
    return int(N)

def read_entries(type, number):
    """
    Reads all the msg and curves file to put their data
    into lists of int or float according to their type
    :param type: Type of data (msg or curve) (string)
    :param number: Number of file (integer)
    :return: list of int (if type == MSG_TITLE) or
    list of list of float (if type == TRACE_TITLE)
    """
    entries_t = []
    for k in range(number):
        file = open(PATH + type + str(k) + FILE_FORMAT, "r")
        for line in file: # read rest of lines
            if type == TRACE_TITLE:
                entries_t.append([float(x) for x in line.split()])
            else:
                entries_t.append(int(line.split()[0]))
    return entries_t

def hamming_weight(x):
    """
    Compute the Hamming Weight of the given number
    :param x: Number you want to have the hamming weight of (integer)
    :return: athe Hamming weight (integer)
    """
    return bin(x).count("1")

def convertBinListToInt(bin_list):
    """
    Convert a binary list ([1, 0, 1, 0]) to an integer
    :param bin_list: Binary list
    :return: Integer representation of the binary list (integer)
    """
    dec = int("".join(map(str, bin_list)),2)
    return dec

def plot_correlation_histogram(corr_coeff_y0, corr_coeff_y1):
    """
    Plot an histogram of correlation coefficients
    for each bit for each hypothesis
    :param corr_coef_y0: list of correlation coefficients for bit = 0 hypothesis
    :param corr_coef_y1: list of correlation coefficients for bit = 1 hypothesis
    """
    bar_width = 0.1
    index = np.arange(len(corr_coeff_y0))
    plt.figure()
    plt.bar(index, corr_coeff_y0, bar_width, label="Hypothèse bit = 0")
    plt.bar(index+bar_width, corr_coeff_y1, bar_width, label="Hypothèse bit = 1")
    plt.ylabel("Coefficients de corrélation")
    plt.xlabel("Bit de la clé")
    plt.title("Coefficients de corrélation pour chaque bit et selon l'hypothèse de bit")
    plt.legend()
    plt.show()
