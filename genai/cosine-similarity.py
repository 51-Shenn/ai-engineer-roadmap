import math

def cosine_similarity(x: list[float], y: list[float]):
    dot_product = sum(x * y for x, y in zip(x, y))
    magnitude_a = math.sqrt(sum(math.pow(x, 2) for x in x))
    magnitude_b = math.sqrt(sum(math.pow(y, 2) for y in y))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

assert cosine_similarity([1,2,3], [1,2,3]) == 1.0
assert cosine_similarity([1,2,3], [2,4,6]) == 1.0
assert cosine_similarity([1,2,3], [-1,-2,-3]) == -1.0
assert cosine_similarity([1,0], [0,1]) == 0.0
assert cosine_similarity([0,0,0], [1,2,3]) == 0.0

print("All tests passed!")
