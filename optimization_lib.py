import random
import time
from itertools import product


def naive(lists, m, f):
    # Naive implementation of the solution is of complexity
    # $O(N_1 * N_2 \cdots N_k)$; or, $O(L)$, with $L = L_{n,k}$ the number of
    # combinations.
    return max(sum(f(elem) for elem in combo) % m for combo in product(*lists))


def efficient(lists, m, f):
    # Consider this one idea: loop through m residue classes (m - 1 through 0)
    # and for each of them check if there is a combo which gives that residue
    # class. The first time a residue class is accessible, that is the max that
    # we were looking for.
    #
    # This efficient algorithm appears to be of complexity $O(L ^ 0.24)$ where
    # $L$ is the number of combinations.
    for res_cls in range(m - 1, -1, -1):
        for combo in product(*lists):
            if sum(f(elem) for elem in combo) % m == res_cls:
                return res_cls


def benchmark_stats(num_lists, num_elements, m, f, replications, impl=naive):
    # With num_lists $k = 8$, num_elements $N_1 = 10$, and the number of
    # combinations about 1.5e06, my efficient algorithm is 50 000 times faster
    # than the naive algorithm.
    if impl not in [naive, efficient]:
        raise NotImplementedError

    rand_lists = [random.sample(range(1, 10**9 + 1), num_elements)] + [
        random.sample(range(1, 10**9 + 1), random.randint(1, 10)) for _ in range(num_lists - 1)
    ]

    times = []
    for _ in range(replications):
        start = time.perf_counter()
        _ = impl(rand_lists, m, f)
        times.append(time.perf_counter() - start)

    return {
        "max_elapsed": max(times),
        "avg_elapsed": sum(times) / replications,
        "min_elapsed": min(times),
    }
