from typing import Generator, List, Optional, Tuple, Dict
Frame = Tuple[List[int], Optional[Tuple[int, ...]], bool, Dict]

def bubble_sort(data: List[int]) -> Generator[Frame, None, None]:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            meta = {"sorted_tail_len": i}
            yield (arr.copy(), (j, j + 1), False, meta)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                meta = {"sorted_tail_len": i}
                yield (arr.copy(), (j, j + 1), True, meta)
    yield (arr.copy(), None, False, {"sorted_tail_len": n})
