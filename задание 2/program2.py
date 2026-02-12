def inverse_mod_2k(a, k):
    """Находит обратный элемент для нечётного a по модулю 2^k"""
    # Для нечётного a обратный элемент по модулю 2^k существует
    # Используем метод Ньютона для 2-адических чисел
    if a % 2 == 0:
        raise ValueError("Число должно быть нечётным для существования обратного по модулю 2^k")
    
    if k == 0:
        return 1
    
    # Начинаем с приближения для модуля 2^1
    inv = 1
    
    # Итеративно уточняем для 2^k
    for i in range(1, k):
        inv = inv * (2 - a * inv) % (2 << i)
    
    return inv % (1 << k)

def compute_2adic_fraction(num, den, mod):
    """Вычисляет значение дроби num/den в 2-адических числах по модулю mod=2^k"""
    # den должен быть нечётным для существования обратного в 2-адических числах
    if den % 2 == 0:
        raise ValueError("Знаменатель должен быть нечётным в 2-адических числах")
    
    k = mod.bit_length() - 1  # mod = 2^k
    
    # Находим обратный к знаменателю по модулю 2^k
    inv_den = inverse_mod_2k(den % mod, k)
    
    # Вычисляем дробь как num * inv_den mod mod
    return (num % mod) * inv_den % mod

def check_bijective_transitive(poly_type='f'):
    """
    Проверяет полином на биективность и транзитивность на ℤ₂
    """
    print(f"\nПроверка полинома {poly_type}(x):")
    
    # 1. Проверка биективности по модулю 4 (Теорема Ларина)
    print("1. Проверка биективности по модулю 4:")
    values_mod4 = {}
    
    for x in range(4):
        # Вычисляем значение полинома по модулю 4
        if poly_type == 'f':
            # f(x) = 18 + x - 7x²
            value = (18 + x - 7*x*x) % 4
        else:
            # g(x) = (17/19)x - 1/15
            # Используем 2-адическое представление
            term1 = compute_2adic_fraction(17 * x, 19, 4)
            term2 = compute_2adic_fraction(-1, 15, 4)
            value = (term1 + term2) % 4
        
        values_mod4[x] = value
        print(f"  {poly_type}({x}) mod 4 = {value}")
    
    # Проверяем, является ли перестановкой по модулю 4
    unique_values = set(values_mod4.values())
    is_bijective_mod4 = len(unique_values) == 4
    
    if is_bijective_mod4:
        print("  Полином является перестановкой по модулю 4 (биективен)")
    else:
        print(f"  Полином НЕ является перестановкой по модулю 4")
    
    # 2. Проверка транзитивности по модулю 8 (для биективных полиномов)
    if is_bijective_mod4:
        print("\n2. Проверка транзитивности по модулю 8:")
        values_mod8 = {}
        
        for x in range(8):
            # Вычисляем значение полинома по модулю 8
            if poly_type == 'f':
                # f(x) = 18 + x - 7x²
                value = (18 + x - 7*x*x) % 8
            else:
                # g(x) = (17/19)x - 1/15
                term1 = compute_2adic_fraction(17 * x, 19, 8)
                term2 = compute_2adic_fraction(-1, 15, 8)
                value = (term1 + term2) % 8
            
            values_mod8[x] = value
            print(f"  {poly_type}({x}) mod 8 = {value}")
        
        # Проверяем, является ли перестановкой одним циклом
        visited = [False] * 8
        cycles = []
        
        for start in range(8):
            if not visited[start]:
                cycle = []
                current = start
                
                while not visited[current]:
                    visited[current] = True
                    cycle.append(current)
                    current = values_mod8[current]
                
                if len(cycle) > 1 or (len(cycle) == 1 and values_mod8[cycle[0]] == cycle[0]):
                    cycles.append(cycle)
        
        print(f"  Найдено циклов: {len(cycles)}")
        
        if len(cycles) == 1 and len(cycles[0]) == 8:
            is_transitive = True
            print("  Полином транзитивен (один цикл длины 8)")
        else:
            is_transitive = False
            print("  Полимум НЕ транзитивен")
            for i, cycle in enumerate(cycles):
                print(f"    Цикл {i+1}: {cycle}")
    else:
        is_transitive = False
        print("\n2. Пропуск проверки транзитивности (полином не биективен)")
    
    # 3. Вывод результатов для ℤ₂
    print("\n3. Результаты для ℤ₂:")
    if not is_bijective_mod4:
        print("  Полином НЕ биективен на ℤ₂")
        print("  Полимум НЕ транзитивен на ℤ₂")
    else:
        print("  Полином биективен на ℤ₂")
        if is_transitive:
            print("  Полимум транзитивен на ℤ₂")
        else:
            print("  Полимум НЕ транзитивен на ℤ₂")
    
    return is_bijective_mod4, is_transitive if is_bijective_mod4 else False

def main():
    """Основная функция"""
    print("ПРОВЕРКА БИЕКТИВНОСТИ И ТРАНЗИТИВНОСТИ ПОЛИНОМОВ НА ℤ₂")
    
    # Анализ f(x) = 18 + x - 7x²
    print("\nАНАЛИЗ f(x) = 18 + x - 7x²")
    f_bijective, f_transitive = check_bijective_transitive('f')
    
    # Анализ g(x) = (17/19)x - 1/15
    print("\nАНАЛИЗ g(x) = (17/19)x - 1/15")
    g_bijective, g_transitive = check_bijective_transitive('g')
    
    print("\nИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("1. f(x) = 18 + x - 7x²:")
    if not f_bijective:
        print("   - НЕ биективна на ℤ₂")
        print("   - НЕ транзитивна на ℤ₂")
    else:
        print("   - Биективна на ℤ₂")
        if f_transitive:
            print("   - Транзитивна на ℤ₂")
        else:
            print("   - НЕ транзитивна на ℤ₂")
    
    print("\n2. g(x) = (17/19)x - 1/15:")
    if not g_bijective:
        print("   - НЕ биективна на ℤ₂")
        print("   - НЕ транзитивна на ℤ₂")
    else:
        print("   - Биективна на ℤ₂")
        if g_transitive:
            print("   - Транзитивна на ℤ₂")
        else:
            print("   - НЕ транзитивна на ℤ₂")

if __name__ == "__main__":
    main()