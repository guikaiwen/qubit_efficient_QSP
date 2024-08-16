import unittest
import numpy as np
from QubitEfficientQSP import QubitEfficientQSP

from braket.devices import LocalSimulator

from helper_functions import generate_normalized_complex_array, generate_normalized_real_array, generate_normalized_real_sparse_array

class TestQubitEfficientQSP(unittest.TestCase):

    def setUp(self):
            self.input_array = [0.22202689-0.27077295j, -0.39217787-0.33686943j, 0.10936691+0.15168349j,
                                0.20360099+0.37102047j, -0.00122174-0.40592865j, -0.22520418+0.00997716j,
                                -0.24708095+0.25582373j,  0.21319728+0.09208224j]
            self.qsp = QubitEfficientQSP(self.input_array)
            
            self.large_real_input_array = generate_normalized_real_array(6)
            self.large_complex_input_array = generate_normalized_complex_array(6)
            self.sparse_input_array = generate_normalized_real_sparse_array(6, [1, 3, 6, 15, 30])
            
            self.large_real_qsp = QubitEfficientQSP(self.large_real_input_array)
            self.large_complex_qsp = QubitEfficientQSP(self.large_complex_input_array)
            self.sparse_qsp = QubitEfficientQSP(self.sparse_input_array)

    def test_initialization(self):
        self.assertEqual(self.qsp.get_array_len(), 8)
        self.assertEqual(self.qsp.get_n(), 3)
        np.testing.assert_almost_equal(self.qsp.get_amplitude_array(), np.abs(self.input_array))
        np.testing.assert_almost_equal(self.qsp.get_phase_array(), np.angle(self.input_array))

    def test_construct_circuit(self):
        circuit = self.qsp.construct_circuit()
        braket_device = LocalSimulator() # define the simulator
        circuit.state_vector() # convert the circuit to state vector
        braket_state_vector_result = braket_device.run(circuit, shots=0).result().values[0] # extract the result
        vec_norm = np.abs(np.dot(self.input_array, np.conj(braket_state_vector_result))) # compute |<psi'|psi>| since there might be global phase diff
        np.testing.assert_almost_equal(vec_norm, 1.0)

    def test_large_construct_circuit_real(self):
        circuit = self.large_real_qsp.construct_circuit()
        braket_device = LocalSimulator() # define the simulator
        circuit.state_vector() # convert the circuit to state vector
        braket_state_vector_result = braket_device.run(circuit, shots=0).result().values[0] # extract the result
        np.testing.assert_almost_equal(self.large_real_input_array, braket_state_vector_result)

    def test_large_construct_circuit_complex(self):
        circuit = self.large_complex_qsp.construct_circuit()
        braket_device = LocalSimulator() # define the simulator
        circuit.state_vector() # convert the circuit to state vector
        braket_state_vector_result = braket_device.run(circuit, shots=0).result().values[0] # extract the result
        vec_norm = np.abs(np.dot(self.large_complex_input_array, np.conj(braket_state_vector_result))) # compute |<psi'|psi>| since there might be global phase diff
        np.testing.assert_almost_equal(vec_norm, 1.0)
         
    def test_sparse_construct_circuit(self):
        circuit = self.sparse_qsp.construct_circuit()
        braket_device = LocalSimulator() # define the simulator
        circuit.state_vector() # convert the circuit to state vector
        braket_state_vector_result = braket_device.run(circuit, shots=0).result().values[0] # extract the result
        np.testing.assert_almost_equal(self.sparse_input_array, braket_state_vector_result)
         

if __name__ == '__main__':
    unittest.main()