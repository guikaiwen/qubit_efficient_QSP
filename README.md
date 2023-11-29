# qubit_efficient_QSP

This repo provides implementations and performance testings for quantum state preparation circuits using a qubit-efficient protocol (no ancilla qubit required) suitable for circuit simulators. 

That is, given an arbitrary list of $2^n$ amplitudes, we create a quantum circuit that creates the corresponding $n$-qubit state:

$$U_{\mathrm{QSP}} |0^n\rangle = |\psi\rangle = \frac{1}{\lVert \mathbf{x}\rVert}\sum_{i=0}^{2^{n-1}}x_i |i\rangle, x_i \in \mathbb{C}$$
 u
The quantum circuit consists of a sequence of multi-control Ry and multi-control Rz gates, using the method described by Mottonen et al. 2004 (https://arxiv.org/pdf/quant-ph/0407010.pdf).

1. You can directly call the QSP function `qsp_qubit_eff` (implemented in `qsp_circ_construction_qubit_efficient.py`) to prepare an arbitrary quantum state, as demonstrated in `QSP_method_call_demo.ipynb`. That is, the function prepares the wave function state vector.

2. We also provide a detailed implementation walkthrough in `QSP_detailed_implementation.ipynb`. We recommend first-time readers start with the walk-through in `QSP_method_call_demo.ipynb`.

3. We compare our implementation performance for dense quantum states against the existing Qiskit's `.initialize` function and the Braket's unitary operation in `performance_benchmark/dense_state_comparisons.ipynb`.

<img width="756" alt="Screenshot 2023-11-08 at 4 11 17 PM" src="https://github.com/guikaiwen/qubit_efficient_QSP/assets/24789128/8dfcc84d-40c8-42d2-9f36-d9dbbd931f71">

4. We provide some performance testings and complexity analysis of sparse state preparation for Braket in `performance_benchmark/braket_sparse_state_cost_benchmark.ipynb` and for Qiskit in `performance_benchmarkqiskit_sparse_state_gate_count.ipynb`.

-------------------------------
## Prerequisites

The Amazon Braket Python SDK can be installed with pip on your local machine as follows:
```ruby
pip install amazon-braket-sdk
```

The IBM Qiskit Python SDK can be installed with pip on your local machine as follows:
```ruby
pip install qiskit
```

See `requirements.txt` for other required Python packages and corresponding versions.

-------------------------------
The current QSP operation demonstrated in this repo has the following circuit complexity numbers:

A. $O(N)$ depth using generalized multi-controlled Ry gates

B. No additional ancilla qubits required (total of $O(\log(N))$ qubits)

(Note that $N = 2^n$ is the total number of amplitude values encoded, and $n$ can also represent the number of data qubits.)

See https://github.com/guikaiwen/QSP_Paper_Artifact and https://arxiv.org/pdf/2303.02131.pdf for an alternative method that has the following circuit complexity numbers:

A. $O(\log(N))$ depth using arbitrary single qubit gate + CNOT gate

B. $O(N)$ ancilla qubits required

-------------------------------
Please contact kgui@uchicago.edu if you have any questions.
