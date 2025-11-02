from typing import Generator, List, Optional, Tuple, Dict
Frame = Tuple[List[int], Optional[Tuple[int, ...]], bool, Dict]

def insertion_sort(data: List[int]) -> Generator[Frame, None, None]:
    arr = data.copy()
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        yield (arr.copy(), (j, i), False, {"sorted_prefix_len": i})
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            yield (arr.copy(), (j, j + 1), True, {"sorted_prefix_len": i})
            j -= 1
        arr[j + 1] = key
        yield (arr.copy(), (j + 1,), True, {"sorted_prefix_len": i + 1})
    yield (arr.copy(), None, False, {"sorted_prefix_len": n})
