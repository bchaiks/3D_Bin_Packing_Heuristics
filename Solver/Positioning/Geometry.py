
""" functions for determining if a piece is feasible at an extreme point"""

def Feasible(newPiece, candidatePosition, candidateOrientation, currentCrate):
    '''
    Returns True if the orientation OR of a piece of dimension
    Dims = HxWxD is feasible in a bin with leftmost corner at EP

    Bin_Size = 1x3 dimensions of bin
    Dims = 1x3
    EP = 1x3 -- coordinates of the chosen spot
    OR = 1x3 a permutation of [0,1,2]
    For all items in Curr_items placed at Curr_Ep
    have to make sure that EP[0] + d[OR[0]] doesn't
    poke through... item[j][0] -- item[j][0] + Curr_Ep[j][0]
    '''
    BS = currentCrate.Bounds
    D = newPiece.Rotate(candidateOrientation)
    CI = currentCrate.Pieces
    EP = candidatePosition

    check = True
    for i in range(3):
        # Bin limits
        if D[i] + EP[i] > BS[i]:
            check = False

    for j in range(len(CI)):
        # checking intersections with other items

        for k in range(3):
            a = (k + 1)%3
            b = (k + 2)%3
            if overlap(D, EP, CI[j], CI[j].Position, k,a,b):
                check = False
    return check

def overlap(d1,c1, d2,c2, k,x, y):
    '''
    returns True if two 3D boxes with dimensions d1, d2
    and lower left corners c1, c2 overlap on the xy plane AND in the k dim...
    '''
    ov = True
    if c1[x] >= c2[x] + d2[x]:
        ov = False
    if c2[x] >= c1[x] + d1[x]:
        ov = False
    if c1[y] >= c2[y] + d2[y]:
        ov = False
    if c2[y] >= c1[y]+d2[y]:
        ov = False
    if c1[k] >= c2[k] + d2[k]:
        ov = False
    if c2[k] >= c1[k] + d1[k]:
        ov = False
    return ov