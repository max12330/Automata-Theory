def pmod(a, k):
    #модуль по степени двойки
    m = 1 << k
    return (a % m + m) % m

def pmod_fraction(r, s, k):
    #дробь по модулю степени двойки
    if s % 2 == 0:
        raise ValueError("Знаменатель не может быть чётным для модуля 2^k")
    if k < 0:
        raise ValueError("k должно быть неотрицательным")
    ans = 0
    for i in range(k):
        A = r & 1
        R = (r - A * s) // 2
        ans |= (A << i)
        r = R
    return ans

_supers = ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹']
def print_poly_mod(name, coeffs):
    #вывод полинома
    parts = []
    for i, c in enumerate(coeffs):
        if i == 0:
            parts.append(f"{c}")
        elif i == 1:
            parts.append(f"+ {c}x")
        else:
            if i < 10:
                parts.append(f"+ {c}x{_supers[i]}")
            else:
                exp = ''.join(_supers[int(d)] for d in str(i))
                parts.append(f"+ {c}x{exp}")
    print(f"{name} = " + " ".join(parts))

def eval_table(coeffs, mod):
    #вычисляет значения полинома для всех элементов кольца
    n = len(coeffs)
    xs = list(range(mod))
    vals = []
    for x in xs:
        acc = 0
        pw = 1
        for j in range(n):
            acc = (acc + coeffs[j] * pw) % mod
            pw = (pw * x) % mod
        vals.append(acc)
    return xs, vals

def check_z4_and_z8(name, fmod4, fmod8):
    #проверка транзитивности

    # f mod 4
    print_poly_mod(f"{name} mod 4", fmod4)
    xs, vals = eval_table(fmod4, 4)
    for x, v in zip(xs, vals):
        print(f"{x} -> {v}")
    flags = 0
    for v in vals:
        flags |= 1 << v
    if flags != 0b1111:
        print("Не биекция => полином не транзитивен")
        return

    print("Полином является биекцией.\n ...Проверка транзитивности на Z8...")
    # f mod 8
    print_poly_mod(f"{name} mod 8", fmod8)
    xs8, vals8 = eval_table(fmod8, 8)
    for x, v in zip(xs8, vals8):
        print(f"{x} -> {v}")

    pin = 0
    seen = 0
    for _ in range(8):
        pin = vals8[pin]
        seen |= 1 << pin
    if seen == 0xFF and pin == 0:
        print("Циклическая перестановка => полином транзитивен")
    else:
        print("Не циклическая перестановка => полином не транзитивен")

def egcd(a, b):
    #алгоритм Евклида
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def inv_mod(a, p):
    #находит обратный элемент a^-1 mod p
    a %= p
    g, x, _ = egcd(a, p)
    if g != 1:
        raise ValueError("Обратного по модулю не существует: gcd(a,p) ≠ 1")
    return x % p

def decompose_via_lemma(r, s, p=2, max_steps=200):
    #разложение p-адической дроби
    if s <= 0:
        raise ValueError("s должно быть ≥ 1")
    if p < 2:
        raise ValueError("p должно быть ≥ 2")
    if s % p == 0:
        raise ValueError("gcd(p,s) ≠ 1: знаменатель кратен p")
    inv_s = inv_mod(s, p)
    mem_r = []
    mem_A = []
    cur = r
    steps = 0
    while cur not in mem_r and steps < max_steps:
        A = (cur * inv_s) % p              
        R = (cur - A * s) // p       
        print(f"{cur}/{s} = {A} + {p}*({R}/{s})")
        mem_r.append(cur)
        mem_A.append(A)
        cur = R
        steps += 1
    if cur in mem_r:
        sep = mem_r.index(cur)
        prefix = mem_A[:sep]
        period  = mem_A[sep:]
        rep = "Результат: (" + "".join(str(d) for d in period[::-1]) + ")" + "".join(str(d) for d in prefix[::-1])
        print(rep)
    else:
        print("Достигнут лимит шагов без обнаружения периода")
    return

def main():
    f_f_mod4 = [pmod(18, 2), pmod(1, 2), pmod(-7, 2)]   # mod 4
    f_f_mod8 = [pmod(18, 3), pmod(1, 3), pmod(-7, 3)]   # mod 8
    print("_"*30)
    print("     f(x) = 18 + 1x - 7x^2")
    print("_"*30)
    check_z4_and_z8("f", f_f_mod4, f_f_mod8)

    print()

    g_a0_mod4 = pmod_fraction(-1, 15, 2)      # -1/15 mod 4
    g_a1_mod4 = pmod_fraction(17, 19, 2)     # 17/19 mod 4
    g_a2_mod4 = 0
    g_a0_mod8 = pmod_fraction(-1, 15, 3)      # -1/15 mod 8
    g_a1_mod8 = pmod_fraction(17, 19, 3)     # 17/19 mod 8
    g_a2_mod8 = 0

    g_g_mod4 = [g_a0_mod4, g_a1_mod4, g_a2_mod4]
    g_g_mod8 = [g_a0_mod8, g_a1_mod8, g_a2_mod8]
    print("_"*30)
    print("     g(x) = (17/19)x - (1/15)")
    print("_"*30)
    check_z4_and_z8("g", g_g_mod4, g_g_mod8)

    print()
    print("_"*30)
    print("Разложение дробей по лемме (p=2)")
    print("_"*30)
    print("a₀: 17/19")
    decompose_via_lemma(17, 19, p=2)
    print("\na₀: -1/15")
    decompose_via_lemma(-1, 15, p=2)

if __name__ == "__main__":
    main()
