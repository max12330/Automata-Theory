import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

def gcd(a : int , b: int) -> int:
    while b != 0:
        a , b = b , a % b
    return abs(a)

def mod1(x):
    if isinstance(x , np.ndarray ):
        r = np.mod (x , 1.0)
        r = np.where ( r < 0.0 , r + 1.0 , r)
        r = np.where ( r == 1.0 , 0.0 , r )
        return r
    r = math.fmod(x , 1.0)
    if r < 0.0:
        r += 1.0
    if r == 1.0:
        r = 0.0
    return r

def mult_order(base : int , mod : int) -> int:
    t = 1
    acc = base % mod
    while acc != 1:
        acc = ( acc * base ) % mod
        t += 1
    return t

def zi(y , c : float , q : float , l: int ):
    return mod1( c * y + mod1 (-(2**l) * q))

def plot_segments( ax , x , y , **kwargs ):
    start = 0
    for i in range(1 , len(x)):
        if abs(y [i ] - y [i - 1]) > 0.5:
            if i - start > 1:
                ax.plot (x [ start : i] , y [ start : i] , **kwargs )
            start = i
    if len(x) - start > 1:
        ax.plot(x[start : len(x)], y[start : len(x)], **kwargs)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type = int , default=2001)
    parser.add_argument('--copies', type = int , default=1)
    args = parser.parse_args()
    
    r , s = -8, 9
    r1 , s1 = -1, 7
    c = r / s
    q = r1 / s1
    
    m = s1 // gcd(s , s1 )
    multm2 = mult_order(2 , m)
    
    y = np.linspace(0.0 , 1.0 , args.k)
    
    fig , ax = plt.subplots(figsize =(6 , 6))
    ax.set_xlim(0 , 1)
    ax.set_ylim(0 , 1)
    ax.set_aspect('equal')
    ax.grid (True , alpha =0.3)
    
    colors = ['#3366cc' , '#cc3366', '#33aa88', '#000000']
    for l in range (multm2) :
        for i_shift in range (-args.copies , args.copies + 1) :
            for j_shift in range (-args.copies , args.copies + 1) :
                x_vals = y
                z_vals = zi (y + i_shift , c , q , l) + j_shift
                mask = (z_vals >= 0.0) & (z_vals <= 1.0)
                if np.any(mask):
                    xv = x_vals[mask]
                    zv = z_vals[mask]
                    if len ( xv ) >= 2:
                        plot_segments(ax , xv , zv , color = colors [l % len ( colors) ], linewidth =1.2 , alpha=0.9)
    ax.set_title (f'c = { r }/{ s} , q = { r1 }/{ s1 }; m = {m} , mult_m (2) = { multm2 }')
    ax.set_xticks([0.0 , 0.2 , 0.4 , 0.6 , 0.8 , 1.0])
    ax.set_yticks([0.0 , 0.2 , 0.4 , 0.6 , 0.8 , 1.0])
    plt.tight_layout ()
    plt.show ()
if __name__ == '__main__':
    main ()