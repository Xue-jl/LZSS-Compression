


### Z_algorithm version 1.0:
# 1. scatter case 1 and case 3 to avoid some repeated comparison in case 3, which optimise potential worst case O(NM) to O(N)
# 2. remove cursor variable to avoid duplicated code, i.e. Zk can replace cursor
# 3. fix base case from a cognitive conceptual errors: {pre-Z-box can cross Z-box} is correct comprehesion

import sys

# Assuming Index from 0
# Assuming Z[0] = 0
# General Z-box is [l, r]

def Z(str):
    Z_array = [0 for _ in range(len(str))]
    #### Base Case: n = 0 (define Z[0])
    r = 0
    l = 0


    #### Inductive Step: Assume n = 1..k-1 ok(Z1...Zk-1), n = k(calculate Zk)
    for k in range(1, len(str)):
        ## Case 1: Zk-box over Z-box(k > r)
        if k > r or (k <= r and k + Z_array[k-l] -1 >= r):
            # calculate Zk = comparing str[k...] with str[1...] until mismatch
            Zk = 0
            while k + Zk < len(str) and str[k + Zk] == str[0 + Zk]:
                Zk += 1
            Z_array[k] = Zk

            # get r and l from Zk
            if Zk > 0:   # update current Z-box to new further right Z-box
                r = k + Zk -1
                l = k


        ## Case 2a: Zk-box inside Z-box(k ≤ r and k + Zk -1 < r), which means can mapping
        elif k <= r and k + Z_array[k-l] -1 < r:
            Z_array[k] = Z_array[k-l]

        ## Case 2b: Zk-box cross Z-box(k > r and k + Zk – 1 ≥ r), which means partly mapping
        ##          from [k..r], so can skip r-k+1 comparisons
        elif k <= r and k + Z_array[k-l] -1 == r:  #has been proved cannot be > r.
            Zk = r - k + 1
            while k + Zk < len(str) and str[k + Zk] == str[0 + Zk]:
                Zk += 1
            r = k + Zk - 1  # no need to check Zk coz partly mapping
            l = k


    return Z_array

def Z_pattern_matching(pat, txt):
    str = pat + '$' + txt
    result = []
    Z_array = Z(str)
    #print(Z_array)
    for i in range(len(pat)+1, len(Z_array)):
        if Z_array[i] == len(pat):
            result.append(i-len(pat)-1)
    return result

