# Software I wrote in Python to solve a Least Squares problem and do line fitting in Python.
# Written by Benjamin B. Cutler in the Summer of 2016. Email bugs to ben.cutler14@gmail.com
# Sample Matricies
#A = [[1,2],[3,4]]
#B = [[5,6],[7,8]]
# [ 1 2 ] * [ 5 6 ] = [19 22]
# [ 3 4 ]   [ 7 8 ]   [43 50]

#import matplotlib.pyplot as plt
import math

def transpose(A):
    #Pre Condition  : A Matrix, Pass by Reference
    #Post Condition : Returns a copy of that matrix which has swapped rows and columns. Matrix A is uneffected by this operation
    #Purpose        : To make a transpose of an arbitraty N x M matrix
    #Sample I/O     : [1,2] <-> [1,3]
    #               : [3,4] <-> [2,4]
    
    outmatrix = [] # Matrix that gets returned
    for i in range(len(A[0])): # Generates a list of Rows, which will be populated by elements
        outmatrix.append([])
        
    for j in range(len(A[0])): # j makes up the Old cols, which become rows
        for i in range(len(A)): #I makes up col rows, which become colss
            outmatrix[j].append(A[i][j]) 
        
    return outmatrix 

def matrixproduct(A,B):
    # Pre Conditions : Two Matricies, 'A' and 'B', given Matrix A is 'Z' x 'z' and B is  'G' x 'g' matrix presuming g == z.
    # Post Condition : Returns an Z x G matrix
    # Purpose        : To compute the product between two matricies
    # Sample I/O     :
    #A = [[1,2],[3,4]]
    #B = [[5,6],[7,8]]
    # [ 1 2 ] * [ 5 6 ] = [19 22]
    # [ 3 4 ]   [ 7 8 ]   [43 50]
    
    outmatrix = []
    for i in range(len(B[0])): # Generates list of lists, which will be populated by elements
        outmatrix.append([])

    if len(A[0]) != len(B): # Makes sure the matricies have the same size.
        print("Matricies must have equal values!")
        quit() # If they don't, this just returns a blank matrix, so that there isn't a value error, which breaks the user from the main function.
    
    # If we have valid input we compute the product
    
    for index,rowsofB in enumerate(transpose(B) ):
        for colsofA in A:
            acc = 0
            for i in range(len(A[0])):
                acc += colsofA[i]*rowsofB[i]
            outmatrix[index].append(acc)
        
    return transpose(outmatrix)

def pivotize(A):
    # Pre Condition   : A matrix 'A' which may not have a value in each pivot
    # Post condition  : The matrix 'A' has the number '1' pivot in each position. Also returns 'A'
    # Purpose         : To put a pivot in each position in the matrix.
    # Sample I/O      : [0,7,4] -> [1,0,(1/3)]
    #                 : [3,0,9] -> [0,1,(7/4)]
    
    for i in range(1000): # This will try 1,000 times to pivotize the matrix.
        counter = -1
        for i in range(len(A)): # Loop through each pivot position
            if A[i][i] == 0:    # Check for a zero there
                chosenrow = random.randint(0,len(A)) # if there is one there, replace it with a random row.
                (A[i],A[chosenrow]) = (A[chosenrow],A[i])
            else:
                counter = counter + 1
        if counter == i:
            break
        if i == 999 :
            print("Something has gone wrong in the pivotize function ")
            printmatrix(A)
            input("Press <Enter> to continue")            
            quit()
            
    # Step 2 requires you to make each pivot equal to 1
    for i in range(len(A)):
        pivot = A[i][i]
        for j in range(len(A[i])):
            A[i][j] = A[i][j] / pivot # Sets each pivot to be equal to 1 by dividing the row by the pivot value
    return A
def rowreduce(A):
    # Pre Condition : An N x N+1 matrix 'A'
    # Post Cond     : Alters 'A' to be in Row Reduced Eschelon Form
    # Purpose       : To take a matrix, and row reduce it to the RREF
    # Sample I/O    : [1,-2,1] -> [1,0,-3]
    #               : [-5,3,9] -> [0,1,-2]
    
    # We must first teach python row subtraction though. This function is defined here to keep it out of the scope of the other functions
    def rowsubtract(row1,row2,n):
        #row1 - n*row2 = outcol
        #[1,2,3] - 5*[.2,.3,45] = [0.0, 0.5, -222]
        # Essentially, you want row1 to be the row that ends up geting the zeroes value
        outcol = []
        for i in range(len(row1)):
            outcol.append(row1[i]- n*row2[i])
        return outcol
    
    for col in range(len(A[0]) -1):
        pivotize(A) 
        for row in range(len(A)):
            if col != row:
                A[row] = rowsubtract(A[row],A[col],A[row][col]/A[row][row])
    return A

