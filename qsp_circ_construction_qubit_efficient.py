# Import Braket libraries
import braket
from braket.circuits import Circuit
from braket.aws import AwsDevice
from braket.devices import LocalSimulator

import numpy as np
import math


def compute_rz_rotation_angle(s: int, j: int, phase_array: np.ndarray) -> float:
    """
    Function to compute a particular \alpha_{s,j} angle according to the equation in
    https://github.com/guikaiwen/qubit_efficient_QSP/blob/main/QSP_detailed_implementation.ipynb
    
    (Note that this implementation uses Numpy's vectorization for better classical paralellization. 
    Mathematically it is equivalent to the implementation in qsp_detailed_implementation.ipynb)
    
    @param s: as it appear in equation 4.30 in the ML with QC book
    @param j: as it appear in equation 4.30 in the ML with QC book
    @param phase_array: the entire wave function array vector phase values to be encoded
    
    @return: a float/double value that holds the computed phase angle
    """
    # Indices for the sum calculation
    indices_top = (2 * j - 1) * 2 ** (s - 1) + np.arange(2 ** (s - 1))
    indices_bottom = (2 * j - 2) * 2 ** (s - 1) + np.arange(2 ** (s - 1))

    # Compute the sum of phase differences
    sum_top = np.sum(phase_array[indices_top] - phase_array[indices_bottom])

    return sum_top / (2 ** (s - 1))


def compute_ry_rotation_angle(s: int, j: int, amplitude_array: np.ndarray) -> float:
    """
    Function to compute a particular \beta_{s,j} angle according to the equation in
    https://github.com/guikaiwen/qubit_efficient_QSP/blob/main/QSP_detailed_implementation.ipynb
    
    (Note that this implementation uses Numpy's vectorization for better classical paralellization. 
    Mathematically it is equivalent to the implementation in qsp_detailed_implementation.ipynb)
    
    @param s: as it appear in equation 4.30 in the ML with QC book
    @param j: as it appear in equation 4.30 in the ML with QC book
    @param amplitude_array: the entire wave function array vector amplitude values to be encoded
    
    @return: a float/double value that holds the computed angle 
    """
    # Indices for sum_top computation
    top_indices = (2 * j - 1) * 2 ** (s - 1) + np.arange(2 ** (s - 1))
    sum_top = np.sum(amplitude_array[top_indices] ** 2)

    # Indices for sum_bottom computation
    bottom_indices = (j - 1) * 2 ** s + np.arange(2 ** s)
    sum_bottom = np.sum(amplitude_array[bottom_indices] ** 2)

    # Handling the edge case where denominator is zero
    if np.isclose(sum_bottom, 0.0):
        return 0.0

    return 2 * np.arcsin(np.sqrt(sum_top / sum_bottom))
    
    
def x_gate_sequence(s: int, j: int, n: int, circ: braket.circuits.circuit.Circuit):
    """
    Function to add x gates to help emulate the anti-control operations
    
    @param s: as it appear in the equation above
    @param j: as it appear in the equation above
    @param n: total number of qubits for the state being prepared
    @param circ: quantum circuit to operate on
    """
    binary_j = bin(j - 1).replace("0b", "").zfill(n - s) # get the binary representation of the current j
    for i in range(n - s):
        if int(binary_j[i]) == 0:
            circ.x(i)
            
            
def full_multi_control_rotation_gate(s: int, j: int, n: int, circ: braket.circuits.circuit.Circuit, amplitude_array: np.ndarray, phase_array: np.ndarray, tolerance=1e-100):
    """
    Function to perform a full multi-control rotation gate based on the s and j values, will anti-control conditions included

    @param s: as it appear in equation 4.30 in the ML with QC book
    @param j: as it appear in equation 4.30 in the ML with QC book
    @param n: total number of qubits for the state being prepared
    @param circ: quantum circuit to operate on
    @param amplitude_array: the amplitude value vector for wave function array vector
    @param phase_array: the phase value vector for wave function array vector
    @param tolerance: a float number to determine if a number is close enough to zero in order to be treated as zero
    """
    ry_rotation_angle = compute_ry_rotation_angle(s, j, amplitude_array)
    rz_rotation_angle = compute_rz_rotation_angle(s, j, phase_array)
    target_bit_index = n - s
    control_qubit_list = list(range(target_bit_index)) # get the control qubit list
    
    if np.abs(ry_rotation_angle) > tolerance or np.abs(rz_rotation_angle) > tolerance:
        x_gate_sequence(s, j, n, circ) # insert x gate if anti-control
    if np.abs(ry_rotation_angle) > tolerance:
        circ.ry(angle=ry_rotation_angle, target=target_bit_index, control=control_qubit_list)
    if np.abs(rz_rotation_angle) > tolerance:
        circ.rz(angle=rz_rotation_angle, target=target_bit_index, control=control_qubit_list)
    if np.abs(ry_rotation_angle) > tolerance or np.abs(rz_rotation_angle) > tolerance:
        x_gate_sequence(s, j, n, circ) # insert x gate if anti-control
    
    
def qsp_qubit_eff(normalized_complex_array: np.ndarray) -> braket.circuits.circuit.Circuit:
    """
    Function to construct the full QSP circuit using the full multi control rotation gate
    
    @param normalized_complex_array: the entire wave function array vector values (can contain complex numbers) to be encoded
    
    @return circ: the constructed quantum circuit
    """
    amplitude_array = np.abs(normalized_complex_array)
    phase_array = np.angle(normalized_complex_array)
    
    array_len = len(normalized_complex_array)
    assert array_len > 0 and (array_len & (array_len - 1)) == 0 , "wave function array need to have length as power of 2, consider pad it with zeros"
    l2_norm = np.linalg.norm(normalized_complex_array, ord=2)
    assert abs(l2_norm - 1) < 1e-10, "wave function array need to be normalized"
    
    circ = Circuit()
    
    n = int(math.log2(len(normalized_complex_array)))
    for s in range(n, 0, -1): # as it exactly defined in the first figure above
            for j in range(2 ** (n - s), 0, -1):
                full_multi_control_rotation_gate(s, j, n, circ, amplitude_array, phase_array)
    return circ

