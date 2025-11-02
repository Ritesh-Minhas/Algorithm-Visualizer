from typing import Generator, List, Optional, Tuple, Dict
Frame = Tuple[List[int], Optional[Tuple[int, ...]], bool, Dict]

def quick_sort(data: List[int]) -> Generator[Frame, None, None]:
    arr = data.copy()

    def _partition(lo: int, hi: int):
        pivot = arr[hi]
        meta = {"pivot": hi, "active_range": (lo, hi)}
        yield (arr.copy(), (hi,), False, meta)  # show pivot
        i = lo
        for j in range(lo, hi):
            meta = {"pivot": hi, "active_range": (lo, hi)}
            yield (arr.copy(), (j, hi), False, meta)  # compare with pivot
            if arr[j] <= pivot:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield (arr.copy(), (i, j), True, meta)
                i += 1
        if i != hi:
            arr[i], arr[hi] = arr[hi], arr[i]
            meta = {"pivot": i, "active_range": (lo, hi)}
            yield (arr.copy(), (i, hi), True, meta)
        return i

    def _qs(lo: int, hi: int):
        if lo < hi:
            p = yield from _partition(lo, hi)
            yield from _qs(lo, p - 1)
            yield from _qs(p + 1, hi)

    if len(arr) > 1:
        yield from _qs(0, len(arr) - 1)
    yield (arr.copy(), None, False, {})