def getdata():
	    #Pre Condition : Gets a comma seperated set of numbers from the user. // TODO : Make File Work
	    #Post condition: Stores it in a list, and returns a 2 x N list
	    #Purpose       : Gets data which will be used

	    
	    #This function gets the data from the user. Inputted (hopefully copied) as a list
	    #It presumes you are solving for f(x) = y
	    print("How would you like to enter data? \n a .txt file: 1  \n Manually enter: 2")
	    usernumber = input(">  ")
	    if usernumber == '2' :	
	        print("Assuming the data input is a list of x values and a list of y values. ")
	        print("Enter a value like")
	        print("1,2,3,4")
	        data = []
	        var = ["x","y"]
	        for i in range(2):
	            print(" Please enter  of values of the dependent variable. This is the coordinate {0}".format(var[i]))
	            data.append(eval(input("")))
	            print(" Data points for  {0} has been entered".format(var[i]))
	    elif usernumber == '1':
	    	data = [[],[]]
	    	delimiter = input("What is the delimiter if the text document? ")
	    	filename = input ("Please enter a filename  \n>   ")
	    	infile = open(filename,'r')
	    	for line in infile:
	    		line = line.strip()
	    		line = line.split(delimiter)
	    		data[0].append(int(line[0]))
	    		data[1].append(int(line[1]))	    		
	    else:
	    	print("Please enter either '1' or '2' ")
	    	data = getdata()
	    return data

def printmatrix(A):
    # Primitive Method of printing a matrix
    for line in A:
        print(line)
    print("")

def printWithCoefs(matrix, coeffs):
	if coeffs[0] != "false":
		for num,line in enumerate(matrix):
			print (coeffs[num],' = ', line [-1])
		print("")
	else:
		for i in range(len(matrix)):
			print("Coefficent " ,i+1, ' : ',matrix[i][-1])

def formmatrix(indata): # Needs to be cleaned up a little bit
    # Pre Condition     : Data from the user.
    # Post condition    : Returns a matrix, and a vector it is equal to
    # Purpose           : This takes the data, and puts it into a matrix, which will then be turned into A^T * A = A^T * b.
    # This returns the 'A' and 'b' in this equation. Row reducing the whole N x N+1 matrix yeilds the co-efficents of the least squares solution
    
    A = indata[0]
    b = indata[1]
    print("Select a function you would like to fit data to:")
    print( "1. : A Line (y = mx +b)")
    print( "2. : Custom Function")
    usernumber = int (input("--") )
    ##
    #Get a function from the user to fit the data to
    ##
    if (usernumber == 1):
        userfunction = "{0},1"
        coeffs = ['m','b']
    elif (usernumber == 2):
        # The 'test case' is for a y = Var1*exp(ax) + Var2*exp(bx) Ideally I can find some way of making the user enter the specific function they want.
        print("For example, if you want to fit to y = C1 exp(-.02x) + C2 exp(-.07x),  then you have to input 'math.exp(-.02 * {0}),math.exp( -.07 * {0})'")
        print("For a line, you would want '{0},1' , and this solves for 'm' and 'b' in y = mx + b")
        print("essentially, and plus sign is a comma, and any coefficent has to be left blank. Make the dependent variable, x, {0}")
        userfunction = input("Please enter the function you want to fit data to   \n ")
        coeffs = ["false"]
    ##
    # Make each row in the matrix that gets returned equal user's function -f- evaluated at 'x', where the '+' or '-' delimits elements of the row
    ##
    outmatrix = []
    for num in A:
        row = list(eval(userfunction.format(num)))
        outmatrix.append(row)
    # Same with 'newb' but this fix is a bit easier
    newb = []
    for elt in b:
        newb = newb + [[elt]]
    return outmatrix,newb,coeffs

def equate(A,b):
    # Pre Condition     : A Matrix 'A' and a vector 'b'
    # Post condition    : A new matrix which A concatinated with 'b' at the end of it
    # Purpose           : To equate two matricies
    # Sample I/O        : A = [1,2]  b = [7]  ->  return [1,2,7]
    #                   :     [5,6]      [8]  ->         [5,6,8]
    outmatrix = []
    for i in range(len(A)):
        outmatrix.append( A[i] + b[i])
    return outmatrix

def bestfit( ):
    # Data comes from the user, which I have to  make a bit better.
    data = getdata()
    # Gets the Matricies 'A' and 'b' In their ready to go states
    A,b,coeffs = formmatrix(data) 
    #Compute Transpose(A)*A = Transpose(A)*b
    left = matrixproduct(transpose(A),A)
    right = matrixproduct(transpose(A),b)
    #Turns thesystem into an augmented matrix
    finalmatrix = equate(left,right)
    #Rowreduces said matrix
    rowreduce(finalmatrix)
    printWithCoefs(finalmatrix,coeffs) 
    test = input()
    #Plots user's input Data
    #plt.scatter(data[0],data[1])    

bestfit()
