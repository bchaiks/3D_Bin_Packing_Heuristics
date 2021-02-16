from Nest import Nest

""" object that stores all info about each piece """

class Piece:
    
    def __init__(self, positionInInputList,
                        # maybe all of this is just in PieceInfo???
                        name, 
                        dimensions, 
                        weight,  
                        allowableOrientations
                        canStack, 
                        canBeStackedOn,
                        nests):

        self.Dim = dimensions
        self.Weight = weight
        self.Volume = self.Dim[0]*self.Dim[1]*self.Dim[2]
        self.Label = name
        self.Index = positionInInputList
        self.Orientations = allowableOrientations # list of allowed orientations...
        self.Stack = canStack
        self.StackOn = canBeStackedOn

        # will hold the possible nests (nest objects) within the piece, 
        # once the piece gets placed, these will be given the correct locations
        # by the function PositionNests
        self.Nest = nests
        self.CrateIndex = None
        # extreme point in the crate
		self.Position = None
        self.Orienation = [0,1,2] # starts in unrotated orientation

        # index of extreme point (for updatingt the list in the algorithm)
		self.ExtremePointIndex = None

        # The position using the 
        self.Location = None
        

    def PositionNests(self):
        """ IF the piece can have stuff nested in it, 
        open some 'Nest' objects within the corresponding crate, 
        and at the appropriate location"""

        if self.CrateIndex == None:
            return "This operation must occur after placing the piece."
        
        for nest in self.nests:
            nest.ExtremePoints[0] = "eggs"

        # THEN ADD THE NESTS TO THE LIST OF OPEN CRATES...

    def FormatOutput(self):
        self.Location = "eggs"
    
    def Rotate(self, rotation):
        
        return([self.Dim[i] for i in rotation])
