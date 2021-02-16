from collections import OrderedDict
from SolverObjects.Piece import Piece
import json


''' functions for formatting inputs and outputs '''


def FormattedInput(inputPieces):
	
    PieceObjects = []
	
	for i in range(len(inputPieces)):
		PieceObjects.append(Piece(i, inputPieces[i]))
		
	return(PieceObjects)	
	
	
def FormattedOutput(reOrderedPieces, Crates, parameters):
	
	originalPieceOrder = sorted(reOrderedPieces, key=lambda piece: piece.Index)
	
	pieceOutput = [Piece.FormatOutput(parameters) for Piece in originalPieceOrder]
	crateOutput = [Sheet.Coordinates for Sheet in sheetObjects]
	
	partsAndSheets = OrderedDict([('parts',partOutput),('sheets',sheetOutput)])
	formattedOutput = OrderedDict([("results",partsAndSheets)])
	return(json.dumps(formattedOutput))