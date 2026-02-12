#Проверка биективности и транзитивности f и g на Z2
def f(x):
    return (18 + x - 7 * x**2) % (2**n)
def g(x):
    return (17 * pow(19, -1, 2**n) * x - pow(15, -1, 2**n)) % (2**n)
n = 4  # степень двойки для проверки биективности
# Проверка биективности
def is_bijective(func):
    seen = set()
    for x in range(2**n):
        y = func(x)
        if y in seen:
            return False
        seen.add(y)
    return True
# Проверка транзитивности
def is_transitive(func):
    visited = [False] * (2**n)
    count = 0
    x = 0
    while not visited[x]:
        visited[x] = True
        x = func(x)
        count += 1
    return count == 2**n
# Проверка функции f
print("Function f:")
print("Bijective:", is_bijective(f))
print("Transitive:", is_transitive(f))
# Проверка функции g
print("Function g:")
print("Bijective:", is_bijective(g))
print("Transitive:", is_transitive(g))