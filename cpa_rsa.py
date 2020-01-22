import matplotlib.pyplot as plt
import numpy as np

N_FILE_PATH = "N.txt"
MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
PATH = "./EMSE/etudiant - 12/"
NB_MEASURES = 999
FILE_FORMAT = ".txt"

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
    if (d[-1] == 1):
        T = T*M % N
        return hamming_weight(T)
    else:
        return 0

if __name__ == "__main__":
    mod = getModulo(PATH + N_FILE_PATH)
    trace_t = read_entries(TRACE_TITLE, NB_MEASURES)
    msg_t = read_entries(MSG_TITLE, NB_MEASURES)

    d_hyp_init = [[0, 0], [0, 1], [1, 0], [1, 1]]
    C_simul_t = np.zeros((len(msg_t), len(d_hyp_init)))
    for i in range (len(d_hyp_init)):
        d = d_hyp_init[i]
        for k in range (len(msg_t)):
            msg = msg_t[k]
            C_simul_t[k, i] = M_d_mod_N_last_d_bit(msg, d, mod)
    correl = np.correlate(trace_t[:][1], C_simul_t)
    indices = np.where(correl == np.amax(correl))
    print(d_hyp_init[indices[1]])
