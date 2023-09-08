import numpy as np
import math
from braket.circuits import Circuit


def compute_target_bit_angle(s, j, feature_array):
    sum_1 = 0.0
    for l in range(0, 2 ** (s - 1) - 1 + 1):
        current_var = feature_array[(2 * j - 1) * 2 ** (s - 1) + l]
        # print(current_var)
        sum_1 = sum_1 + current_var ** 2
    
    sum_2 = 0.0
    for l in range(0, 2 ** s - 1 + 1):
        current_var = feature_array[(j - 1) * 2 ** s + l]
        # print(current_var)
        sum_2 = sum_2 + current_var ** 2
        
    if sum_2 == 0: # edge case: arcsin denominator is zero
        return 0.0
    else:
        return 2 * np.arcsin(np.sqrt(sum_1) / np.sqrt(sum_2))
    

def multi_control_rotation_gate_matrix(s, total_qubit_num, target_bit_angle):
    matrix_size = 2 ** (total_qubit_num + 1 - s)
    gate_matrix = [[0] * matrix_size for _ in range(matrix_size)] # initialize the matrix with zeros
    for i in range(0, matrix_size - 2):
        gate_matrix[i][i] = 1 # fill the diagonal elements with 1
    
    # modify the last 4 elements to the corresponding trig values
    gate_matrix[matrix_size - 2][matrix_size - 2] = np.cos(target_bit_angle / 2)
    gate_matrix[matrix_size - 2][matrix_size - 1] = -np.sin(target_bit_angle / 2)
    gate_matrix[matrix_size - 1][matrix_size - 2] = np.sin(target_bit_angle / 2)
    gate_matrix[matrix_size - 1][matrix_size - 1] = np.cos(target_bit_angle / 2)
    return gate_matrix


def full_multi_control_rotation_gate_unitary(s, j, total_qubit_num, circ, feature_array):
    # make some assertions on j to prevent out of range issue
    # assert feature vector is normalized
    # add if statement to prevent zero rotation gates
    target_bit_angle = compute_target_bit_angle(s, j, feature_array)
    # print(target_bit_angle)
    binary_j = bin(j - 1).replace("0b", "").zfill(total_qubit_num - s)
    # print(binary_j)
    for i in range(total_qubit_num - s):
        if int(binary_j[i]) == 0:
            circ.x(i)
    qubit_list = []
    for i in range(total_qubit_num - s + 1):
        qubit_list.append(i)
    circ.unitary(matrix=np.array(multi_control_rotation_gate_matrix(s, total_qubit_num, target_bit_angle)), targets=qubit_list)
    for i in range(total_qubit_num - s):
        if int(binary_j[i]) == 0:
            circ.x(i)
            

def get_qsp_circ_unitary(WF_array): 
    n = int(math.log2(len(WF_array)))
    
    circ = Circuit()
    for s in range(n, 0, -1):
        for j in range(2 ** (n - s), 0, -1):
            full_multi_control_rotation_gate_unitary(s, j, n, circ, WF_array)
    
    circ_unitary = circ.to_unitary()
    
    return circ_unitary