import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import braket
from braket.circuits import Circuit
from braket.devices import LocalSimulator

from qiskit import QuantumCircuit
from qiskit.execute_function import execute
from qiskit import BasicAer
from qiskit import transpile

# import functions from parent folder
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname('performance_benchmark'), ".."))
sys.path.append(parent_dir)
from QubitEfficientQSP import QubitEfficientQSP

from helper_functions import nicer_array_display

class BenchmarkTime():
    def __init__(self, normalized_complex_array: np.ndarray):
        """
        Initialize the BenchmarkTime with a normalized complex array.

        Args:
            normalized_complex_array (np.ndarray): A normalized complex array representing the quantum state.
        """
        self._normalized_complex_array = normalized_complex_array
        self._array_len = len(normalized_complex_array)
        self._n = int(np.log2(self._array_len))

        self._braket_circ = Circuit()
        self._qiskit_circ = QuantumCircuit(self._n)
        self._braket_circ_from_unitary_alt = Circuit()

    def setup_braket(self):
        qsp_braket = QubitEfficientQSP(self._normalized_complex_array) # construct the QSP object
        self.braket_circ = qsp_braket.construct_circuit() # create the circuit using the QSP object

    def run_braket(self):
        braket_device = LocalSimulator() # define the simulator
        self._braket_circ.state_vector() # convert the circuit to state vector
        braket_state_vector_result = braket_device.run(self._braket_circ, shots=0).result().values[0] # extract the result
        print(nicer_array_display(braket_state_vector_result, 3)) # print out the resulted state vector

    def setup_qiskit(self):
        self._qiskit_circ.initialize(self._normalized_complex_array, range(self._n))

    def run_qiskit_statevector(self):
        qiskit_backend = BasicAer.get_backend('statevector_simulator')
        job = execute(self._qiskit_circ, qiskit_backend)
        qiskit_state_vector_result = job.result().get_statevector()
        print(nicer_array_display(qiskit_state_vector_result, 3)) # print out the resulted state vector

    def setup_braket_unitary(self):
        braket_qsp_circ_unitary_matrix_alt = self._braket_circ.state_vector().to_unitary()
        self._braket_circ_from_unitary_alt.unitary(matrix=braket_qsp_circ_unitary_matrix_alt, targets=range(self._n))

    def run_braket_unitary(self):
        braket_device = LocalSimulator()
        self._braket_circ_from_unitary_alt.state_vector() # convert the circuit to state vector
        braket_result_from_unitary_alt = braket_device.run(self._braket_circ_from_unitary_alt, shots=0).result().values[0] # extract the result
        print(nicer_array_display(braket_result_from_unitary_alt, 3)) # print out the resulted state vector

