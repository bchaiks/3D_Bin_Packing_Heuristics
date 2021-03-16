import numpy as np

##################################################################
#######   INPUT
##################################################################

# Maximum box dimensions
# need to make sure that dimensions are big enough to handle each piece...
H_box = 40
W_box = 60
D_box = 48


# pieces are (dimensions, label)
# dimensions are H x W x D
Pieces = [[[51.,36.,20.], 'Piece 1'],
		[[26.75, 48., 11.25], 'Piece 2'],
		[[29., 56., 23.],'Piece 3'],
		[[15., 30., 24.],'Piece 4'],
		[[15., 30, 24.],'Piece 5']]
	
for i in range(len(Pieces)):
	Pieces[i].append(i)


''' 
Rotations are achieved by
Permuting the dimensions and recording the 
rotations'''

# [0,1,2] -- no rotation 
# [0,2,1] -- 90 around height  
# [1,0,2] -- 90 around depth
# [1,2,0] -- 90 around width, then 90 around (new) depth
# [2,0,1] -- 90 around height, then 90 around (new) depth
# [2,1,0] -- 90 around width 

Ors = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]

# stores the rotation that FIXES the given plane
# i.e. rotXY rotates around the Z axis 
rotXY = {0: 0,
		1:  90,
		2:  0, 
		3:  0, 
		4:  90,
		5: 0, }
		
rotYZ = {0: 0,
		1: 0,
		2: 0,
		3: 90,
		4:  0,
		5: 90}

rotXZ = {0: 0,
		1: 0,
		2: 90,
		3: 90,
		4: 90,
		5: 0}



##################################################################
#######   Preliminary Functions
##################################################################

def order(x,vals):
	'''
	idea is to apply this to the pieces, with different
	vectors for vals depending on the ordering rule
	(probably start with non-increasing volume)
	'''
	x = [i for _,i in sorted(zip(vals,x), reverse = True)]
	return x

def re_order(dim, OR):
	'''
	dim stores original dimensions, OR is a permutation
	'''
	D = dim
	new_dim = []
	for i in range(3):
		new_dim.append(D[OR[i]])
	return new_dim

def Feas(Dims, EP, Bin_Size, OR, Curr_items, Curr_EP):
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
	BS = Bin_Size
	D = re_order(Dims,OR)
	CI = Curr_items
	CE = Curr_EP
	check = True
	for i in range(3):
		# Bin limits
		if D[i] + EP[i] > BS[i]:
			check = False

	for j in range(len(CI)):
		# checking intersections with other items

		####################################################
		#### DOUBLE CHECK THIS FOR CORRECTNESS!!!!
		####################################################
		for k in range(3):
			a = (k + 1)%3
			b = (k + 2)%3
			if overlap(D,EP,CI[j],CE[j],k,a,b):
				check = False
	return check

def overlap(d1,c1, d2,c2, k,x, y):
	'''
	returns True if two 3-d boxes with dimensions d1 d2
	and lower left corners c1, c2 overlap on the xy plane AND k dim...
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
'''
Compute Merit function for given placement of a piece
'''
def Merit_Res(Dims, OR, EP, Rs, Bin_Size):
	'''
	not gonna bother checking feasibility...
	assume that this calc comes AFTER feasibility check...

	--Maybe weight the dimensions differently to
	make the different orientations different?
	'''
	D = Dims
	BS = Bin_Size
	'''
	this does NOT take account of the orientation
	so the orientation is basically just for feasibility...
	'''
	# The "extra" EP[0] + Dims[0] is supposed to penalize "high" positions...
	return sum(Rs) - sum(Dims) + EP[0] + Dims[0]

#### Work with people to determine best/better merit functions.

#### CODE UP THE BOUNDING BOX ONES TOO!! THESE SEEM LIKELY
#### CANDIDATES FOR US...

def Merit_WD(Dims, OR, EP, curr_items, curr_eps):
	'''
	Selects position that minimizes the bounding 
	box in the WxD dimension
	
	curr_items = items in crate
	curr_eps = position of items 
	EP = candidate position 
	OR = candidate orientation
	'''
	Dim = re_order(Dims,OR)
	CI = curr_items
	CE = curr_eps
	''' 
	start out with the box bounds as the new guy
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

