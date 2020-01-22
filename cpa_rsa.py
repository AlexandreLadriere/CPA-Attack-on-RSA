

# file = open(".txt", "r")

# numpy.correlate
#

def hamming_weight(x):
    return bin(x).count("1")

def M_d_mod_N(M, d, N):
    C_simul = []
    T = M
    for i in range(len(d)-2, -1, -1):
        T = T**2 % N
        C_simul.append(hamming_weight(T))
        if (d[i] == 1):
            T = T*M % N
            C_simul.append(hamming_weight(T))
        else:
            C_simul.append(0)
    return C_simul
