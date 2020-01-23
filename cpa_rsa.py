import matplotlib.pyplot as plt
import numpy as np

N_FILE_PATH = "N.txt"
MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
PATH = "./EMSE/etudiant - 12/"
NB_MEASURES = 999
FILE_FORMAT = ".txt"
KEY_LENGTH = 32

def getModulo(file_path):
    """
    Retrieve the n parameter of the RSA algorithm from 
    the specified text file
    :return: an integer corresponding to N
    """
    f = open(file_path, 'r')
    N = f.read()
    return int(N)

def read_entries(type, number):
    """
    Reads all the msg and curves file to put their data 
    into lists of int or float according to their type
    :param type: Type of data (msg or curve)
    :param number: Number of file
    :return: list of int (if type == MSG_TITLE) or 
    list of list of float (if type == TRACE_TITLE)
    """
    entries_t = []
    for k in range(number):
        file = open(PATH+type+str(k)+FILE_FORMAT, "r")
        for line in file: # read rest of lines
            if type == TRACE_TITLE:
                entries_t.append([float(x) for x in line.split()])
            else:
                entries_t.append(int(line.split()[0]))
    return entries_t

def hamming_weight(x):
    """
    Calcul the Hamming Weight of the given number
    :param x: Number you want to have the hamming weight of
    :return: an integer corresponding to the Hamming weight
    """
    return bin(x).count("1")

def M_d_mod_N(M, d, N):
    """
    Return the hamming weight of T at the end of the RSA exponentiation
    :param M: Massage (integer)
    :param d: Key (bits array)
    :param N: n parameter (n = p*q) (integer)
    :return: Hamming weight of the exponentiation result (integer)
    """
    T = M
    hw = 0 # Hamming Weight of T
    for i in range(len(d) - 2, -1, -1):
        T = (T**2) % N
        if (d[i] == 1):
            T = (T*M) % N
            if i == 0:
                # The end
                hw = hamming_weight(T)
        else:
            if i == 0:
                # The end
                T = (T**2) % N
                hw = hamming_weight(T)
    return hw

if __name__ == "__main__":
    n = getModulo(PATH + N_FILE_PATH)
    trace_t = np.asarray(read_entries(TRACE_TITLE, NB_MEASURES))
    msg_t = read_entries(MSG_TITLE, NB_MEASURES)
    d_hyp = [1] # key hypothesis initialization
    array_hw_zeros = np.zeros((NB_MEASURES, 1))
    array_hw_ones = np.zeros((NB_MEASURES, 1))
    cpt = 1
    while trace_t[0][cpt] != -1000:
        for k in range(len(msg_t)):
            d_tmp = [0] + d_hyp # 0 hypothesis
            array_hw_zeros[k] = M_d_mod_N(msg_t[k], d_tmp, n)
            d_tmp = [1] + d_hyp # 1 hypothesis
            array_hw_ones[k] = M_d_mod_N(msg_t[k], d_tmp, n)
        # print("array_hw_zeros =", array_hw_zeros)
        # print("array_hw_ones =", array_hw_ones)
        # print("trace_t[:, cpt:cpt + 1] = ", trace_t[:, cpt:cpt + 1])
        mat_corr_zeros = np.corrcoef(array_hw_zeros, trace_t[:, cpt:cpt + 1], False)
        mat_corr_ones = np.corrcoef(array_hw_ones, trace_t[:, cpt:cpt + 1], False)
        # print("mat_corr_zeros =", mat_corr_zeros)
        # print("mat_corr_ones =", mat_corr_ones)
        corr_coef_zeros = mat_corr_zeros[1][0]
        corr_coef_ones = mat_corr_ones[1][0]
        if (corr_coef_ones <= corr_coef_zeros):
            d_hyp = [0] + d_hyp
            cpt += 1
        else:
            d_hyp = [1] + d_hyp
            cpt += 2
        # print("cpt =", cpt)
    d_hyp.reverse()
    print(d_hyp)