import numpy as np
from braket.circuits import Circuit

class QuantumStatePreparation:
    """
    Class for preparing a quantum state using amplitude and phase information 
    from a normalized complex array.
    """

    def __init__(self, normalized_complex_array: np.ndarray):
        """
        Initialize the QuantumStatePreparation with a normalized complex array.

        Args:
            normalized_complex_array (np.ndarray): A normalized complex array representing the quantum state.
        """
        self._normalized_complex_array = normalized_complex_array
        self._amplitude_array = np.abs(normalized_complex_array)
        self._phase_array = np.angle(normalized_complex_array)
        self._array_len = len(normalized_complex_array)

        # Validate that the array length is a power of 2
        assert self._array_len > 0 and (self._array_len & (self._array_len - 1)) == 0, \
            "Wave function array needs to have length as power of 2. Consider padding it with zeros."
        
        # Validate that the array is normalized
        l2_norm = np.linalg.norm(normalized_complex_array, ord=2)
        assert abs(l2_norm - 1) < 1e-7, "Wave function array needs to be normalized."

        self._n = int(np.log2(self._array_len))
        self._circ = Circuit()

    def get_amplitude_array(self) -> np.ndarray:
        """Return the amplitude array for debugging purposes."""
        return self._amplitude_array
    
    def get_phase_array(self) -> np.ndarray:
        """Return the phase array for debugging purposes."""
        return self._phase_array
    
    def get_array_len(self) -> int:
        """Return the length of the array for debugging purposes."""
        return self._array_len
    
    def get_n(self) -> int:
        """Return the number of qubits for debugging purposes."""
        return self._n

    def _compute_rz_rotation_angle(self, s: int, j: int) -> float:
        """
        Compute the Rz rotation angle for given s and j.

        Args:
            s (int): As it appears in equation 4.30 in the ML with QC book.
            j (int): As it appears in equation 4.30 in the ML with QC book.

        Returns:
            float: The computed Rz rotation angle.
        """
        indices_top = (2 * j - 1) * 2 ** (s - 1) + np.arange(2 ** (s - 1))
        indices_bottom = (2 * j - 2) * 2 ** (s - 1) + np.arange(2 ** (s - 1))
        sum_top = np.sum(self._phase_array[indices_top] - self._phase_array[indices_bottom])
        return sum_top / (2 ** (s - 1))
    
    def get_rz_rotation_angle(self, s:int, j: int) -> float:
        """Return the the rz angle for a particular <s, j> instance for debugging purposes."""
        return self._compute_rz_rotation_angle(s, j)

    def _compute_ry_rotation_angle(self, s: int, j: int) -> float:
        """
        Compute the Ry rotation angle for given s and j.

        Args:
            s (int): As it appears in equation 4.30 in the ML with QC book.
            j (int): As it appears in equation 4.30 in the ML with QC book.

        Returns:
            float: The computed Ry rotation angle.
        """
        top_indices = (2 * j - 1) * 2 ** (s - 1) + np.arange(2 ** (s - 1))
        sum_top = np.sum(self._amplitude_array[top_indices] ** 2)
        bottom_indices = (j - 1) * 2 ** s + np.arange(2 ** s)
        sum_bottom = np.sum(self._amplitude_array[bottom_indices] ** 2)
        if np.isclose(sum_bottom, 0.0):
            return 0.0
        return 2 * np.arcsin(np.sqrt(sum_top / sum_bottom))

    def get_ry_rotation_angle(self, s:int, j: int) -> float:
        """Return the the ry angle for a particular <s, j> instance for debugging purposes."""
        return self._compute_ry_rotation_angle(s, j)