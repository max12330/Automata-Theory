import numpy as np
import matplotlib.pyplot as plt
from colorsys import hsv_to_rgb
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod1(a):
    a = a - int(a)
    if a < 0:
        return a + 1
    return a

def zi(y, c, q, l):
    return mod1(c * y + mod1(-(2 ** l) * q))

r, s, r_prime, s_prime = 17, 19, -1, 15
c = r / s
q = r_prime / s_prime
m = s_prime // gcd(s, s_prime)
mult_m_p = 1
while (2 ** mult_m_p) % m != 1 and m > 1:
    mult_m_p += 1
k = 10
p_k = 1 << k
y = np.linspace(0, 1, p_k)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

random.seed(42)
colors1 = ['red', 'blue']
for i in range(2):
    z = np.array([zi(yj, c, q, i) for yj in y])
    ax1.scatter(y, z, s=3, color=colors1[i], alpha=0.8, label=f'z_{i}')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('x')
ax1.set_ylabel('g(x) mod 1')
ax1.set_title('2 обмотки тора (shift=0)')
ax1.legend()

random.seed(42)
for i in range(mult_m_p):
    hue = random.random()
    saturation = 0.7
    lightness = 0.5
    color = hsv_to_rgb(hue, saturation, lightness)
    for shift in range(s):
        z = np.array([zi(yj + shift, c, q, i) for yj in y])
        ax2.scatter(y, z, s=2, color=color, alpha=0.8)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect('equal')
ax2.grid(False)
ax2.set_xlabel('x')
ax2.set_ylabel('g(x) mod 1')
ax2.set_title('Полные обмотки тора g(x) = 17/19x - 1/15')

plt.tight_layout()
plt.savefig('g.png', dpi=150, bbox_inches='tight')
plt.show()

