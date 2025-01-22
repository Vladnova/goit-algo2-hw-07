import random
import time


# Функція для обчислення суми елементів без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

# Функція для оновлення елемента без кешу
def update_no_cache(array, index, value):
    array[index] = value

# LRU-кеш для зберігання результатів запитів типу Range
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.order = []
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)

    def invalidate(self):
        self.cache.clear()
        self.order.clear()

# Функція для обчислення суми елементів з кешем
def range_sum_with_cache(cache, array, L, R):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

# Функція для оновлення елемента з кешем
def update_with_cache(cache, array, index, value):
    array[index] = value
    cache.invalidate()

# Генерація тестових даних
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
queries = [("Range", random.randint(0, N-1), random.randint(0, N-1)) if random.random() < 0.7 else ("Update", random.randint(0, N-1), random.randint(1, 1000)) for _ in range(Q)]

# Виконання запитів без кешу
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        L, R = sorted((query[1], query[2]))
        range_sum_no_cache(array, L, R)
    elif query[0] == "Update":
        update_no_cache(array, query[1], query[2])
no_cache_time = time.time() - start_time

# Виконання запитів з кешем
cache = LRUCache(capacity=1000)
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        L, R = sorted((query[1], query[2]))
        range_sum_with_cache(cache, array, L, R)
    elif query[0] == "Update":
        update_with_cache(cache, array, query[1], query[2])
cache_time = time.time() - start_time

# Результати
print(f"\nЧас виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")
