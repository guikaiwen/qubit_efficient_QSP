import numpy as np
from braket.circuits import Circuit
from QuantumStatePreparation import QuantumStatePreparation

class QubitEfficientQSP(QuantumStatePreparation):
    """
    Class for preparing a quantum state using a qubit efficient method.
    Inherits from QuantumStatePreparation.
    """

    def _x_gate_sequence(self, s: int, j: int):
        """
        Add X gates to emulate the anti-control operations.

        Args:
            s (int): As it appears in equation 4.30 in the ML with QC book.
            j (int): As it appears in equation 4.30 in the ML with QC book.
        """
        binary_j = bin(j - 1).replace("0b", "").zfill(self._n - s)
        for i in range(self._n - s):
            if int(binary_j[i]) == 0:
                self.circ.x(i)

    def _full_multi_control_rotation_gate(self, s: int, j: int, tolerance: float = 1e-100):
        """
        Perform a full multi-control rotation gate based on the s and j values, 
        including anti-control conditions.

        Args:
            s (int): As it appears in equation 4.30 in the ML with QC book.
            j (int): As it appears in equation 4.30 in the ML with QC book.
            tolerance (float): A small value to determine if a number is close enough to zero to be treated as zero.
        """
        ry_rotation_angle = self._compute_ry_rotation_angle(s, j)
        rz_rotation_angle = self._compute_rz_rotation_angle(s, j)
        target_bit_index = self._n - s
        control_qubit_list = list(range(target_bit_index))

        if np.abs(ry_rotation_angle) > tolerance or np.abs(rz_rotation_angle) > tolerance:
            self._x_gate_sequence(s, j)
        
        if np.abs(ry_rotation_angle) > tolerance:
            self.circ.ry(angle=ry_rotation_angle, target=target_bit_index, control=control_qubit_list)
        
        if np.abs(rz_rotation_angle) > tolerance:
            self.circ.rz(angle=rz_rotation_angle, target=target_bit_index, control=control_qubit_list)
        
        if np.abs(ry_rotation_angle) > tolerance or np.abs(rz_rotation_angle) > tolerance:
            self._x_gate_sequence(s, j)

    def construct_circuit(self) -> Circuit:
        """
        Construct the full quantum state preparation (QSP) circuit using the qubit efficient method.

        Returns:
            Circuit: The constructed quantum circuit.
        """
        for s in range(self._n, 0, -1):
            for j in range(2 ** (self._n - s), 0, -1):
                self._full_multi_control_rotation_gate(s, j)
        return self.circ