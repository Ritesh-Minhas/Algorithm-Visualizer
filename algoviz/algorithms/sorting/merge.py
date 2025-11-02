from typing import Generator, List, Optional, Tuple, Dict
Frame = Tuple[List[int], Optional[Tuple[int, ...]], bool, Dict]

def merge_sort(data: List[int]) -> Generator[Frame, None, None]:
    arr = data.copy()
    aux = arr.copy()

    def _merge(lo: int, mid: int, hi: int):
        aux[lo:hi+1] = arr[lo:hi+1]
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            meta = {"active_range": (lo, hi)}
            if i <= mid and j <= hi:
                yield (arr.copy(), (i, j), False, meta)
            if i > mid:
                arr[k] = aux[j]; j += 1
                yield (arr.copy(), (k,), True, meta)
            elif j > hi:
                arr[k] = aux[i]; i += 1
                yield (arr.copy(), (k,), True, meta)
            elif aux[j] < aux[i]:
                arr[k] = aux[j]; j += 1
                yield (arr.copy(), (k,), True, meta)
            else:
                arr[k] = aux[i]; i += 1
                yield (arr.copy(), (k,), True, meta)

    def _sort(lo: int, hi: int):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        yield from _sort(lo, mid)
        yield from _sort(mid + 1, hi)
        yield from _merge(lo, mid, hi)

    if len(arr) > 1:
        yield from _sort(0, len(arr) - 1)
    yield (arr.copy(), None, False, {})
