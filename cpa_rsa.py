import matplotlib.pyplot as plt

N_FILE_PATH = "./EMSE/etudiant - 12/N.txt"


def getModulo(file_path):
    f = open(file_path, 'r')
    N = f.read()
    return N

MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
PATH = "./EMSE/etudiant - 12/"
NB_MEASURES = 999
FILE_FORMAT = ".txt"


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
#

trace_t = read_entries(TRACE_TITLE, NB_MEASURES)
msg_t = read_entries(MSG_TITLE, NB_MEASURES)
print("msg :", msg_t[18])
print("trace :", trace_t[18])

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

if __name__ == "__main__":
    print(getModulo(N_FILE_PATH))