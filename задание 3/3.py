def pmod(a, k):
    modulus = 1 << k
    return (a % modulus + modulus) % modulus

def h(x):
    return (x ^ 1) ^ (2 * (x & (1 + 2 * x) 
                         & (3 + 4 * x) & (7 + 8 * x) & (15 + 16 * x) 
                         & (31 + 32 * x) & (63 + 64 * x))) \
                   ^ (4 * (x * x + 19))

mod256 = [0] * 256
flags = [0] * 256
pin = 0

for i in range(256):
    mod256[i] = pmod(h(i), 8)

cycle_output = "0"
for i in range(256):
    pin = mod256[pin]
    flags[pin] = 1
    cycle_output += f" -> {pin}"

for i in range(10, 256):
    pin = mod256[pin]
    flags[pin] = 1

total_visited = sum(flags)

print(cycle_output + " -> ...")
print()
print(f"Всего посещено элементов: {total_visited} из 256")
print()

if total_visited == 256:
    print("Функция h(x) транзитивна по модулю 256")
else:
    print("Функция h(x) не транзитивна")

