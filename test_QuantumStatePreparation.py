# to run all test, type the following code in Terminal: python3 -m unittest discover

import unittest
import numpy as np
from QuantumStatePreparation import QuantumStatePreparation
from helper_functions import generate_normalized_complex_array

class TestQuantumStatePreparation(unittest.TestCase):

    def setUp(self):
        self.input_array = [0.22202689-0.27077295j, -0.39217787-0.33686943j, 0.10936691+0.15168349j,
                            0.20360099+0.37102047j, -0.00122174-0.40592865j, -0.22520418+0.00997716j,
                            -0.24708095+0.25582373j,  0.21319728+0.09208224j]
        self.qsp = QuantumStatePreparation(self.input_array)
        self.large_input_array = generate_normalized_complex_array(10)
        self.qsp_large = QuantumStatePreparation(self.large_input_array)

    def test_initialization(self):
        self.assertEqual(self.qsp.get_array_len(), 8)
        self.assertEqual(self.qsp.get_n(), 3)
        np.testing.assert_almost_equal(self.qsp.get_amplitude_array(), np.abs(self.input_array))
        np.testing.assert_almost_equal(self.qsp.get_phase_array(), np.angle(self.input_array))

    def test_array_length_not_power_of_2(self):
        """
        Test that an exception is raised when the input array length is not a power of 2.
        """
        # Create an array of length 3 (not a power of 2)
        invalid_length_array = np.array([1 + 1j, 0 + 0j, 0 + 0j], dtype=np.complex128)

        with self.assertRaises(ValueError) as context:
            QuantumStatePreparation(invalid_length_array)
        
        self.assertTrue("Wave function array needs to have length as power of 2" in str(context.exception))

    def test_array_not_normalized(self):
        """
        Test that an exception is raised when the input array is not normalized.
        """
        # Create an array of length 4 that is not normalized
        not_normalized_array = np.array([1 + 0j, 1 + 0j, 0 + 0j, 0 + 0j], dtype=np.complex128)

        with self.assertRaises(ValueError) as context:
            QuantumStatePreparation(not_normalized_array)
        
        self.assertTrue("Wave function array needs to be normalized" in str(context.exception))


    def test_rz_rotation_angle(self):
        angle_11 = self.qsp.get_rz_rotation_angle(1, 1)
        angle_12 = self.qsp.get_rz_rotation_angle(1, 2)
        angle_13 = self.qsp.get_rz_rotation_angle(1, 3)
        angle_14 = self.qsp.get_rz_rotation_angle(1, 4)
        angle_21 = self.qsp.get_rz_rotation_angle(2, 1)
        angle_22 = self.qsp.get_rz_rotation_angle(2, 2)
        angle_31 = self.qsp.get_rz_rotation_angle(3, 1)

        expected_angle_11 = -1.5479194676028394
        expected_angle_12 = 0.12280456503629966
        expected_angle_13 = 4.671124921312853
        expected_angle_14 = -1.9311019846798128
        expected_angle_21 = 2.66545748949725
        expected_angle_22 = 0.61150428084382
        expected_angle_31 = 1.3927335150559301

        self.assertAlmostEqual(angle_11, expected_angle_11)
        self.assertAlmostEqual(angle_12, expected_angle_12)
        self.assertAlmostEqual(angle_13, expected_angle_13)
        self.assertAlmostEqual(angle_14, expected_angle_14)
        self.assertAlmostEqual(angle_21, expected_angle_21)
        self.assertAlmostEqual(angle_22, expected_angle_22)
        self.assertAlmostEqual(angle_31, expected_angle_31)

    def test_ry_rotation_angle(self):
        angle_11 = self.qsp.get_ry_rotation_angle(1, 1)
        angle_12 = self.qsp.get_ry_rotation_angle(1, 2)
        angle_13 = self.qsp.get_ry_rotation_angle(1, 3)
        angle_14 = self.qsp.get_ry_rotation_angle(1, 4)
        angle_21 = self.qsp.get_ry_rotation_angle(2, 1)
        angle_22 = self.qsp.get_ry_rotation_angle(2, 2)
        angle_31 = self.qsp.get_ry_rotation_angle(3, 1)

        expected_angle_11 = 1.9509323748251872
        expected_angle_12 = 2.3094685560086594
        expected_angle_13 = 1.0138511509434476
        expected_angle_14 = 1.1569091788177739
        expected_angle_21 = 1.2754161475988395
        expected_angle_22 = 1.4818736555372252
        expected_angle_31 = 1.3613136063500926

        self.assertAlmostEqual(angle_11, expected_angle_11)
        self.assertAlmostEqual(angle_12, expected_angle_12)
        self.assertAlmostEqual(angle_13, expected_angle_13)
        self.assertAlmostEqual(angle_14, expected_angle_14)
        self.assertAlmostEqual(angle_21, expected_angle_21)
        self.assertAlmostEqual(angle_22, expected_angle_22)
        self.assertAlmostEqual(angle_31, expected_angle_31)

    def test_arbitrary_large_instance(self):
        self.assertEqual(self.qsp_large.get_array_len(), 1024)
        self.assertEqual(self.qsp_large.get_n(), 10)
        np.testing.assert_almost_equal(self.qsp_large.get_amplitude_array(), np.abs(self.large_input_array))
        np.testing.assert_almost_equal(self.qsp_large.get_phase_array(), np.angle(self.large_input_array))



if __name__ == '__main__':
    unittest.main()