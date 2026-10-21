"""Choose an offered bank before assigning its successful operation.

Every option must have a compatible mathematical witness. Rejection therefore
occurs before the uniform key draw, never as a consequence of that draw.
"""
from functools import lru_cache
import itertools


def is_echelon(bits):
    previous = -1
    zero_seen = False
    for row in range(4):
        occupied = (bits >> (4 * row)) & 15
        if not occupied:
            zero_seen = True
        else:
            pivot = (occupied & -occupied).bit_length() - 1
            if zero_seen or pivot <= previous:
                return False
            previous = pivot
    return True


@lru_cache(maxsize=1)
def operation_support():
    # Enumerate terminal echelon patterns, then undo the offered erasures.
    # Subsets include already-zero and redundant coordinates without requiring
    # a globally minimum operation. This finite enumeration needs no assets.
    terminals = [m for m in range(1 << 16) if is_echelon(m)]
    result = {}
    for size in (2, 3):
        for cells in itertools.combinations(range(16), size):
            operation = sum(1 << c for c in cells)
            subsets = [sum(1 << c for c in sub)
                       for n in range(1, size + 1)
                       for sub in itertools.combinations(cells, n)]
            masks = {terminal | sub for terminal in terminals
                     if not terminal & operation for sub in subsets
                     if not is_echelon(terminal | sub)}
            if masks:
                result[cells] = frozenset(masks)
    return result


def compatible_masks(bank, bottom_zero):
    support = operation_support()
    witnesses = []
    for option in bank:
        candidates = support[option].difference(
            *(support[other] for other in bank if other != option))
        candidates = [m for m in candidates if (m >> 12 == 0) == bottom_zero]
        erased = sum(1 << c for c in option)
        candidates = [m for m in candidates
                      if sum(bool((m >> (4*i)) & 15) for i in range(4)) >= 3
                      and sum(bool(((m & ~erased) >> (4*i)) & 15)
                              for i in range(4)) >= 2]
        # No-op counting must leave a competitor; the echelon conditions
        # decide which offered replacement actually works.
        candidates = [m for m in candidates if sum(
            sum(not m & (1 << c) for c in other)
            <= sum(not m & (1 << c) for c in option)
            for other in bank) >= 2]
        if not candidates:
            return None
        witnesses.append(sorted(candidates))
    return witnesses


def sample(rng):
    size = rng.choice((2, 3))
    bottom_zero = rng.choice((False, True))
    pool = [o for o, masks in operation_support().items() if len(o) == size
            and any((m >> 12 == 0) == bottom_zero for m in masks)]
    # This bound is a programming guard, not a key-dependent resampling rule.
    for _ in range(10000):
        bank = rng.sample(pool, 5)
        witnesses = compatible_masks(bank, bottom_zero)
        if witnesses is not None:
            break
    else:
        raise RuntimeError('No fully supported offered bank found')
    selected = rng.randrange(5)
    mask = rng.choice(witnesses[selected])
    matrix = [[rng.choice(tuple(range(-9, 0)) + tuple(range(1, 10)))
               if mask & (1 << (4*i+j)) else 0 for j in range(4)]
              for i in range(4)]
    bank = [[[c // 4, c % 4] for c in option] for option in bank]
    rng.shuffle(bank)
    return {'matrix': matrix, 'bank': bank}
