from SolverObjects.Parameters import Parameters
from Formatting import *
from collections import OrderedDict

"""function that returns the formatted list of pieces arranged in crates """

def Solution(inputPieces, maxCrateSize, options = False):
	# options could signal the "randomized b&b" for instance...
	problemParameters = Parameters(maxCrateSize)
	Pieces= []
	Crates = []	
	unsortedPieces = FormattedInput(inputPieces)
	
	if options:
		# do something else
		return("this functionality hasn't been configured yet.")
	else:
        # or some other sorting??
		Pieces = sorted(unsortedPieces, key=lambda piece: piece.Volume, reverse = True) 
		
	Solve(Parts, Crates, problemParameters)
		
	return(FormattedOutput(Parts, Crates, problemParameters))