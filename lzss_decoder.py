

from Elias_Coding import *
import sys

def LZSS_decoder(file):


    # 1. preparation
    binary_code = open(file, 'r').readline().strip('\n')
    binary_code = [binary_code]   # make binary_code a pointer


    # 2. Intermediate stage： LZSS decode to tuple/triples
    decoded = []
    while binary_code[0] != "":
        format = binary_code[0][0]
        binary_code[0] = binary_code[0][1:]
        if format == '0':     # triple => Elias decoding
            decoded_cache = lzss_elias_seq_decoder(binary_code)
            decoded.append((0, decoded_cache[0], decoded_cache[1]))
        elif format == '1':   # tuple => ASCII decoding
            decoded.append((1, chr(DecimalRep(binary_code[0][:8]))))
            binary_code[0] = binary_code[0][8:]
    # return decoded


    # 3. Final stage: decode to string
    decoded_str = ""
    for tuple in decoded:
        if len(tuple) == 2:
            decoded_str += tuple[1]
        elif len(tuple) == 3:
            offset = tuple[1]
            length = tuple[2]
            cache = ""
            while offset <= length:
                cache += decoded_str[-offset:]
                length -= offset
            decoded_str += (cache + decoded_str[-offset:-offset+length])
            # print(decoded_str, cache)

    outfile = open("output_lzss_decoder.txt", 'w')
    outfile.write(decoded_str)
    outfile.close()

    return decoded_str


def lzss_elias_seq_decoder(code_word):

    Ns = []
    elias_codeword_count = 0
    while code_word[0] != "" and elias_codeword_count < 2:
        # 1. start with 1st bit, which is always '0'
        binary_L: str = '1'  # binary rep of length component
        L: int = len(binary_L) + 1
        code_word[0] = code_word[0][1:]
        # 2. repeated decode until meet '1' as the 1st bit, which means get the original binary rep of N
        while code_word[0] != "" and code_word[0][0] == '0':
            # probe next L bits
            binary_L = '1' + code_word[0][1:L]
            # cut next L bits in elias code word
            code_word[0] = code_word[0][L:]
            # binary Length-component  => decimal Length-component, update L
            L = DecimalRep(binary_L) + 1

        # 3. final decoded number comes from rest code_word[0] which starts with bit '1'
        N = DecimalRep(code_word[0][:L])
        code_word[0] = code_word[0][L:]
        Ns.append(N)
        elias_codeword_count += 1

    return Ns


if __name__ == '__main__':
    LZSS_decoder(sys.argv[1])
