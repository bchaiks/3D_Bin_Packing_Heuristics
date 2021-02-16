
''' 
A nest is a space that behaves like a crate, but is 
inside another piece.  As such, its dimensions are 
totally fixed from the beginning. 
'''

class Nest:
    def __init__(self, dimension, startingExtremePoint):
        # will rearrange this using the Same orientation 
        # as the piece...
        self.Dim = dimension
        # starting extreme point is the location of the lower left corner of 
        # the nest given the ORIGINAL piece orientation, this has to get updated...
        self.ExtremePoints = [startingExtremePoint]