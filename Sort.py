from GameList import games_data

def merge_sort(arr, key=lambda x: x):
    """Sorts arr from A to Z based on the key function."""
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
    """Sorts arr from Z to A based on the key function."""
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if key(x) >= key(pivot)]
        greater = [x for x in arr[1:] if key(x) < key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

def selection_sort(arr, key=lambda x: x):
    """Sorts arr from high to low based on the key function."""
    for i in range(len(arr)):
        max_idx = i
        for j in range(i+1, len(arr)):
            if key(arr[j]) > key(arr[max_idx]):
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

def bubble_sort(arr, key=lambda x: x):
    """Sorts arr from low to high based on the key function."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(arr[j]) > key(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr, key=lambda x: x):
    """Sorts arr from high to low based on the key function."""
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) < key(key_item):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

def heapify(arr, n, i, key=lambda x: x):
    """Help function to maintain the heap property."""
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
    """Sorts arr from low to high based on the key function."""
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, key)

    return arr

def sort_games(criteria):
    """
    Sorts the games based on the specified criteria.
    - 'title_az': Alphabetically A-Z (merge_sort)
    - 'title_za': Alphabetically Z-A (quick_sort)
    - 'price_high_low': Price High to Low (selection_sort)
    - 'price_low_high': Price Low to High (bubble_sort)
    - 'review_high_low': Review Score High to Low (insertion_sort)
    - 'review_low_high': Review Score Low to High (heap_sort)
    """
    if criteria == 'title_az':
        return merge_sort(games_data, key=lambda x: x['title'])
    elif criteria == 'title_za':
        return quick_sort(games_data, key=lambda x: x['title'])
    elif criteria == 'price_high_low':
        return selection_sort(games_data, key=lambda x: x['price'])
    elif criteria == 'price_low_high':
        return bubble_sort(games_data, key=lambda x: x['price'])
    elif criteria == 'review_high_low':
        return insertion_sort(games_data, key=lambda x: x['review'])
    elif criteria == 'review_low_high':
        sorted_games = heap_sort(games_data, key=lambda x: x['review'])
        return sorted_games[::-1]
    else:
        raise ValueError("Invalid sorting criteria")

# Assuming the sorting functions are already defined above this section...

def sort_and_print_games(sorted_games):
    """Utility function to print sorted games with all their details."""
    for game in sorted_games:
        print(f"{game['title']} - ${game['price']} - Rating: {game['review']} - Genre: {game['genre']} - ESRB: {game['esrb_rating']}")

def test_sorting(criteria):
    """Test sorting based on different criteria."""
    print(f"\nSorting games by {criteria.replace('_', ' ').upper()}:\n")
    sorted_games = sort_games(criteria)
    sort_and_print_games(sorted_games)

if __name__ == "__main__":
    # Test cases for each sorting criterion
    criteria_list = [
        'title_az', 'title_za', 'price_high_low', 'price_low_high', 'review_high_low', 'review_low_high'
    ]
    for criteria in criteria_list:
        test_sorting(criteria)

