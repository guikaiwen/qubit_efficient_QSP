import braket
from braket.circuits import Circuit
from braket.aws import AwsDevice
from braket.devices import LocalSimulator

import numpy as np
import random


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
    """Converts a 1D row vector to a 1D column vector."""
    if not isinstance(row_vector, np.ndarray) or row_vector.ndim != 1:
        raise ValueError("Input must be a 1D NumPy array (row vector).")

    return row_vector.reshape(-1, 1)


def generate_normalized_random_feature_vec(n: int) -> np.ndarray:
    """
    Function to generate a normalized random feature value vector
    
    @param n: total number of data qubit
    
    @return normalized_v: an array of size 2^n that holds the generated nomalized feature values
    """
    vec = []
    for i in range(2 ** n):
        vec.append(random.random())
    normalized_v = np.array(vec) / np.sqrt(np.sum(np.array(vec)**2)) # need to normalize the vector
    return normalized_v


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