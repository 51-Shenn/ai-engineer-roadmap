lst = [1, 2, 3]

for e in lst:
    print(e)

squares = [x**2 for x in range (10)]
print(squares)

for n, i in enumerate(squares):
    if squares[n] <= 10:
        print(f'index: {n}, value: {i}')

powers = [(x, x**2, x**3) for x in range (10)]
print(powers)

for n, (i, j, k) in enumerate(powers):
    print(f'index: {n}, value 1: {i}, value 2: {j}, value 3: {k}')

x = len(squares) - 1
while x >= -1:
    if (x < 0):
        print("\n")
        break
    print(squares[x], end='.')
    x -= 1
