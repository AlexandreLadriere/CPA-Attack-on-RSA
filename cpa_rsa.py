import numpy as np
from utils import *

corr_coeff_y1 = [] # for report purpose
corr_coeff_y0 = [] # for report purpose

def M_d_mod_N(M, d, N):
    """
    Return the hamming weight of T at the end of the RSA exponentiation
    :param M: Massage (integer)
    :param d: Key (array of integer (0, 1))
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

def keyCalculationByCPA(n, traces, messages):
    """
    Compute the secret key from cypher msg and traces
    :param n: the modulus (integer)
    :param traces: Traces retrieved when the RSA computation was made (list of list of foat)
    :param messages: Cyper msg (list of integer)
    :return: Secret key (array of integer (0, 1))
    """
    d_hyp = [1] # key hypothesis initialization
    array_hw_zeros = np.zeros((NB_MEASURES, 1))
    array_hw_ones = np.zeros((NB_MEASURES, 1))
    cpt = 1
    while traces[0][cpt] != -1000:
        for k in range(len(messages)):
            d_tmp = [0] + d_hyp # 0 hypothesis
            array_hw_zeros[k] = M_d_mod_N(messages[k], d_tmp, n)
            d_tmp = [1] + d_hyp # 1 hypothesis
            array_hw_ones[k] = M_d_mod_N(messages[k], d_tmp, n)
        mat_corr_zeros = np.corrcoef(array_hw_zeros, traces[:, cpt:cpt + 1], False)
        mat_corr_ones = np.corrcoef(array_hw_ones, traces[:, cpt:cpt + 1], False)
        corr_coef_zeros = mat_corr_zeros[1][0]
        corr_coef_ones = mat_corr_ones[1][0]
        corr_coeff_y1.append(corr_coef_ones)
        corr_coeff_y0.append(corr_coef_zeros)
        if (corr_coef_ones <= corr_coef_zeros): # it is highly possible that it is a 0
            d_hyp = [0] + d_hyp
            cpt += 1
        else: # it is highly possible that it is a 1
            d_hyp = [1] + d_hyp
            cpt += 2
    d_hyp.reverse()
    return d_hyp

def keyCalculationByFactoring():
    """
    Compute the secret key by factoring the mod
    :return: The secret key d (integer)
    """
    n = getModulo(PATH + N_FILE_PATH)
    (p, q) = prime_factors(n)
    fi_n = (p-1) * (q-1)
    d = invmod(E, fi_n)
    return d

def saveKey(file_path, key_cpa, key_fac):
    """
    Save the keys (in bin and dec format) found by factoring and CPA calculation in a file
    :param file_path: Path for the output file (string)
    :param key_cpa: Key found by CPA (integer)
    :param key_dec: Key found by factoring (integer)
    :return: None
    """
    f = open(file_path, 'w+')
    f.write("KEY CALCULATED BY FACTORING N")
    f.write("\nKey (bin): " + str(bin(key_fac)))
    f.write("\nKey (dec): " + str(key_fac))
    f.write("\n\nKEY CALCULATED BY CPA")
    f.write("\nKey (bin): " + str(bin(key_cpa)))
    f.write("\nKey (dec): " + str(key_cpa))
    f.close()

if __name__ == "__main__":
    n = getModulo(PATH + N_FILE_PATH)
    trace_t = np.asarray(read_entries(TRACE_TITLE, NB_MEASURES))
    msg_t = read_entries(MSG_TITLE, NB_MEASURES)
    key_cpa = keyCalculationByCPA(n, trace_t, msg_t)
    key_cpa_int = convertBinListToInt(key_cpa)
    key_fac_int = keyCalculationByFactoring()
    print("Key (by factoring) =", bin(key_fac_int))
    print("Key (by CPA) =", bin(key_cpa_int))
    print("Equal Keys: ", key_fac_int == key_cpa_int)
    saveKey(KEY_PATH, key_cpa_int, key_fac_int)
    plot_correlation_histogram(corr_coeff_y0, corr_coeff_y1)
