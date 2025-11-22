import os

# --- ALU Logic Functions (Reused) ---

def to_signed_int(bits, width=4):
    """Converts a binary string (two's complement) to a signed integer."""
    decimal_val = int(bits, 2)
    if bits[0] == '1':
        return decimal_val - (1 << width)
    return decimal_val

def to_twos_complement_bin(val, width=4):
    """Converts a signed integer to a two's complement binary string of a given length."""
    mask = (1 << width) - 1
    return bin(val & mask)[2:].zfill(width)

def to_ones_complement_bin(bits):
    """Converts a binary string to its one's complement representation."""
    return ''.join(['1' if bit == '0' else '0' for bit in bits])

def alu_operation_4bit(A_bin, B_bin, opcode_bin):
    """
    Simulates the 4-bit ALU operation based on the opcode, yielding a 4-bit result.
    """
    
    BITS = 4
    MAX_UNSIGNED = (1 << BITS) - 1
    
    A_signed = to_signed_int(A_bin, BITS)
    B_signed = to_signed_int(B_bin, BITS)
    A_unsigned = int(A_bin, 2)
    B_unsigned = int(B_bin, 2)
    
    result_bin = 'xxxx' 

    # --- Arithmetic Operations (0000 - 0011) ---
    if opcode_bin in ['0000', '0001', '0010']:
        if opcode_bin == '0000': 
            unsigned_res = A_unsigned + B_unsigned
        elif opcode_bin == '0001': 
            unsigned_res = A_unsigned - B_unsigned
        elif opcode_bin == '0010': 
            unsigned_res = B_unsigned - A_unsigned
            
        result_val = unsigned_res & MAX_UNSIGNED
        result_bin = bin(result_val)[2:].zfill(BITS)

    elif opcode_bin == '0011': # Multiply A * B
        product = A_signed * B_signed
        result_bin = to_twos_complement_bin(product, BITS)
        
    # --- Logic and Bit-wise Operations (0100 - 1111) ---
    elif opcode_bin == '0100': # Bit-wise AND
        result = A_unsigned & B_unsigned
        result_bin = bin(result)[2:].zfill(BITS)
    elif opcode_bin == '0101': # Bit-wise OR
        result = A_unsigned | B_unsigned
        result_bin = bin(result)[2:].zfill(BITS)
    elif opcode_bin == '0110': # Bit-wise XOR
        result = A_unsigned ^ B_unsigned
        result_bin = bin(result)[2:].zfill(BITS)
    elif opcode_bin == '0111': # Bit-wise NAND
        result = ~(A_unsigned & B_unsigned) & MAX_UNSIGNED
        result_bin = bin(result)[2:].zfill(BITS)
    elif opcode_bin == '1000': # Display A in two's complement
        result_bin = A_bin
    elif opcode_bin == '1001': # Display A in one's complement
        result_bin = to_ones_complement_bin(A_bin)
    elif opcode_bin == '1010' or opcode_bin == '1100': # Shift A left Logical/Arithmetic
        shifted = (A_unsigned << 1) & MAX_UNSIGNED
        result_bin = bin(shifted)[2:].zfill(BITS)
    elif opcode_bin == '1011': # Shift A right logical
        shifted = A_unsigned >> 1
        result_bin = bin(shifted)[2:].zfill(BITS)
    elif opcode_bin == '1101': # Shift A right Arithmetic
        shifted = A_signed >> 1
        result_bin = to_twos_complement_bin(shifted, BITS)
    elif opcode_bin == '1110': # Shift A left circular
        msb = (A_unsigned >> 3) & 1
        shifted = ((A_unsigned << 1) | msb) & MAX_UNSIGNED
        result_bin = bin(shifted)[2:].zfill(BITS)
    elif opcode_bin == '1111': # Shift A right circular
        lsb = A_unsigned & 1
        shifted = (A_unsigned >> 1) | (lsb << 3)
        result_bin = bin(shifted)[2:].zfill(BITS)

    return result_bin

def generate_complete_truth_table(filename="alu_complete_truth_table.txt"):
    """
    Generates all 4096 possible rows of the truth table.
    """
    
    total_rows = 0
    
    with open(filename, 'w') as f:
        # Write header
        header = "A[4]\tB[4]\tC[4]\tOutput[4]"
        f.write(header + "\n")
        
        # Iterate A from 0000 to 1111 (0 to 15)
        for A_val in range(16):
            A_bin = bin(A_val)[2:].zfill(4)
            
            # Iterate B from 0000 to 1111 (0 to 15)
            for B_val in range(16):
                B_bin = bin(B_val)[2:].zfill(4)
                
                # Iterate Opcode from 0000 to 1111 (0 to 15)
                for opcode_val in range(16):
                    opcode_bin = bin(opcode_val)[2:].zfill(4)
                    
                    output_bin = alu_operation_4bit(A_bin, B_bin, opcode_bin)
                    
                    # Format row with tabs
                    row = f"{A_bin}\t{B_bin}\t{opcode_bin}\t{output_bin}"
                    f.write(row + "\n")
                    total_rows += 1
                    
    return total_rows

# --- Execution ---

file_name = "alu_complete_truth_table.txt"

# Generate the file
num_rows = generate_complete_truth_table(file_name)

print(f"✅ Complete truth table generated and saved to '{file_name}'.")
print(f"The file contains {num_rows} rows (all 2^12 = 4096 possible combinations).")
