def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right)

def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if key(x) >= key(pivot)]
        greater = [x for x in arr[1:] if key(x) < key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

def selection_sort(arr, key=lambda x: x):
    for i in range(len(arr)):
        max_idx = i
        for j in range(i+1, len(arr)):
            if key(arr[j]) > key(arr[max_idx]):
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

def bubble_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(arr[j]) > key(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(key_item):  # Updated condition for Price Low to High
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr


def heapify(arr, n, i, key=lambda x: x):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and key(arr[left]) < key(arr[largest]):
        largest = left

    if right < n and key(arr[right]) < key(arr[largest]):
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key)

def heap_sort(arr, key=lambda x: x):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, key)

    return arr