import time
import timeit

def measure_time(func, *args, **kwargs):

    start_wall_time = timeit.default_timer()
    start_cpu_time = time.process_time()

    result = func(*args, **kwargs)

    end_cpu_time = time.process_time()
    end_wall_time = timeit.default_timer()

    cpu_time = end_cpu_time - start_cpu_time
    wall_time = end_wall_time - start_wall_time

    return result, cpu_time, wall_time

# Example function to test the time measurement
def example_function(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    n = 100000
    result, cpu_time, wall_time = measure_time(example_function, n)
    print(f"Result: {result}")
    print(f"CPU Time: {cpu_time:.6f} seconds")
    print(f"Wall Time: {wall_time:.6f} seconds")