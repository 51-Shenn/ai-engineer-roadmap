import math

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    modulus_a = math.sqrt(sum(x * x for x in a))
    modulus_b = math.sqrt(sum(x * x for x in b))
    if modulus_a == 0 or modulus_b == 0:
        return 0.0

    return dot / (modulus_a * modulus_b)

assert cosine_similarity([1,2,3], [1,2,3]) == 1.0
assert cosine_similarity([1,2,3], [2,4,6]) == 1.0
assert cosine_similarity([1,2,3], [-1,-2,-3]) == -1.0
assert cosine_similarity([1,0], [0,1]) == 0.0
assert cosine_similarity([0,0,0], [1,2,3]) == 0.0

print("All tests passed!")
