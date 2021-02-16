import json
from collections import OrderedDict
from Solver.Solution import Solution

""" Interface to the crate-packing solver """

def Pack(inputData, maxCrateSize):
    inputPieces = inputData.get_json()['furniture']
    return(Solution(inputPieces, maxCrateSize))
