


#
# Elias Coding performs prefix-free(variable-length) encode/decode for integer stream
#

def elias_encoder(N:int):
    assert N > 0, "Cannot encode non-positive number!"
    if N == 1:
        return str(N)
    # 1. initialization, base case(binary rep for N)
    binary_N:str = BinaryRep(N)
    L:int = len(binary_N)-1
    encoded:str = binary_N

    # 2. repeated encode length component(L) until L = 1
    while L > 1:
        binary_L:str = BinaryRep(L)
        encoded = '0' + binary_L[1:] + encoded

        L = len(binary_L) - 1

    # 3. return elias code word for N
    return '0'+ encoded




def elias_decoder(code_word:str):
    '''
    Decode to a single integer
    :param code_word: '1000011' machine code
    :return:
    '''
    if code_word == '1':
        return int(code_word)
    # 1. start with 1st bit, which is always '0'
    binary_L:str = '1'   # binary rep of length component
    L:int = len(binary_L) + 1
    code_word = code_word[1:]

    # 2. repeated decode until meet '1' as the 1st bit, which means get the original binary rep of N
    while code_word != "" and code_word[0] == '0':
        # probe next L bits
        binary_L = '1' + code_word[1:L]
        # cut next L bits in elias code word
        code_word = code_word[L:]
        # binary Length-component  => decimal Length-component, update L
        L = DecimalRep(binary_L) + 1

    # 3. final decoded number comes from rest code_word which starts with bit '1'
    N = DecimalRep(code_word[:L])

    return N

def elias_seq_decoder(code_word:str):
    '''
    Decode to a sequence of integers
    :param code_word: '1000011' machine code
    :return:
    '''
    if code_word == '1':
        return [int(code_word)]

    Ns = []

    while code_word != "":
        # 1. start with 1st bit, which is always '0'
        binary_L: str = '1'  # binary rep of length component
        L: int = len(binary_L) + 1
        code_word = code_word[1:]
        # 2. repeated decode until meet '1' as the 1st bit, which means get the original binary rep of N
        while code_word != "" and code_word[0] == '0':
            # probe next L bits
            binary_L = '1' + code_word[1:L]
            # cut next L bits in elias code word
            code_word = code_word[L:]
            # binary Length-component  => decimal Length-component, update L
            L = DecimalRep(binary_L) + 1

        # 3. final decoded number comes from rest code_word which starts with bit '1'
        N = DecimalRep(code_word[:L])
        code_word = code_word[L:]
        Ns.append(N)

    return Ns



def BinaryRep(n:int):
    ret = ""
    while n > 0:
        ret = str(n % 2) + ret
        n //= 2
    return ret

def DecimalRep(b:str):  # b: the binary rep
    ret = 0  # ret: return decimal number
    base = 1  # base: the multiplicator for specific bit
    while b != "":
        ret += int(b[-1])*base
        base *= 2
        b = b[:-1]
    return ret

if __name__ == '__main__':
    print(elias_encoder(561))
    print(elias_seq_decoder("011000100"))
    print(elias_seq_decoder("011011"))

    # test encodes
    outfile = open("elias_code_word.txt", 'w')
    for i in range(100):
        outfile.write("{:3}    {}\n".format(i, elias_encoder(i)))

    outfile.close()

