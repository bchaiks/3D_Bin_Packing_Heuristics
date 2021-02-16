def Randomize(partObjects):
	# eventually want to randomize the order
	# and re-run the whole thing to get a broader 
	# picture of the solution space
	return(partObjects)

def SortArrayByArgMinIndex(array,index):
	''' MAKE SURE TO SORT BY MOST IMPORTANT INDEX LAST!!! '''
	a = array
	L = len(a)
	for i in range(L):
		temp = a[i]
		flag = 0
		j = 0
		while j < i and flag == 0:
			if temp[index] < a[j][index]:
				a[j+1] = a[j]
				a[j] = temp
				j += 1
			else:
				flag = 1
	return(a)

def UniqueValues(array):
	u_a = []
	L = len(array)
	for i in range(L):
		if array[i] in u_a:
			continue
		else:
			u_a.append(array[i])
	return(u_a)
