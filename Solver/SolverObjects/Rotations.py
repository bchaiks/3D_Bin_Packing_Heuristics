from collections import OrderedDict

""" class storing the allowable rotations (for each piece?) """

class Rotations:

    Permutations = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
    XY = OrderedDict(sorted([
        (0, 0),
        (1, 90),
        (2, 0),
        (3, 0),
        (4, 90),
        (5, 0)])
    YZ = OrderedDict(sorted([
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 90),
        (4, 0),
        (5, 90)])
    XZ = OrderedDict(sorted([
        (0, 0),
        (1, 0),
        (2, 90),
        (3, 90),
        (4, 90),
        (5, 0)])

# for reference...
    # [0,1,2] -- no rotation
    # [0,2,1] -- 90 around height --
    # [1,0,2] -- 90 around depth
    # [1,2,0] -- 90 around width, then 90 around (new) depth
    # 012 --> 021 (width) --> 120 (depth)
    # [2,0,1] -- 90 around height, then 90 around (new) depth
    # 012 --> 021 (height) --> 201 (depth)
    # [2,1,0] -- 90 around width