'''
Update Extreme point list
'''
def proj(d1,e1,d2,e2, ep_dir, proj_dir):
	'''
	d1, e1 -- dim of new piece, placed at point e1
	d2, e2 -- cycle these through the other pieces

	ep_dir is the coordinate "pushed out" by the piece dimension in
	the candidate extreme point
	proj_dir is the one to shrink... (number 0,1,2 corresponding to x, y, z)
	These are NEVER the same...
	'''
	e = ep_dir
	pd = proj_dir
	# remaining dimension???
	od = 3-e - pd
	eps = 0.0
	check = True

	if d2[pd] + e2[pd] > e1[pd] - eps:
		#i.e. piece is further from axis in projection direction
		check = False
	if e2[e] > e1[e] + d1[e] - eps:
		#i.e. piece too far
		check = False
	if e2[e] + d2[e] < e1[e] + d1[e] + eps:
		# i.e. piece not far enough
		check = False
	if  e2[od] > e1[od] - eps:
		#i.e. piece too far
		check = False
	if e2[od] + d2[od] < e1[od] + eps:
		# i.e. piece not far enough
		check = False
	return check

def Update_EP(Dims, EP, Curr_EPs, Curr_Items):
	'''
	Dims = 1x3 HxWxD of current piece placed
		(in orienation OR* decided by Feas and Merit...)
	EP = 1x3 coordinates of lower left corner of current piece
	Curr_EPs = list of current extreme points where Curr_Items
		are located
	Curr_Items = list of dimensions of current items

	idea is you take current EP and push it out in the
	three dimensions of the current piece, then project
	each of these towards the two other axes...

	e.g. [ep[0],ep[1] + Dims[1], ep[2]] projected in
	x and z directions...

	- Six possible new ones (possibly duplicated...)
	- each of the three
	New_Eps[0], [1] are x_y and x_z projections of (ep[0]+dim[0],ep[1],ep[2])
	by shrinking the y and z coordinates, respectively...
	'''
	D = Dims
	CI = Curr_Items
	CE = Curr_EPs
	New_Eps = [[EP[0]+D[0],EP[1],EP[2]],[EP[0]+D[0],EP[1],EP[2]],
				[EP[0],EP[1]+D[1],EP[2]],[EP[0],EP[1]+D[1],EP[2]],
				[EP[0],EP[1],EP[2]+D[2]],[EP[0],EP[1],EP[2]+D[2]]]

	Max_bounds = -1*np.ones(6)

	for i in range(len(CI)):
		# x_y -- New_Eps[0] shrinking y coordinate
		if proj(D, EP, CI[i], CE[i],0,1) and CE[i][1] + CI[i][1] > Max_bounds[0]:
			New_Eps[0] = [EP[0] + D[0], CE[i][1] + CI[i][1],EP[2]]
			Max_bounds[0] = CE[i][1] + CI[i][1]

		#x_z -- New_Eps[1] shrinking z coordinate
		if proj(D, EP, CI[i], CE[i],0,2) and CE[i][2] + CI[i][2] > Max_bounds[1]:
			New_Eps[1] = [EP[0] + D[0], EP[1], CE[i][2] + CI[i][2]]
			Max_bounds[1] = CE[i][2] + CI[i][2]

		# y_x -- New_Eps[2] shrinking x coordinate
		if proj(D, EP, CI[i], CE[i],1,0) and CE[i][0] + CI[i][0] > Max_bounds[2]:
			New_Eps[2] = [CE[i][0] + CI[i][0], EP[1] + D[1],EP[2]]
			Max_bounds[2] = CE[i][0] + CI[i][0]

		#y_z -- New_Eps[3] shrinking z coordinate
		if proj(D, EP, CI[i], CE[i],1,2) and CE[i][2] + CI[i][2] > Max_bounds[3]:
			New_Eps[3] = [EP[0], EP[1]+D[1], CE[i][2] + CI[i][2]]
			Max_bounds[3] = CE[i][2] + CI[i][2]

		# z_x -- New_Eps[4] shrinking x coordinate
		if proj(D, EP, CI[i], CE[i],2,0) and CE[i][0] + CI[i][0] > Max_bounds[2]:
			New_Eps[2] = [CE[i][0] + CI[i][0], EP[1],EP[2] + D[2]]
			Max_bounds[2] = CE[i][0] + CI[i][0]

		# z_y -- New_Eps[5] shrinking y coordinate
		if proj(D, EP, CI[i], CE[i],2,1) and CE[i][1] + CI[i][1] > Max_bounds[0]:
			New_Eps[0] = [EP[0], CE[i][1] + CI[i][1],EP[2] + D[2]]
			Max_bounds[0] = CE[i][1] + CI[i][1]
	# remove duplicates
	
	
	New_Eps = np.unique(New_Eps, axis = 0)
	return New_Eps



