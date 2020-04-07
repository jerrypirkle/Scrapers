#!/usr/bin/env python3
"""
Sort List to find unique combinations
"""

# Function which returns subset or r length from n
from itertools import combinations

def rSubset(arr, r):

    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))

# Driver Function
if __name__ == "__main__":
    arr = ["Allusol","Breshos","Broc","Cantac","Fala","Fin","Foisso","Gonu","Gustuc","Higoh","Jotha","Lidamuuh","Ligebur","Lond","Mund","Nieth","Peospa","Scon","Shube","Tathath","Truukar","Unte","Vas","Woiloth","Yeoth"]
    r = 2
    print(rSubset(arr, r))
