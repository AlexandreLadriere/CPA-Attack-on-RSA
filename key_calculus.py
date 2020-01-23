from cpa_rsa import *

def prime_factors(n):
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
   x, lastx, y, lasty = 0, 1, 1, 0
   while b != 0:
       a, (quotient, b) = b, divmod(a, b)
       x, lastx = lastx - quotient * x, x
       y, lasty = lasty - quotient * y, y
   return a, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)


def invmod(a, m):
   g, x, y = extended_gcd(a, m)
   if g != 1:
       raise ValueError
   return x % m

if __name__ == "__main__":
    e = 65537
    n = getModulo(PATH + N_FILE_PATH)
    (p, q) = prime_factors(n)
    fi_n = (p-1) * (q-1)
    d = invmod(e, fi_n)
    print("d (dec) =", d)
    print("d (bin) =", bin(d))
