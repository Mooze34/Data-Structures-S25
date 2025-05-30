# MXA 220164 
# Mustafa Alawad 
# CS 3345 Project 2 


# Merge two sorted lists into one sorted list.
# Parameters: left (sorted list), right (sorted list).
# Returns: merged sorted list.
def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# Perform iterative (bottom-up) merge sort.
# Parameter: arr (list of elements to sort).
# Returns: new sorted list.
def merge_sort_iterative(arr):
    n = len(arr)
    if n <= 1:
        return arr[:]
    
    width = 1
    result = arr[:]
    
    while width < n:
        for i in range(0, n, 2 * width):
            left = result[i : i + width]
            right = result[i + width : i + 2 * width]
            merged = merge(left, right)
            result[i : i + len(merged)] = merged
        width *= 2
    return result

# Sort the subarray a[low...high] in place using insertion sort.
def insertion_sort(a, low, high):
    for i in range(low + 1, high + 1):
        key = a[i]
        j = i - 1
        while j >= low and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

# Partition the subarray using the median-of-three method.
# Chooses pivot as the median of the first, middle, and last elements.
# Returns the final pivot index after partitioning.
def partition_median_of_three(a, low, high):
    mid = (low + high) // 2
    if a[mid] < a[low]:
        a[low], a[mid] = a[mid], a[low]
    if a[high] < a[low]:
        a[low], a[high] = a[high], a[low]
    if a[high] < a[mid]:
        a[mid], a[high] = a[high], a[mid]
    
    pivot = a[mid]
    a[mid], a[high] = a[high], a[mid]
    i = low
    for j in range(low, high):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[high] = a[high], a[i]
    return i

# Quicksort that uses median-of-three partitioning and a cutoff of 15 for small subarrays.
# Sorts the list 'a' in place.
def quick_sort_alternative(a):
    # Recursive helper function for quicksort.
    def _quick_sort(a, low, high):
        if low >= high:
            return
        # Use insertion sort for subarrays of size 15 or less.
        if high - low + 1 <= 15:
            insertion_sort(a, low, high)
            return
        
        pivot_index = partition_median_of_three(a, low, high)
        _quick_sort(a, low, pivot_index - 1)
        _quick_sort(a, pivot_index + 1, high)
    
    _quick_sort(a, 0, len(a) - 1)

# Main block to test both sorting methods.
if __name__ == "__main__":
    import random
    # Generate a sample list of 25 random integers between 1 and 100.
    sample = [random.randint(1, 100) for _ in range(25)]
    print("Original list:")
    print(sample)
    
    # Use iterative merge sort, which returns a new sorted list.
    print("Sorted with merge_sort_iterative:")
    print(merge_sort_iterative(sample))
    
    # Use quicksort which sorts the list in place.
    sample_qs = sample.copy()
    quick_sort_alternative(sample_qs)
    print("Sorted with quick_sort_alternative:")
    print(sample_qs)