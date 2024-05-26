


from flask_app import app
from flask import render_template,redirect,request,session

app.secret_key="session_solver"

@app.route("/")
def index():
    # data={
    #     "a": {"x":[-1,1,1],"y":[4,-1,1]},
    #     "b":[160,30,80],
    #     "c":[20.00,60.00],
    #     "z":3520.00,
    #     "symb":["<=","<=","<="],
    #     "res":{"x":32,"y":48}
    # }
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solver():
    data={
        "a":{"x":[
            request.form["ax0"],
            request.form["ax1"],
            request.form["ax2"]
        ],
        "y":[
            request.form["ay0"],
            request.form["ay1"],
            request.form["ay2"]
        ]},
        "b":[
            request.form["b0"],
            request.form["b1"],
            request.form["b2"]
        ],
        "c":[
            request.form["c0"],
            request.form["c1"]
        ],
        "symb":[
            request.form["symb0"],
            request.form["symb1"],
            request.form["symb2"]
        ]
    }
    # keep the data in the session so it will reappear with the routing
    session["data"]=data
    return redirect("/result")

@app.route("/result")
def result():
    s,v=solve_it(session["data"])
    res=[]
    for variable, value in s:
        print(f"x[{variable}] = {value}")
        res.append(round(value))
    
    return render_template("result.html",data=session["data"],res=res,z=round(v))


#Solving Simplex Algo

import heapq


def identity(numRows, numCols, val=1, rowStart=0):
   return [[(val if i == j else 0) for j in range(numCols)]
               for i in range(rowStart, numRows)]



def standardForm(cost, greaterThans=[], gtThreshold=[], lessThans=[], ltThreshold=[],
               equalities=[], eqThreshold=[], maximization=True):
   newVars = 0
   numRows = 0
   if gtThreshold != []:
      newVars += len(gtThreshold)
      numRows += len(gtThreshold)
   if ltThreshold != []:
      newVars += len(ltThreshold)
      numRows += len(ltThreshold)
   if eqThreshold != []:
      numRows += len(eqThreshold)

   if not maximization:
      cost = [-x for x in cost]

   if newVars == 0:
      return cost, equalities, eqThreshold

   newCost = list(cost) + [0] * newVars

   constraints = []
   threshold = []

   oldConstraints = [(greaterThans, gtThreshold, -1), (lessThans, ltThreshold, 1),
                     (equalities, eqThreshold, 0)]

   offset = 0
   for constraintList, oldThreshold, coefficient in oldConstraints:
      constraints += [c + r for c, r in zip(constraintList,
         identity(numRows, newVars, coefficient, offset))]

      threshold += oldThreshold
      offset += len(oldThreshold)

   return newCost, constraints, threshold


def dot(a,b):
   return sum(x*y for x,y in zip(a,b))

def column(A, j):
   return [row[j] for row in A]

def transpose(A):
   return [column(A, j) for j in range(len(A[0]))]

def isPivotCol(col):
   return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1

def variableValueForPivotColumn(tableau, column):
   pivotRow = [i for (i, x) in enumerate(column) if x == 1][0]
   return tableau[pivotRow][-1]

# assume the last m columns of A are the slack variables; the initial basis is
# the set of slack variables
def initialTableau(c, A, b):
   tableau = [row[:] + [x] for row, x in zip(A, b)]
   tableau.append([ci for ci in c] + [0])
   return tableau


def primalSolution(tableau):
   # the pivot columns denote which variables are used
   columns = transpose(tableau)
   indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
   return [(colIndex, variableValueForPivotColumn(tableau, columns[colIndex]))
            for colIndex in indices]


def objectiveValue(tableau):
   return -(tableau[-1][-1])


def canImprove(tableau):
   lastRow = tableau[-1]
   return any(x > 0 for x in lastRow[:-1])


# this can be slightly faster
def moreThanOneMin(L):
   if len(L) <= 1:
      return False

   x,y = heapq.nsmallest(2, L, key=lambda x: x[1])
   return x == y


def findPivotIndex(tableau):
   # pick minimum positive index of the last row
   column_choices = [(i,x) for (i,x) in enumerate(tableau[-1][:-1]) if x > 0]
   column = min(column_choices, key=lambda a: a[1])[0]

   # check if unbounded
   if all(row[column] <= 0 for row in tableau):
      raise Exception('Linear program is unbounded.')

   # check for degeneracy: more than one minimizer of the quotient
   quotients = [(i, r[-1] / r[column])
      for i,r in enumerate(tableau[:-1]) if r[column] > 0]

   if moreThanOneMin(quotients):
      raise Exception('Linear program is degenerate.')

   # pick row index minimizing the quotient
   row = min(quotients, key=lambda x: x[1])[0]

   return row, column


def pivotAbout(tableau, pivot):
   i,j = pivot

   pivotDenom = tableau[i][j]
   tableau[i] = [x / pivotDenom for x in tableau[i]]

   for k,row in enumerate(tableau):
      if k != i:
         pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
         tableau[k] = [x - y for x,y in zip(tableau[k], pivotRowMultiple)]


def simplex(c, A, b):
   tableau = initialTableau(c, A, b)
   print("Initial tableau:")
   for row in tableau:
      print(row)
   print()

   while canImprove(tableau):
      pivot = findPivotIndex(tableau)
      print("Next pivot index is=%d,%d \n" % pivot)
      pivotAbout(tableau, pivot)
      print("Tableau after pivot:")
      for row in tableau:
         print(row)
      print()

   return tableau, primalSolution(tableau), objectiveValue(tableau)



def collect_LP_from_user(data):
    # Prompt the user to enter the number of variables and constraints
    num_constraints=3
    
    # Prompt the user to enter the coefficients of the objective function
    print("Enter the coefficients of the objective function:")
    c = [float(data["c"][i]) for i in range(1)]
    
   # Prompt the user to enter the constraint matrix
    print("Enter the constraint matrix A (one row at a time):")
    A = [[float(data["a"][j][i]) for j in {"x","y"}] for i in range(2)]

   # Prompt the user to enter the right-hand side vector
    print("Enter the right-hand side vector b:")
    b = [float(data["b"][i]) for i in range(2)]

    return c, A, b,num_constraints

def solve_it(data):
    # Collect the linear program from the user
    c, A, b ,num_constraints= collect_LP_from_user(data)
    # add slack variables by hand
    num_slack_variables = num_constraints
    for row in A:
      row += [0] * num_slack_variables
      c += [0] * num_slack_variables

    # Solve the linear program using the simplex algorithm
    t, s, v = simplex(c, A, b)
    
    # Print the primal solution and the value of the objective function
    print("Primal Solution:")
    for variable, value in s:
        print(f"x[{variable}] = {value}")
    print("Objective Value:", v)
    return s,v
