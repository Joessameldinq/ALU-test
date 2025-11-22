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

def detect_carry(result, width=4):
    """Detects if a carry occurred (result exceeds width bits)."""
    return 1 if result > ((1 << width) - 1) else 0

def detect_overflow_add(A_signed, B_signed, result_signed, width=4):
    """Detects overflow in addition (two's complement)."""
    # Overflow occurs when:
    # - Both operands have same sign AND result has different sign
    if (A_signed >= 0 and B_signed >= 0 and result_signed < 0):
        return 1
    if (A_signed < 0 and B_signed < 0 and result_signed >= 0):
        return 1
    return 0

def detect_overflow_sub(A_signed, B_signed, result_signed, width=4):
    """Detects overflow in subtraction (two's complement)."""
    # Overflow in A - B occurs when:
    # - A is positive and B is negative but result is negative
    # - A is negative and B is positive but result is positive
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
        
        # Flags
        result_signed = to_signed_int(result_bin, BITS)
        Carry = detect_carry(unsigned_res, BITS)
        Overflow_flag = detect_overflow_add(A_signed, B_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
        
    elif opcode_bin == '0001':  # SUBTRACT: A - B
        # For unsigned: if A < B, there's a borrow
        if A_unsigned < B_unsigned:
            unsigned_res = A_unsigned - B_unsigned + (1 << BITS)
            Carry = 1
        else:
            unsigned_res = A_unsigned - B_unsigned
            Carry = 0
        
        result_val = unsigned_res & MAX_UNSIGNED
        result_bin = bin(result_val)[2:].zfill(BITS)
        
        # Overflow detection for signed subtraction (A - B)
        result_signed = to_signed_int(result_bin, BITS)
        Overflow_flag = detect_overflow_sub(A_signed, B_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
        
    elif opcode_bin == '0010':  # SUBTRACT: B - A
        # For unsigned: if B < A, there's a borrow
        if B_unsigned < A_unsigned:
            unsigned_res = B_unsigned - A_unsigned + (1 << BITS)
            Carry = 1
        else:
            unsigned_res = B_unsigned - A_unsigned
            Carry = 0
        
        result_val = unsigned_res & MAX_UNSIGNED
        result_bin = bin(result_val)[2:].zfill(BITS)
        
        # Overflow detection for signed subtraction (B - A)
        result_signed = to_signed_int(result_bin, BITS)
        Overflow_flag = detect_overflow_sub(B_signed, A_signed, result_signed, BITS)
        Zero_flag = detect_zero_flag(result_bin)
        
    elif opcode_bin == '0011':  # MULTIPLY: A * B
        product = A_signed * B_signed
        result_bin = to_twos_complement_bin(product, BITS)
        
        # Check for overflow in multiplication
        result_signed = to_signed_int(result_bin, BITS)
        if product != result_signed:
            Overflow_flag = 1
        
        Zero_flag = detect_zero_flag(result_bin)
        # Carry is typically not used for multiplication
        Carry = 0
    
    return result_bin, Zero_flag, Carry, Overflow_flag

def generate_arithmetic_truth_table(filename="alu_arithmetic_truth_table.txt"):
    """
    Generates truth table for arithmetic operations (0000-0011) with flags.
    Output format matches the reference file provided.
    """
    
    total_rows = 0
    
    with open(filename, 'w') as f:
        # Write header - matching the reference format exactly
        header = "A[4]\tB[4]\tC[4]\tOutput[4]\tZero_flag\tCarry\tOverflow_flag"
        f.write(header + "\n")
        
        # Iterate A from 0000 to 1111 (0 to 15)
        for A_val in range(16):
            A_bin = bin(A_val)[2:].zfill(4)
            
            # Iterate B from 0000 to 1111 (0 to 15)
            for B_val in range(16):
                B_bin = bin(B_val)[2:].zfill(4)
                
                # Only iterate through arithmetic opcodes (0000-0011)
                for opcode_val in range(4):
                    opcode_bin = bin(opcode_val)[2:].zfill(4)
                    
                    output_bin, zero_flag, carry_flag, overflow_flag = alu_arithmetic_4bit(
                        A_bin, B_bin, opcode_bin
                    )
                    
                    # Format row with tabs - matching reference format
                    row = f"{A_bin}\t{B_bin}\t{opcode_bin}\t{output_bin}\t{zero_flag}\t{carry_flag}\t{overflow_flag}"
                    f.write(row + "\n")
                    total_rows += 1
    
    return total_rows

# --- Execution ---

file_name = "alu_arithmetic_truth_table.txt"

# Generate the file
num_rows = generate_arithmetic_truth_table(file_name)

print(f"✅ Arithmetic truth table generated and saved to '{file_name}'.")
print(f"The file contains {num_rows} rows (all 4 operations × 16×16 combinations = 1024 rows).")
print(f"\nOperations included:")
print(f"  0000 - ADD (A + B)")
print(f"  0001 - SUBTRACT (A - B)")
print(f"  0010 - SUBTRACT (B - A)")
print(f"  0011 - MULTIPLY (A × B)")
print(f"\nFlags included: Zero_flag, Carry, Overflow_flag")
