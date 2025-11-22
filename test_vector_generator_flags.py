import os

# --- Helper Functions ---

def to_signed_int(bits, width=4):
    """Converts a binary string (two's complement) to a signed integer."""
    decimal_val = int(bits, 2)
    if bits[0] == '1':
        return decimal_val - (1 << width)
    return decimal_val

def to_twos_complement_bin(val, width=4):
    """Converts a signed integer to a two's complement binary string."""
    mask = (1 << width) - 1
    return bin(val & mask)[2:].zfill(width)

def detect_carry_add(result, width=4):
    """Detects if a carry occurred in addition."""
    return 1 if result > ((1 << width) - 1) else 0

def detect_overflow_add(A_signed, B_signed, result_signed, width=4):
    """Detects overflow in addition (two's complement)."""
    if (A_signed >= 0 and B_signed >= 0 and result_signed < 0):
        return 1
    if (A_signed < 0 and B_signed < 0 and result_signed >= 0):
        return 1
    return 0

def detect_overflow_sub(A_signed, B_signed, result_signed, width=4):
    """Detects overflow in subtraction (two's complement)."""
    if (A_signed >= 0 and B_signed < 0 and result_signed < 0):
        return 1
    if (A_signed < 0 and B_signed >= 0 and result_signed >= 0):
        return 1
    return 0

def detect_zero_flag(result_bin):
    """Detects if result is zero."""
    return 1 if result_bin == '0000' else 0

# --- ALU Arithmetic Operations ---

def alu_arithmetic_4bit(A_bin, B_bin, opcode_bin):
    """
    Simulates the 4-bit ALU arithmetic operations (0000-0011) 
    and returns result with flags (Zero_flag, Carry, Overflow_flag).
    """
    
    BITS = 4
    MAX_UNSIGNED = (1 << BITS) - 1
    
    A_signed = to_signed_int(A_bin, BITS)
    B_signed = to_signed_int(B_bin, BITS)
    A_unsigned = int(A_bin, 2)
    B_unsigned = int(B_bin, 2)
    
    Zero_flag = 0
    Carry = 0
    Overflow_flag = 0
    result_bin = '0000'
    
    if opcode_bin == '0000':  # ADD: A + B
        unsigned_res = A_unsigned + B_unsigned
        result_val = unsigned_res & MAX_UNSIGNED
        result_bin = bin(result_val)[2:].zfill(BITS)
        
        # Flags for ADD
        result_signed = to_signed_int(result_bin, BITS)
        Carry = detect_carry_add(unsigned_res, BITS)
        Overflow_flag = detect_overflow_add(A_signed, B_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
        
    elif opcode_bin == '0001':  # SUBTRACT: A - B
        unsigned_res = A_unsigned - B_unsigned
        if unsigned_res < 0:
            result_val = (unsigned_res + (1 << BITS)) & MAX_UNSIGNED
            Carry = 1
        else:
            result_val = unsigned_res & MAX_UNSIGNED
            Carry = 0
        
        result_bin = bin(result_val)[2:].zfill(BITS)
        result_signed = to_signed_int(result_bin, BITS)
        Overflow_flag = detect_overflow_sub(A_signed, B_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
        
    elif opcode_bin == '0010':  # SUBTRACT: B - A
        unsigned_res = B_unsigned - A_unsigned
        if unsigned_res < 0:
            result_val = (unsigned_res + (1 << BITS)) & MAX_UNSIGNED
            Carry = 1
        else:
            result_val = unsigned_res & MAX_UNSIGNED
            Carry = 0
        
        result_bin = bin(result_val)[2:].zfill(BITS)
        result_signed = to_signed_int(result_bin, BITS)
        Overflow_flag = detect_overflow_sub(B_signed, A_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
    
    return result_bin, Zero_flag, Carry, Overflow_flag

def generate_arithmetic_truth_table(filename="alu_arithmetic_truth_table.txt"):
    """
    Generates truth table for arithmetic operations (0000-0010) with flags.
    Output format matches the reference file provided.
    """
    
    total_rows = 0
    
    with open(filename, 'w') as f:
        # Write header
        header = "A[4]\tB[4]\tC[4]\tOutput[4]\tZero_flag\tCarry\tOverflow_flag"
        f.write(header + "\n")
        
        # Iterate A from 0000 to 1111 (0 to 15)
        for A_val in range(16):
            A_bin = bin(A_val)[2:].zfill(4)
            
            # Iterate B from 0000 to 1111 (0 to 15)
            for B_val in range(16):
                B_bin = bin(B_val)[2:].zfill(4)
                
                # Only iterate through arithmetic opcodes (0000-0010) as in reference
                for opcode_val in range(3):
                    opcode_bin = bin(opcode_val)[2:].zfill(4)
                    
                    output_bin, zero_flag, carry_flag, overflow_flag = alu_arithmetic_4bit(
                        A_bin, B_bin, opcode_bin
                    )
                    
                    # Format row with tabs
                    row = f"{A_bin}\t{B_bin}\t{opcode_bin}\t{output_bin}\t{zero_flag}\t{carry_flag}\t{overflow_flag}"
                    f.write(row + "\n")
                    total_rows += 1
    
    return total_rows

# --- Execution ---

file_name = "alu_arithmetic_truth_table.txt"

# Generate the file
num_rows = generate_arithmetic_truth_table(file_name)

print(f"✅ Arithmetic truth table generated and saved to '{file_name}'.")
print(f"The file contains {num_rows} rows (3 operations × 16×16 combinations = 768 rows).")
print(f"\nOperations included:")
print(f"  0000 - ADD (A + B)")
print(f"  0001 - SUBTRACT (A - B)")
print(f"  0010 - SUBTRACT (B - A)")
print(f"\nFlags included: Zero_flag, Carry, Overflow_flag")
