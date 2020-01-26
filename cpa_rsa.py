import matplotlib.pyplot as plt
import numpy as np
import math as ma

N_FILE_PATH = "N.txt"
MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
PATH = "./EMSE/etudiant - 12/"
NB_MEASURES = 999
FILE_FORMAT = ".txt"
KEY_LENGTH = 32

def getModulo(file_path):
    f = open(file_path, 'r')
    N = f.read()
    return int(N)

def read_entries(type, number):
    entries_t = []
    for k in range(number):
        file = open(PATH+type+str(k)+FILE_FORMAT, "r")
        for line in file: # read rest of lines
            if type == TRACE_TITLE:
                entries_t.append([float(x) for x in line.split()])
            else:
                entries_t.append(int(line.split()[0]))
    return entries_t

# numpy.correlate

def hamming_weight(x):
    return bin(x).count("1")

def M_d_mod_N_last_d_bit(M, d_hyp, N):
    T = M
    for i in range(len(d_hyp)-2, -1, -1):
        T = T**2 % N
        if (d_hyp[i] == 1):
            T = T*M % N
    return hamming_weight(T)

def list_to_binary(x):
    return bin(int(''.join(map(str, x)), 2) << 1)

if __name__ == "__main__":
    mod = getModulo(PATH + N_FILE_PATH)
    trace_t = np.asarray(read_entries(TRACE_TITLE, NB_MEASURES))
    msg_t = read_entries(MSG_TITLE, NB_MEASURES)

    d_hyp = [1]
    for bit in range(32):
        d_hyp = [[0] + d_hyp, [1] + d_hyp]
        C_simul_t = np.zeros((len(msg_t), len(d_hyp)))
        for i in range (len(d_hyp)):
            d = d_hyp[i]
            for k in range (len(msg_t)):
                msg = msg_t[k]
                C_simul_t[k, i] = M_d_mod_N_last_d_bit(msg, d, mod)
        correl = np.zeros((len(d_hyp), len(trace_t[0])))
        for i in range(len(d_hyp)):
            for k in range (len([val for val in trace_t[0] if val!=-1000])):
                correl[i, k] = np.corrcoef(trace_t[:, k], C_simul_t[:, i])[0, 1]
        print(correl)

        maxi = -999
        imax = 0
        for i in range(len(d_hyp)):
            if (max(correl[i]) > maxi):
                maxi = max(correl[i])
                imax = i
        d_hyp = d_hyp[imax]

    print("Key found: \n", list_to_binary(d_hyp))
    print("Key found (reversed): \n", list_to_binary(d_hyp[::-1]))
    print("Real key: \n 0b101101100000001011110000001")
