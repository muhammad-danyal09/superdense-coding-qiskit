# Superdense Coding
# Source: Superdense coding.ipynb (Google Drive: Project super dense coding)

### 1. Installing Qiskit packages
# This section installs relevant Qiskit packages to proceed with the project.

# !pip install qiskit
# !pip install qiskit-aer
# !pip install pylatexenc

#### 1.1 Checking versions:
from qiskit import __version__
print(__version__)

from qiskit_aer import __version__
print(__version__)

#### 1.2 Importing Necessary Libraries
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import pylatexenc

### 2. Scenario and Protocol Setup / 3. Analysis / 4. Verification of Protocol
c = '1'
d = '0'
protocol = QuantumCircuit(2)

# Preparing ebit that will be used for superdense coding
protocol.h(0)
protocol.cx(0, 1)
protocol.barrier()

# ALice's operation
if d == '1':
  protocol.z(0)

if c == '1':
  protocol.x(0)
protocol.barrier()

# Bob's actions
protocol.cx(0, 1)
protocol.h(0)

protocol.measure_all()
display(protocol.draw(output = 'mpl'))

# Now I'm going to run Aer simulator.
simulator = AerSimulator()
job = simulator.run(protocol, shots = 4096)
result = job.result()
statistics = result.get_counts()

for outcome, frequency in statistics.items():
  print(f'Measured {outcome} and with frequency {frequency}')

display(plot_histogram(statistics))

# **Result**
# When the input is fixed (i.e., c=1, d = 0), we get a 100% "10" outcome measured in all 4096 shots.
# It confirms that Alice's I, X, Z, or XZ gates (encoding) and Bob's C-NOT + Hadamard operations (decoding)
# correctly recover the transmitted 2-bit message with zero error for a fixed, known input when we run our
# circuit on an ideal Aer simulator.

#### 5.1 Random Bit Generator and Superdense Coding Protocol
# Now I will use an additional qubit as a random bit generator to randomly choose "c" and "d",
# and then run the superdense coding protocol.
random_bit_generator = QuantumRegister(1, 'coin')
qubit_Alice = QuantumRegister(1, 'A')
qubit_Bob = QuantumRegister(1, 'B')
Alice_c = ClassicalRegister(1, 'c')
Alice_d = ClassicalRegister(1, 'd')

test = QuantumCircuit(random_bit_generator, qubit_Alice, qubit_Bob, Alice_c, Alice_d)

# Again preparing the e-bit
test.h(qubit_Alice)
test.cx(qubit_Alice, qubit_Bob)
test.barrier()


# Using the coin qubit twice to generate Alice's bits 'c' and 'd'.
test.h(random_bit_generator)
test.measure(random_bit_generator, Alice_c)
test.h(random_bit_generator)
test.measure(random_bit_generator, Alice_d)
test.barrier()

# Now protocol runs, starting with Alice's actions, which depends on her bits
with test.if_test((Alice_c, 1), label = "X"):
  test.x(qubit_Alice)

with test.if_test((Alice_d, 1), label = "Z"):
  test.z(qubit_Alice)
test.barrier()

# Bob's Action
test.cx(qubit_Alice, qubit_Bob)
test.h(qubit_Alice)
test.barrier()

# Bob's Action: Creating ouput bits of Bob after measuremnt and then streamline it with my circuit
Bob_c = ClassicalRegister(1, "Bob_c")
Bob_d = ClassicalRegister(1, "Bob_d")

test.add_register(Bob_c)
test.add_register(Bob_d)
test.measure(qubit_Alice, Bob_d )
test.measure(qubit_Bob, Bob_c)

display(test.draw('mpl'))

# Running the Aer simulator shows the results:
result = AerSimulator().run(test, shots = 4096).result()
statistics = result.get_counts()
display(plot_histogram(statistics))

# **Result**
# The random bit generator generates Alice's bits 'c' and 'd' randomly instead of fixing them. As a result,
# we get four 4-bit outcomes (0000, 0101, 1010, 1111) with approximately equal probabilities. The probabilities
# of our outcomes are given by:
# 1. P(0000) ~ 1048/4096 ~ 25.6%
# 2. P(0101) ~ 993/4096 ~ 24.2%
# 3. P(1010) ~ 1063/4096 ~ 26%
# 4. P(1111) ~ 992/4096 ~ 24.2%
#
# Each 4-bit outcome is structured as Alice's bits and Bob's bits, i.e., cdcd. The fact that every observed
# outcome has this repeated-pair structure is the key result that Bob's decoded bits are bit-for-bit identical
# to Alice's original, randomly generated bits in every single shot.
#
# **Why only 4-bit outcomes appear?**
#
# With four classical bits, there are 16 possible outcomes. But only four of them are observed in our graph
# (the ones where the first two bits and the last two bits are equal) because:
#
# * The other outcomes (e.g., 0001, 0110, 1100 etc.) would represent a decoding error. Since the simulation
#   is noiseless and error-free, this never happens, and those outcomes have exactly zero counts.
# * The circuit is a noise-free deterministic quantum simulation, and there is no mechanism in an ideal
#   circuit for Bob's bits to differ from Alice's bits.
# * The only randomness in the circuit comes from the coin qubit which determines what Alice sends (c, d)
#   for every individual shot; Bob's output always matches.

### 6. Conclusion:
# Both simulations confirm 100% fidelity of the superdense coding protocol. Bob correctly recovers Alice's
# 2 classical bits from a single transmitted qubit in every shot, for both "fixed test case" and "randomized
# inputs". It validates the theoretical claim that shared entanglement doubles the classical information
# capacity of a single qubit.
