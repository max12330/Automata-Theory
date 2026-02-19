import math
import random
import colorsys
import numpy as np
import matplotlib.pyplot as plt


k = 10
p_k = 1 << k
epsilon = 1.0 / p_k

def gcd_py(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)

def mod1(a, eps=epsilon):
    if isinstance(a, np.ndarray):
        r = np.remainder(a, 1.0)
        r = np.where(r < 0.0, r + 1.0, r)
        r = np.where(np.abs(r) < eps, 0.0, r)
        return r
    r = math.fmod(a, 1.0)
    if r < 0.0:
        r += 1.0
    if abs(r) < eps:
        r = 0.0
    return r

def zi(y, c: float, q: float, l: int, eps=epsilon):
    return mod1(c * y + mod1(-(2 ** l) * q, eps), eps)

def mult_order_two(modulus: int) -> int:
    t = 1
    while (1 << t) % modulus != 1 and modulus > 1:
        t += 1
    return t

def main():
    # g(x) = r/s * x + r1/s1
    r, s = 17, 19
    r1, s1 = -1, 15
    c = r / s
    q = r1 / s1

    m = s1 // gcd_py(s, s1)
    multm2 = mult_order_two(m)

    y = np.linspace(0.0, 1.0, p_k)
    
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    rng = random.Random()
    for i in range(multm2):
        h = rng.random()
    r_c, g_c, b_c = colorsys.hls_to_rgb(h, 0.5, 0.7)
    color = (r_c, g_c, b_c)

    for shift in range(1):
        z = zi(y + shift, c, q, i, epsilon)
    ax.scatter(y, z, s=2.0, c=[color], linewidths=0)

    ax.set_title(f'c = {r}/{s}, q = {r1}/{s1}; m = {m}, mult_m (2) = {multm2}')
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    fig.tight_layout()
    fig.savefig('g_copy.png', dpi=100)

if __name__ == '__main__':
    main()