##################################################################
#######  Full Packing Stage
##################################################################

#### pieces_to_pack is THE SAME as from the nesting stage...
#### with all the nested pieces removed (whole nested ensemble
#### treated as one...)

#### Instantiate first Crate with first EP at [0,0,0]...

# can be different for each one... in principle...
Bin_size = [H_box,W_box,D_box]

# List of open EP's in open Crates
Cr = [[[0,0,0]]]
## when create a new crate, give it one of the size bounds
## from Crate_Dims and initialize the Crate_RS_Lists with these

## Stores Residuals for each EP in each Crate (ORDERING HAS TO BE THE SAME)
Cr_RS = [[Bin_size]]

# Stores a list of the dimensions of items currently in each crate
Cr_Item=[[]]

# Stores a list of the EPs where the current items
# were placed -- need this to compute intersections
Cr_EPs =[[]]



ptp = Pieces

## List of the locations and orientations of packed pieces
Packings = []

for p in range(len(ptp)):
	'''
	try the piece in EACH existing crate, pick best spot
	according to the merit function.
	If NO possible packing THEN Crates.append([[0,0,0]]) and
	pack it in this one...

	For bounding box merit function, maybe also start a new
	crate if the BEST Merit value is too bad...
	'''
	# update this with the crate it's packed in...
	packed_in = None
	Dims = ptp[p][0]

	Best_Merit = 2 * H_box * W_box * D_box
	e_cand = None
	o_cand = None

	for c in range(len(Cr)):

		EPL = Cr[c]
		Curr_Items = Cr_Item[c]
		Curr_EP = Cr_EPs[c]
		Ordered_EPL = []

		for e in range(len(EPL)):
			for o in range(len(Ors)):
				if Feas(Dims, EPL[e], Bin_size, Ors[o], Curr_Items, Curr_EP) and Merit_WD(Dims, Ors[o], EPL[e], Curr_Items, Curr_EP) < Best_Merit:
					#Best_Merit = Merit_Res(Dims, Ors[o], EPL[e], RS_List[e], Bin_size)
					Best_Merit = Merit_WD(Dims, Ors[o], EPL[e], Curr_Items, Curr_EP)
					e_cand = e
					o_cand = o
					packed_in = c

	if packed_in is not None:

		k = packed_in
		EPL = Cr[k]
		Curr_Items = Cr_Item[k]
		#Curr_EP = Cr_EPs[k]


		Dims = re_order(Dims, Ors[o_cand])
		NE = Update_EP(Dims, EPL[e_cand], Curr_EP, Curr_Items)

		## before had this appending the ORIGINAL orientation
		Cr_Item[k].append(Dims)
		Cr_EPs[k].append(EPL[e_cand])
		L = len(Cr_EPs[k])

		del EPL[e_cand]

		for i in range(len(NE)):
			EPL.append(NE[i])

		# Sort the EPs by lowest z, y, x respectively...
		# might want to change this, depending on how things go...

		for i in range(3):
			# the [2-i] means it sorts the 0 index last -- i.e. really ordered
			# by smallest height... wherever height is in the list...
			order_i = [np.argsort(EPL,0)[r][2-i] for r in range(len(EPL))]

			#### Seems to be ok to do this in place like this...

			EPL = [EPL[order_i[j]] for j in range(len(order_i))]

		'''
		WILL NEED TO CHANGE THIS so that it returns the format that Kyle wants
		need to make a dictionary mapping the orientation chosen in the loop
		to the relevant orientation in the "XY 90 degree" language...
		'''

		Result = [ptp[p][2],{'name': ptp[p][1], 'rotationXY': rotXY[o_cand], 'rotationYZ': rotYZ[o_cand], 'rotationXZ': rotXZ[o_cand],'bottomLeftX':Cr_EPs[k][L-1][1], 'bottomLeftY': Cr_EPs[k][L-1][2], 'bottomLeftZ': Cr_EPs[k][L-1][0], 'crate': packed_in}]
		#orientation HxWxD = {Dims}, bottom left at {Cr_EPs[k][L-1]} in Crate {packed_in}.
		Packings.append(Result)

		Cr[k] = EPL
		#Cr_Item[k] = Curr_Items
		#Cr_EPs[k] = Curr_EP

	if packed_in is None:
		Cr.append([[0,0,0]])
		Cr_Item.append([])
		Cr_EPs.append([])

		c = len(Cr)-1
		packed_in = c
		EPL = Cr[c]
		Curr_Items = Cr_Item[c]
		Curr_EP = Cr_EPs[c]
		e_cand = 0
		o_cand = None
		
		for o in range(len(Ors)):
			if  Feas(Dims, EPL[e_cand], Bin_size, Ors[o], Curr_Items, Curr_EP) and Merit_WD(Dims, Ors[o], EPL[e_cand], Curr_Items, Curr_EP) < Best_Merit:
				#Best_Merit = Merit_Res(Dims, Ors[o], EPL[e_cand], RS_List[e_cand], Bin_size)
				Best_Merit = Merit_WD(Dims, Ors[o], EPL[e_cand], Curr_Items, Curr_EP) < Best_Merit
				o_cand = o

		Dims = re_order(Dims, Ors[o_cand])
		NE = Update_EP(Dims, EPL[e_cand], Curr_EP, Curr_Items)

		## same thing, was adding the ORIGNINAL Orientation before...
		Curr_Items.append(Dims)
		Curr_EP.append(EPL[e_cand])
		L = len(Curr_EP)

		del EPL[e_cand]

		for i in range(len(NE)):
			EPL.append(NE[i])
			# Sort the EPs by lowest height, width, and depth respectively...
			# might want to change this, depending on how things go...
		for i in range(3):
			order_i = [np.argsort(EPL,0)[r][2-i] for r in range(len(EPL))]
			EPL = [EPL[order_i[j]] for j in range(len(order_i))]


		Result = [ptp[p][2],{'name': ptp[p][1], 'rotationXY': rotXY[o_cand], 'rotationYZ': rotYZ[o_cand], 'rotationXZ': rotXZ[o_cand],'bottomLeftX': Cr_EPs[k][L-1][1], 'bottomLeftY': Cr_EPs[k][L-1][2], 'bottomLeftZ': Cr_EPs[k][L-1][0], 'crate': packed_in}]
		Packings.append(Result)
		Cr[c] = EPL
		Cr_Item[c] = Curr_Items
		Cr_EPs[c] = Curr_EP


################################################################################
######## Generate dimensions of crates
################################################################################


'''
X - width
Y - Depth
Z - Height
(Z,X,Y)
'''
Crate_dims = []
orientations = []

for i in range(len(Cr_Item)):

	H_dim = max([Cr_Item[i][j][0] + Cr_EPs[i][j][0] for j in range(len(Cr_Item[i]))])
	W_dim = max([Cr_Item[i][j][1] + Cr_EPs[i][j][1] for j in range(len(Cr_Item[i]))])
	D_dim = max([Cr_Item[i][j][2] + Cr_EPs[i][j][2] for j in range(len(Cr_Item[i]))])
	Crate_dims.append([H_dim, W_dim, D_dim])


for i in range(len(Pieces)):
	for j in range(len(Packings)):
		if Packings[j][0] == i:
			print(Packings[j][1])
			orientations.append(Packings[j][1])
			
