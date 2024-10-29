from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
import numpy as np
import random
import re
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer
from encryption import generate_shared_key, encrypt_healthcare_data, decrypt_healthcare_data

with open('healthcare_data.txt', 'r') as file:
    healthcare_data = file.read()

print(f"Original Healthcare Data: {healthcare_data}")

def ekert_91():
    # Creating registers
    qr = QuantumRegister(2, name="qr")
    cr = ClassicalRegister(2, name="cr")  # Only 2 classical bits are needed

    # Prepare the singlet state (entangled qubits)
    singlet = QuantumCircuit(qr, cr, name='singlet')
    singlet.h(qr[0])
    singlet.cx(qr[0], qr[1])

    # Define Alice's measurement circuits for different bases
    measureA1 = QuantumCircuit(qr, cr, name='measureA1')
    measureA1.h(qr[0])
    measureA1.measure(qr[0], cr[0])

    measureA2 = QuantumCircuit(qr, cr, name='measureA2')
    measureA2.s(qr[0])
    measureA2.h(qr[0])
    measureA2.measure(qr[0], cr[0])

    measureA3 = QuantumCircuit(qr, cr, name='measureA3')
    measureA3.measure(qr[0], cr[0])

    # Define Bob's measurement circuits for different bases
    measureB1 = QuantumCircuit(qr, cr, name='measureB1')
    measureB1.s(qr[1])
    measureB1.h(qr[1])
    measureB1.measure(qr[1], cr[1])

    measureB2 = QuantumCircuit(qr, cr, name='measureB2')
    measureB2.measure(qr[1], cr[1])

    measureB3 = QuantumCircuit(qr, cr, name='measureB3')
    measureB3.s(qr[1])
    measureB3.h(qr[1])
    measureB3.measure(qr[1], cr[1])

    # Create measurement choices and combine with singlet
    aliceMeasurements = [measureA1, measureA2, measureA3]
    bobMeasurements = [measureB1, measureB2, measureB3]

    numberOfSinglets = 4000
    aliceMeasurementChoices = [random.randint(1, 3) for _ in range(numberOfSinglets)]
    bobMeasurementChoices = [random.randint(1, 3) for _ in range(numberOfSinglets)]

    circuits = []
    for i in range(numberOfSinglets):
        combined_circuit = singlet.compose(aliceMeasurements[aliceMeasurementChoices[i] - 1])
        combined_circuit = combined_circuit.compose(bobMeasurements[bobMeasurementChoices[i] - 1])
        circuits.append(combined_circuit)

    backend = Aer.get_backend('qasm_simulator')
    transpiled_result = transpile(circuits, backend)
    job = backend.run(transpiled_result, shots=500).result()

    # Plot the measurement outcomes
    plot_measurement_outcomes(job, circuits, numberOfSinglets)

    # Function to calculate the CHSH correlation value
    def chsh_corr(result):
        countA1B1 = [0, 0, 0, 0]
        countA1B3 = [0, 0, 0, 0]
        countA3B1 = [0, 0, 0, 0]
        countA3B3 = [0, 0, 0, 0]

        abPatterns = [
            re.compile('00$'),
            re.compile('01$'),
            re.compile('10$'),
            re.compile('11$')
        ]

        for i in range(numberOfSinglets):
            res = list(result.get_counts(circuits[i]).keys())[0]
            if (aliceMeasurementChoices[i] == 1 and bobMeasurementChoices[i] == 1):
                for j in range(4):
                    if abPatterns[j].search(res):
                        countA1B1[j] += 1

            if (aliceMeasurementChoices[i] == 1 and bobMeasurementChoices[i] == 3):
                for j in range(4):
                    if abPatterns[j].search(res):
                        countA1B3[j] += 1

            if (aliceMeasurementChoices[i] == 3 and bobMeasurementChoices[i] == 1):
                for j in range(4):
                    if abPatterns[j].search(res):
                        countA3B1[j] += 1

            if (aliceMeasurementChoices[i] == 3 and bobMeasurementChoices[i] == 3):
                for j in range(4):
                    if abPatterns[j].search(res):
                        countA3B3[j] += 1

        total11 = sum(countA1B1) or 1  # Avoid division by zero
        total13 = sum(countA1B3) or 1
        total31 = sum(countA3B1) or 1
        total33 = sum(countA3B3) or 1

        expect11 = (countA1B1[0] - countA1B1[1] - countA1B1[2] + countA1B1[3]) / total11
        expect13 = (countA1B3[0] - countA1B3[1] - countA1B3[2] + countA1B3[3]) / total13
        expect31 = (countA3B1[0] - countA3B1[1] - countA3B1[2] + countA3B1[3]) / total31
        expect33 = (countA3B3[0] - countA3B3[1] - countA3B3[2] + countA3B3[3]) / total33

        print(f'E(a1, b1) = {expect11}')
        print(f'E(a1, b3) = {expect13}')
        print(f'E(a3, b1) = {expect31}')
        print(f'E(a3, b3) = {expect33}')

        # CHSH value calculation
        corr = expect11 - expect13 + expect31 + expect33

        plot_chsh_histogram(countA1B1, countA1B3, countA3B1, countA3B3)

        return corr

    # Calculate and print CHSH correlation value
    corr = chsh_corr(job)
    print(f'CHSH correlation value: {round(corr, 3)}')

    # Generate shared keys
    key_alice, key_bob = generate_shared_key(job, aliceMeasurementChoices, bobMeasurementChoices, circuits, numberOfSinglets)

    def check_shared_keys(key_alice, key_bob):
        print(f"alice key: {key_alice}, bob key: {key_bob}")
        if len(key_alice) != len(key_bob):
            print("Key lengths do not match.")
            return False
        if key_alice == key_bob:
            print("Both keys match.")
            return True
        else:
            print("Keys do not match.")
            return False
        
    # Check if keys match
    keys_are_same = check_shared_keys(key_alice, key_bob)
    print(keys_are_same)

    return key_alice, key_bob


