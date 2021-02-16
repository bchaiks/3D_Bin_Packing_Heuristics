
""" object to store the crate info """


class Crate:
    def __init__(self, bounds, index):
        self.Bounds = bounds
        self.Index = index
    
        # will update this to keep track of the size 
        # as items get added
        self.Dims = [0.0,0.0,0.0]
       
        # list of pieces in this crate
        self.Pieces = []
        
        self.ExtremePoints = [[0.0,0.0,0.0]]
    
    def XY_Box(self):
        # bounding box in the XY plane, for some positioning logic
        return(self.Dims[0] * self.Dims[1])
    def Volume(self):
        return (self.Dims[0]*self.Dims[1]*self.Dims[2])
    def Weight(self):
        return (sum(piece.Weight for piece in self.pieces))

    