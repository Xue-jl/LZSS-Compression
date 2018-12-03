

# LZSS version 2.0
# every time encoded a tuple/triple, don't return a next char tuple (except for length = 0)

#
# Lempel Ziv SS is a <sliding window> based algorithm
# Applied for compress file => triples(context level) => binary bits(machine level)
#

# Assuming the Sliding Window size is 10.
# size(dictionary) = 6. size(Lookup Buffer) = 4

from Elias_Coding import *
from Z_algorithm import *
import sys

def LZSS_encoder(file, dic_size, buf_size):
    text = open(file, 'r').readline().strip('\n')
    DICTIONARY_SIZE = int(dic_size)
    BUFFER_SIZE = int(buf_size)

    # 1. initialization
    dictionary = ""
    buffer = text[:BUFFER_SIZE]
    cursor = 0   # the index of current cursor in the whole string
    encoded = []



    # 2. encode triples
    while cursor < len(text):
        encoded_cache = get_encoded_tuple(dictionary, buffer, cursor, text)
        encoded += encoded_cache[0]

        # update dictionary && buffer
        cursor += (encoded_cache[1] + (1 if encoded_cache[1] == 0 else 0))
        dictionary = text[(cursor-DICTIONARY_SIZE):cursor] if cursor>=DICTIONARY_SIZE else text[:cursor]
        buffer = text[cursor:cursor+BUFFER_SIZE]

    #return encoded
    # 3. machine(binary) code output
    binary_encoded = ""
    for tuple in encoded:
        binary_encoded += str(tuple[0])
        if len(tuple) == 2:
            binary_encoded += ('0' + BinaryRep(ord(tuple[1])))
        elif len(tuple) == 3:
            binary_encoded += (elias_encoder(tuple[1]) + elias_encoder(tuple[2]))


    outfile = open("output_lzss_encoder.txt", 'w')
    outfile.write(binary_encoded)
    outfile.close()

    return binary_encoded






def get_encoded_tuple(dic, buf, cursor, text):
    """
    Finds the longest substring in dictionary(search window) that
    matches the prefix of buffer(lookahead buffer)
    Output: encoded tuple
    """
    length = 0
    offset = 0
    # print(dic, buf)
    if dic == "": return [[(1, buf[0])], 0]
    for i in range(1, len(dic)+1):

        # construct Z_array based on new extended dic chunk
        window = dic[-i:] + buf
        Z_array = Z(window)
        # print(Z_array[:i], Z_array[i:])

        # probe for any longer match length
        for j in range(i, len(Z_array)):
            if Z_array[i] > length:    # i： cursor'sposition
                length = Z_array[i]
                offset = j

    # LZSS solution: length check ~ 3
    ret = []
    if length >= 3:   # return a triple <format 0, offset, length) and a tuple <format 1, char>
        ret.append((0, offset, length))
    elif length == 2:             # return three tuple <format 1, char>
        ret += [(1, buf[0]), (1, buf[1])]
    elif length < 2:        # return two tuple
        ret.append((1, buf[0]))



    return (ret, length)





if __name__ == '__main__':
    LZSS_encoder(sys.argv[1], sys.argv[2], sys.argv[3])




