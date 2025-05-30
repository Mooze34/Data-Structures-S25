# MXA 220164 
# Mustafa Alawad 
# CS 3345 Project 2 



import time
import random
import statistics
from sorting_algos import merge_sort_iterative, quick_sort_alternative

def generate_random_array(n):
    # Generate an array of n random integers between 0 and n.
    return [random.randint(0, n) for _ in range(n)]

def generate_almost_sorted_array(n, swap_fraction=0.05):
    
    # Generate an "almost sorted" array by starting with a sorted array and randomly swapping
    # a small fraction of its elements.
    
    arr = list(range(n))
    num_swaps = max(1, int(n * swap_fraction))
    for _ in range(num_swaps):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def benchmark_sort(sort_func, array, iterations=5, in_place=False):
    
    # Benchmark a sorting function by averaging the execution time over multiple iterations.
    
    
    times = []
    for _ in range(iterations):
        # Always work on a fresh copy of the array.
        arr_copy = array.copy()
        start = time.perf_counter()
        if in_place:
            sort_func(arr_copy)
            # Verify correctness.
            assert arr_copy == sorted(array)
        else:
            result = sort_func(arr_copy)
            # Verify correctness.
            assert result == sorted(array)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)

def run_benchmarks():
    sizes = [1000, 5000, 10000]  # Array sizes to benchmark.
    iterations = 5              # Number of iterations per test case.

    for n in sizes:
        print(f"\nBenchmarking for array size n = {n}")
        
        # Generate test arrays: one random and one almost sorted.
        random_array = generate_random_array(n)
        almost_sorted_array = generate_almost_sorted_array(n, swap_fraction=0.05)
        
        for array_type, test_array in [("Random", random_array), ("Almost Sorted", almost_sorted_array)]:
            # Benchmark merge_sort_iterative (non in-place sort)
            merge_time = benchmark_sort(merge_sort_iterative, test_array, iterations=iterations, in_place=False)
            # Benchmark quick_sort_alternative (in-place sort)
            quick_time = benchmark_sort(quick_sort_alternative, test_array, iterations=iterations, in_place=True)
            
            print(f"{array_type} arrays: MergeSort average time = {merge_time:.6f}s, QuickSort average time = {quick_time:.6f}s")
            
            # Determine which sorting algorithm is faster.
            if merge_time < quick_time:
                diff = quick_time - merge_time
                print(f"--> MergeSort is faster by {diff:.6f}s for {array_type} arrays of size {n}.")
            elif quick_time < merge_time:
                diff = merge_time - quick_time
                print(f"--> QuickSort is faster by {diff:.6f}s for {array_type} arrays of size {n}.")
            else:
                print(f"--> Both algorithms perform similarly for {array_type} arrays of size {n}.")

if __name__ == "__main__":
    run_benchmarks()