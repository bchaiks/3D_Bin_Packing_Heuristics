

""" functions for assessing merit of a given feasible position """


def Merit_WD(newPiece, OR, EP, crate):
        '''
        Selects position that minimizes the bounding 
        box in the WxD dimension
        
        crate = crate with some pieces already placed
        EP = candidate position 
        OR = candidate orientation
        '''
        Dim = newPiece.Rotate(OR)
        CI = crate.Pieces
        CE = [piece.Position for piece in CI]
        ''' 
        start out with the box bounds as bounding box (this is the biggest it'll ever be...)

        MIGHT want to make it more square? or something... or penalize volume/weight
        '''
        W = EP[1] + Dim[1]
        D =  EP[2] + Dim[2]
        for i in range(len(CI)):
            if CE[i][1] + CI[i][1] > W:
                W = CE[i][1] + CI[i][1]
            if CE[i][2] + CI[i][2] > D:
                D = CE[i][2] + CI[i][2]
        #Penalizes Height
        val = W*D + (EP[0] + Dim[0]) * W
        return(val)