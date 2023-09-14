# qubit_efficient_QSP

This repo provides two examples of using our quantum state preparation functions.

You can directly call the QSP function `qsp_qubit_eff` (implemented in `qsp_circ_construction_qubit_efficient.py`) to prepare an arbitrary quantum state, as demonstrated in `QSP_Method_Call_Demo.ipynb`.

We also provide a detailed implementation walkthrough in `[Detailed Implementation] QSP.ipynb`.

We recommend first-time readers start with the walk-through in `QSP_Method_Call_Demo.ipynb`.

We also provide a performance comparison in `Comparison_to_Other_Methods.ipynb` against the existing Qiskit's `.initialize` function and the Braket's unitary operation.

<img width="573" alt="Performance Comparison" src="https://github.com/guikaiwen/qubit_efficient_QSP/assets/24789128/6672ce54-d52a-4081-ad26-a3c8b6ba7703">


-------------------------------
## Prerequisites

The Amazon Braket Python SDK can be installed with pip on your local machine as follows:
```ruby
pip install amazon-braket-sdk
```
See https://pypi.org/project/amazon-braket-sdk/ for more installation details.

The current Braket SDK version is `1.55.0`.

The IBM Qiskit Python SDK can be installed with pip on your local machine as follows:
```ruby
pip install qiskit
```
See https://qiskit.org/documentation/getting_started.html for more installation details.

The current Qiskit SDK version is `0.44.1`.

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
