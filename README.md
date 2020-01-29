# CPA Attack on RSA

Python implementation of an attack using CPA on a simplified RSA.

## Description

The subject of this lab is in the [TP-EMSE-2020.pdf] file (in french) and the [EMSE] folder contains several data sets used for the CPA. Since it is a baby RSA, the key can be retrieved by factorization. The [cpa_rsa.py] script calculates the key by factorization but also by CPA.

## Run

First, choose the data set you want to use. In order to do that, go into the file [utils.py] and modify the value of the ```DATA_SET``` variable:
```python
DATA_SET = "12" # Data set number (10, 11, 12, 13, 14, or 15)
```

To test the script, simply run the following command:
```bash
$ python3 cpa_rsa.py
```

## Results

you will get something like the following output:
```bash
>>> Key (by factoring) = 0b101101100000001011110000001
>>> Key (by CPA) = 0b101101100000001011110000001
>>> Equal Keys:  True
```

The result will also be stored in a file called ```d_DATA-SET-NUMBER.txt``` (ex: [d_12.txt]), and a histogram will be displayed, representing the correlation factors for each bit and for each hypothesis (1 or 0).

  [TP-EMSE-2020.pdf]: <TP-EMSE-2020.pdf>
  [EMSE]: <./EMSE/>
  [cpa_rsa.py]: <cpa_rsa.py>
  [d_12.txt]: <d_12.txt>
  [utils.py]: <utils.py>