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
    T = T**2 % N
    if (d_hyp[-1] == 1):
        T = T*M % N
        return hamming_weight(T), T
    else:
        return hamming_weight(T), T

if __name__ == "__main__":
    mod = getModulo(PATH + N_FILE_PATH)
    trace_t = read_entries(TRACE_TITLE, NB_MEASURES)
    msg_t = read_entries(MSG_TITLE, NB_MEASURES)

    for bit in range(1):
        if bit == 0:
            d_hyp = [[0, 0], [0, 1], [1, 0], [1, 1]]
        else:
            d_hyp = [d_hyp + [0], d_hyp + [1]]
        C_simul_t = np.zeros((len(msg_t), len(d_hyp)))
        for i in range (len(d_hyp)):
            d = d_hyp[i]
            msg_t_i = msg_t
            for k in range (len(msg_t)):
                msg = msg_t_i[k]
                C_simul_t[k, i], msg_t_i[k] = M_d_mod_N_last_d_bit(msg_t_i[k], d, mod)
        correl = np.zeros((len(d_hyp), len(trace_t[0])))
        for i in range(len(d_hyp)):
            for k in range (len(trace_t[0])):
                cur_cor = np.corrcoef(np.asarray(trace_t)[:, k], C_simul_t[:, i])
                # if not(ma.isnan(cur_cor[0, 1])):
                #     pass
                #      # correl[i, k] = cur_cor[0, 1]
                # else:
                #     pass
                    # correl[i, k] = 0
    #     for i in range(len(d_hyp)):
    #         if (max(correl[i]) > maxi):
    #             maxi = max(correl[i])
    #             imax = i
    #     d_hyp = d_hyp[imax]
    # print(d_hyp)
