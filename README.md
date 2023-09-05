# qubit_efficient_QSP

This repo provides two examples of using our quantum state preparation functions.

You can directly call the QSP function (implemented in qsp_circ_construction_qubit_efficient.py) to prepare an arbitrary quantum state, as demonstrated in QSP_Method_Call_Demo.ipynb.

We also provide a detailed implementation walkthrough in [Detailed Implementation] QSP.ipynb.

We recommend first-time readers start with the walk-through in QSP_Method_Call_Demo.ipynb.

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
