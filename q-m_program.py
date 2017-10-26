import copy
import numpy

def check_empty(group):

    if len(group) == 0:
        return True
    else:
        count = 0
        for i in group:
            if i:
                count+=1
        if count == 0:
            return True
    return False

#compare two binary strings, check where there is one difference
def compBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None

def remove_redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group

def combinePairs(group, unchecked):
    #define length
    l = len(group) -1

    #check list
    check_list = []

    #create next group
    next_group = [[] for x in range(l)]

    #go through the groups
    for i in range(l):
        #first selected group
        for elem1 in group[i]:
            #next selected group
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    #append the ones used in check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    #replace the different bit with '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked

def piChart(Chart,minterm_list,unchecked):
	c=0
	print("\n\nMinterms", end = "\t")
	for i in minterm_list:
		print(i, end = "\t")
	print("\n")
	#for j in unchecked:
		#print(j,end="\t\t")	
	for i,j in zip(Chart, unchecked):
		print(j,end="\t\t")
		for j in i:
			print(j, end = "\t")
		print()
	print()

def compBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True

def find_prime(Chart):
    prime_row = []
    for col in range(len(Chart[0])):
        count = 0
        pos_row = 0
        for row in range(len(Chart)):
            #find essential
            if Chart[row][col] == 1:
                count += 1
                pos_row = row

        if count == 1:
            prime_row.append(pos_row)
            Chart[row][col]=0

    return prime_row
'''
def makeRow0(Chart, prime_row):
	Chart_np = numpy.array(Chart) 
	for i in range(len(Chart)):
		if i in prime_row:
			for j in range(len(Chart[0])):
				if(Chart[i][j]==1):
					Chart[i][j]=0
					Chart_np[:,j]=0
'''
def makeRowCol0(Chart, prime_row):
	for row in range(len(Chart)):
		flag=0
		for col in range(len(Chart[0])):
			if row in prime_row:
				if(Chart[row][col]==1):
					Chart[row][col]=0
					for i in range(len(Chart)):
						Chart[i][col]=0

#print the binary code to letter
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        #if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n+=1
        #conditions for next operations
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out


def main():
	n_var = int(input("\nEnter the number of switching variables: "))
	minterms = input("\nEnter the minterms (ex. 0 1 6 8 11) : ")
	a = minterms.split()
	#put the numbers in list in int form
	a = list(map(int, a))
	minterm_list = a
	print(minterm_list)
	no_of_minterms = len(a)
	group=[[] for x in range(n_var+1)]
	for i in range(no_of_minterms):
	#convert to binary
		a[i] = bin(a[i])[2:]
		if len(a[i]) < n_var:
			for j in range(n_var - len(a[i])):
				a[i] = '0'+ a[i]
		elif len(a[i]) > n_var:
			print ('\n Error : Choose the correct number of variables(bits)\n')
			return
		index = a[i].count('1')
		group[index].append(a[i])
		print(group)
	print(group)
	prime_row=[]
	all_group=[]
	unchecked = []
	#combine the pairs in series until nothing new can be combined
	while check_empty(group) == False:
		all_group.append(group)
		next_group, unchecked = combinePairs(group,unchecked)
		group = remove_redundant(next_group)
		print(next_group,"\n")

	print("All Group" , all_group)
	print("Unchecked" , unchecked)

	Chart = [[0 for x in range(len(minterm_list))] for x in range(len(unchecked))]
	for i in range(len(a)):
		for j in range (len(unchecked)):
			if compBinarySame(unchecked[j], a[i]):
				Chart[j][i] = 1

	old_chart = [[0 for x in range(len(minterm_list))] for x in range(len(unchecked))]
	s=''
	s1=''
	pi_row=set()
	minterm_set_list = [set() for i in range(len(Chart))]
	while Chart != old_chart:
		old_chart = copy.deepcopy(Chart)
		print(old_chart)
		piChart(Chart, minterm_list, unchecked)
		prime_row = prime_row + find_prime(Chart)
		if makeRowCol0(Chart,prime_row)!=old_chart:
			makeRowCol0(Chart,prime_row)
		else:
			for row in range(len(Chart)):
				for col in range(len(Chart[0])):
					if Chart[row][col] == 1:
						minterm_set_list[row].append(col)
			for row in range(len(minterm_set_list)-1):
				for i in range(row+1,len(minterm_set_list)):
					if minterm_set_list[row] == minterm_set_list[i]:
						pi_row.add(row)
						pi_row.add(i)
					elif minterm_set_list[row] > minterm_set_list[i]:
						prime_row = prime_row + [row]
					elif minterm_set_list[row] < minterm_set_list[i]:
						prime_row = prime_row + [i]	

	prime_row=set(prime_row)
	print("--Answer--")
	for i in range(len(unchecked)):
		if i in prime_row:
			print(unchecked[i])
			s= s+binary_to_letter(unchecked[i])+' + '
	if pi_row == prime_row or len(pi_row)==0:
		print (s[:(len(s)-3)])
	else:
		for j in pi_row:
			print (s[:(len(s)-3)],end="")
			s1=s1+binary_to_letter(unchecked[j])
			print(" + " , s1)
			s1=''


if __name__ == "__main__":
    main()
    exit_program = input("\nPress Enter to Quit")
