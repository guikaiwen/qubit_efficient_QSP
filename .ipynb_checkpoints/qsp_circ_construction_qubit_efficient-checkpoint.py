# Import Braket libraries
import braket
from braket.circuits import Circuit
from braket.aws import AwsDevice
from braket.devices import LocalSimulator

import numpy as np
import math

def compute_target_bit_angle(s: int, j: int, feature_array: np.ndarray) -> float:
    """
    Function to compute a particular beta_{s,j} angle according to the equation above
    
    @param s: as it appear in equation 4.30 in the ML with QC book
    @param j: as it appear in equation 4.30 in the ML with QC book
    @param feature_array: the entire feature array vector values to be encoded
    
    @return: a float/double value that holds the computed angle 
    """
    sum_top = 0.0
    for l in range(0, 2 ** (s - 1) - 1 + 1): # compute the sum on the numerator
        current_var = feature_array[(2 * j - 1) * 2 ** (s - 1) + l]
        sum_top += current_var ** 2
    
    sum_bottom = 0.0
    for l in range(0, 2 ** s - 1 + 1): # compute the sum on the denominator
        current_var = feature_array[(j - 1) * 2 ** s + l]
        sum_bottom += current_var ** 2
        
    if sum_bottom == 0: # edge case: arcsin denominator is zero
        return 0.0
    else:
        return 2 * np.arcsin(np.sqrt(sum_top) / np.sqrt(sum_bottom))
    
    
def x_gate_sequence(s: int, j: int, total_qubit_num: int, circ: braket.circuits.circuit.Circuit):
    """
    Function to add x gates to help emulate the anti-control operations
    
    @param s: as it appear in the equation above
    @param j: as it appear in the equation above
    total_qubit_num: total number of qubits for the state being prepared
    circ: quantum circuit to operate on
    """
    binary_j = bin(j - 1).replace("0b", "").zfill(total_qubit_num - s) # get the binary representation of the current j
    for i in range(total_qubit_num - s):
        if int(binary_j[i]) == 0:
            circ.x(i)
            
            
def full_multi_control_rotation_gate(s: int, j: int, total_qubit_num: int, circ: braket.circuits.circuit.Circuit, feature_array: np.ndarray):
    """
    Function to perform a full multi-control rotation gate based on the s and j values, will anti-control conditions included

    @param s: as it appear in equation 4.30 in the ML with QC book
    @param j: as it appear in equation 4.30 in the ML with QC book
    @param total_qubit_num: total number of qubits for the state being prepared
    @param circ: quantum circuit to operate on
    @param feature_array: the entire feature array vector values to be encoded 
    """
    target_bit_index = total_qubit_num - s
    target_bit_angle = compute_target_bit_angle(s, j, feature_array)
    control_qubit_list = list(range(target_bit_index)) # get the control qubit list
    
    x_gate_sequence(s, j, total_qubit_num, circ) # insert x gate if anti-control
    circ.ry(angle=target_bit_angle, target=target_bit_index, control=control_qubit_list)
    x_gate_sequence(s, j, total_qubit_num, circ) # insert x gate if anti-control
    
    
def qsp_qubit_eff(feature_array: np.ndarray, mode='initialization', orig_circ=None) -> braket.circuits.circuit.Circuit:
    """
    Function to construct the full QSP circuit using the full multi control rotation gate
    
    @param feature_array: the entire feature array vector values to be encoded
    @param mode: can be in 2 modes, initialization mode to contruct the qsp circuit from the |0> state, or append mode to append the qsp circuit onto another circuit
    @param orig_circ, original circuit to pass in if set in append mode
    
    @return circ: the constructed quantum circuit
    """
    array_len = len(feature_array)
    assert array_len > 0 and (array_len & (array_len - 1)) == 0 , "feature array need to have length as power of 2, consider pad it with zeros"
    l2_norm = np.linalg.norm(feature_array, ord=2)
    assert abs(l2_norm - 1) < 1e-10, "feature array need to be normalized"
    
    if mode == 'initialization':
        circ = Circuit()
    if mode == 'append':
        circ = orig_circ
    
    total_qubit_num = int(math.log2(len(feature_array)))
    for s in range(total_qubit_num, 0, -1):
            for j in range(2 ** (total_qubit_num - s), 0, -1):
                full_multi_control_rotation_gate(s, j, total_qubit_num, circ, feature_array)
    return circ