def encrypting():
    with open('healthcare_data.txt', 'r') as file:
        healthcare_data = file.read()

    patient_records = healthcare_data.split('Patient: ')
    print(patient_records)

    encrypted_records = []
    key_alice, key_bob = ekert_91()

    for record in patient_records:
        encrypted_record = encrypt_healthcare_data(record, key_alice)
        encrypted_records.append(encrypted_record)

        print(f"Encrypted data: {encrypted_record}")
        decrypted_data = decrypt_healthcare_data(encrypted_record, key_bob)
        print(f"Decrypted data: {decrypted_data}")


def calculate_qber(key_alice, key_bob, sample_size):
    assert len(key_alice) == len(key_bob), "Key lengths must be the same."

    if sample_size > len(key_alice):
        raise ValueError("Sample size cannot be larger than the key length")

    sample_indices = random.sample(range(len(key_alice)), sample_size)
    error_count = sum([1 for i in sample_indices if key_alice[i] != key_bob[i]])
    qber = error_count / sample_size
    return qber


def plot_measurement_outcomes(job, circuits, numberOfSinglets):
    counts_list = [job.get_counts(circuit) for circuit in circuits]
    sample_index = random.randint(0, numberOfSinglets - 1)
    plot_histogram(counts_list[sample_index], title=f"Sample Measurement Outcomes for Singlet {sample_index}")

    aggregated_counts = counts_list[0]
    for counts in counts_list[1:]:
        for key, value in counts.items():
            aggregated_counts[key] = aggregated_counts.get(key, 0) + value
    plot_histogram(aggregated_counts, title="Aggregated Measurement Outcomes for All Singlets")


def plot_chsh_histogram(counts_a1b1, counts_a1b3, counts_a3b1, counts_a3b3):
    combined_counts = {
        "A1B1_00": counts_a1b1[0],
        "A1B1_01": counts_a1b1[1],
        "A1B1_10": counts_a1b1[2],
        "A1B1_11": counts_a1b1[3],
        "A1B3_00": counts_a1b3[0],
        "A1B3_01": counts_a1b3[1],
        "A1B3_10": counts_a1b3[2],
        "A1B3_11": counts_a1b3[3],
        "A3B1_00": counts_a3b1[0],
        "A3B1_01": counts_a3b1[1],
        "A3B1_10": counts_a3b1[2],
        "A3B1_11": counts_a3b1[3],
        "A3B3_00": counts_a3b3[0],
        "A3B3_01": counts_a3b3[1],
        "A3B3_10": counts_a3b3[2],
        "A3B3_11": counts_a3b3[3]
    }
    
    plot_histogram(combined_counts, title="CHSH Measurement Outcomes")


if __name__ == "__main__":
    encrypting()