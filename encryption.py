def generate_shared_key(result, aliceMeasurementChoices, bobMeasurementChoices, circuits, numberOfSinglets):
    key_alice = []
    key_bob = []
    
    for i in range(numberOfSinglets):
        # Alice's and Bob's bases need to match for a key to be generated
        if aliceMeasurementChoices[i] == bobMeasurementChoices[i]:
            res = list(result.get_counts(circuits[i]).keys())[0]
            print(f"Measurement result for circuit {i}: {res}")
            # Extract Alice's and Bob's measurement outcomes for key generation
            key_alice.append(int(res[-2]))  # Alice's outcome is stored in cr[0]
            key_bob.append(int(res[-1]))    # Bob's outcome is stored in cr[1]
    
    # Return both keys with equal length (truncate to match shorter key)
    min_key_length = min(len(key_alice), len(key_bob))
    return key_alice[:min_key_length], key_bob[:min_key_length]


# Function to XOR encrypt healthcare data using the shared key
def encrypt_healthcare_data(data, key):
    # Convert data to binary
    binary_data = ''.join(format(ord(char), '08b') for char in data)
    print(f"Binary data before encryption: {binary_data}")

    # Encrypt using XOR
    encrypted_data = ''.join(str(int(binary_data[i]) ^ key[i % len(key)]) for i in range(len(binary_data)))
    print(f"Encrypted binary data: {encrypted_data}")

    # Convert encrypted binary to a human-readable format (base64 or hex)
    return encrypted_data  # Change this to return base64 or hex if needed


# Function to XOR decrypt healthcare data using the shared key
def decrypt_healthcare_data(encrypted_data, key):
    print(f"Encrypted data for decryption: {encrypted_data}")

    # Decrypt using XOR
    decrypted_binary = ''.join(str(int(encrypted_data[i]) ^ key[i % len(key)]) for i in range(len(encrypted_data)))
    #print(f"Decrypted binary data: {decrypted_binary}")

    # Convert binary to original data
    decrypted_data = ''.join(chr(int(decrypted_binary[i:i+8], 2)) for i in range(0, len(decrypted_binary), 8))
    
    # Remove non-printable characters and keep only readable characters
    decrypted_data = ''.join(filter(lambda x: x.isprintable(), decrypted_data))
    print(f"Decrypted data: {decrypted_data}")

    return decrypted_data
