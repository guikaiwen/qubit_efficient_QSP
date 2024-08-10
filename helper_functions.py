import numpy as np
import random

import time
import timeit


def round_to_three_significant_digits(numbers_vec: list, digit: int) -> np.ndarray:
    """
    Function to round the input vector of floating numbers to the targeted number of digits
    
    @param numbers_vec: vector of floating numbers to be rounded each
    @param digit: targetting number of digits to round to
    
    @return rounded_numbers_vec: rounded vector of floating numbers
    """
    rounded_numbers_vec = []
    for num in numbers_vec:
        if num == 0:
            rounded_numbers_vec.append(0)
        else:
            rounded_numbers_vec.append(np.round(num, digit))
    return np.array(rounded_numbers_vec)


def row_to_column_vector(row_vector: np.ndarray) -> np.ndarray:
    """
    Function to converts a 1D row vector to a 1D column vector
    
    @param row_vector: input row vector
    
    @return the converted column vector
    """
    if not isinstance(row_vector, np.ndarray) or row_vector.ndim != 1:
        raise ValueError("Input must be a 1D NumPy array (row vector).")

    return row_vector.reshape(-1, 1)


def nicer_array_display(input_vec: np.ndarray, digit: int) -> np.ndarray:
    """
    Function to combine the effect of both digit trimming and row to column conversion
    
    @param input_vec: input row vector to process
    @param digit: targetting number of digits to round to
    
    @return the processed column vector
    """
    return row_to_column_vector(round_to_three_significant_digits(input_vec, digit))


def generate_normalized_real_array(n: int) -> np.ndarray:
    """
    Function to generate a normalized random real value vector
    
    @param n: total number of data qubit
    
    @return normalized_v: an array of size 2^n that holds the generated nomalized real vector
    """
    vec = []
    for i in range(2 ** n):
        vec.append(random.random())
    normalized_real_array = np.array(vec) / np.sqrt(np.sum(np.array(vec)**2)) # need to normalize the vector
    return normalized_real_array


def generate_normalized_complex_array(n: int) -> np.ndarray:
    """
    Function to generate a normalized random complex value vector
    
    @param n: total number of data qubit
    
    @return normalized_v: an array of size 2^n that holds the generated nomalized complex vector
    """
    array_length = 2 ** n
    # Generate a complex array with random complex values that may contain negatives
    complex_array = (np.random.rand(array_length) - 0.5) + 1j * (np.random.rand(array_length) - 0.5)

    # Normalize the complex array
    normalized_complex_array = complex_array / np.linalg.norm(complex_array)

    return normalized_complex_array


def generate_normalized_real_sparse_array(n: int, none_zero_index_array: np.ndarray) -> np.ndarray:
    """
    Function to generate a normalized random real value vector
    
    @param n: total number of data qubit
    @param none_zero_index_array: a 1d array that stores the index of the non zero elements. E.g., a quantum state of |a> = 0.6|00> + 0.8|11> would have the array as [0, 3]
    
    @return normalized_v: an array of size 2^n that holds the generated nomalized real vector
    """
    vec = [0] * (2 ** n)
    for i in range(len(none_zero_index_array)):
        vec[none_zero_index_array[i]] = random.random()
    normalized_real_array = np.array(vec) / np.sqrt(np.sum(np.array(vec)**2)) # need to normalize the vector
    return normalized_real_array


def binary_to_decimal(binary: str) -> int:
    """
    Function to convert a binary number into a decimal number
    
    @param binary: a string that represents the binary number
    
    @return decimal: an int that represents the decimal number
    """
    decimal = 0
    power = 0
    for digit in reversed(binary):
        decimal += int(digit) * (2 ** power)
        power += 1
    return decimal


def measure_time(obj, method_name, *args, **kwargs):
    # Get the method from the object
    method = getattr(obj, method_name)

    # Measure CPU start time
    start_cpu_time = time.process_time()

    # Call the method
    method(*args, **kwargs)

    # Measure CPU end time
    end_cpu_time = time.process_time()

    cpu_time = end_cpu_time - start_cpu_time

    return cpu_time