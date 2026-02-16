import numpy as np
import matplotlib.pyplot as plt

def pmod(a, k):
    mod = 1 << k
    return (a % mod + mod) % mod

def f(x):
    return 18 + x - 7*x*x
    '''
    return (x ^ 1) ^ (2 * (x & (1 + 2 * x) 
            & (3 + 4 * x) & (7 + 8 * x) & (15 + 16 * x) 
            & (31 + 32 * x) & (63 + 64 * x))) \
            ^ (4 * (x * x + 29))
    '''

a = 15
r = 3

for k in range(a, a + r * 2):
    p_k = 1 << k
    x = np.arange(p_k) / p_k
    fx = np.array([pmod(f(i), k) / p_k for i in range(p_k)])
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.scatter(x, fx, s=8, color='blue', alpha=0.5, edgecolors='none')
    ax.set_title(f'f(x) projections, k = {k}', fontsize=16)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x) mod 2^k', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'f(x)plot_k{k}.png', dpi=150, bbox_inches='tight')
    plt.show()
