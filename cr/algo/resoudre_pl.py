import heapq

def identity(numRows, numCols, val=1, rowStart=0):
    return [[(val if i == j else 0) for j in range(numCols)] for i in range(rowStart, numRows)]

def standardForm(cost, num_constraints, constraint_types):
    newVars = num_constraints
    numRows = num_constraints

    newCost = list(cost) + [0] * newVars
    constraints = []
    threshold = []

    for constraint_type, threshold_values in constraint_types.items():
        for threshold_value in threshold_values:
            if constraint_type == "greater":
                constraints.append([0] * len(cost) + [1 if i == idx else 0 for i in range(num_constraints)])
                threshold.append(threshold_value)
            elif constraint_type == "less":
                constraints.append([0] * len(cost) + [-1 if i == idx else 0 for i in range(num_constraints)])
                threshold.append(threshold_value)
            elif constraint_type == "equal":
                constraints.append([0] * len(cost) + [0 if i != idx else 1 for i in range(num_constraints)])
                threshold.append(threshold_value)

    return newCost, constraints, threshold

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def column(A, j):
    return [row[j] for row in A]

def transpose(A):
    return [column(A, j) for j in range(len(A[0]))]

def isPivotCol(col):
    return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1

def variableValueForPivotColumn(tableau, column):
    pivotRow = [i for (i, x) in enumerate(column) if x == 1][0]
    return tableau[pivotRow][-1]

def initialTableau(c, A, b):
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    tableau.append([ci for ci in c] + [0])
    return tableau

def primalSolution(tableau):
    columns = transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
    return [(colIndex, variableValueForPivotColumn(tableau, columns[colIndex])) for colIndex in indices]

def objectiveValue(tableau):
    return -(tableau[-1][-1])

def canImprove(tableau):
    return any(x > 0 for x in tableau[-1][:-1])

def moreThanOneMin(L):
    return len(set(val for idx, val in L)) != len(L)

def findPivotIndex(tableau):
    column_choices = [(i, x) for (i, x) in enumerate(tableau[-1][:-1]) if x > 0]
    column = min(column_choices, key=lambda a: a[1])[0]

    if all(row[column] <= 0 for row in tableau):
        raise Exception('Linear program is unbounded.')

    quotients = [(i, r[-1] / r[column]) for i, r in enumerate(tableau[:-1]) if r[column] > 0]

    if moreThanOneMin(quotients):
        raise Exception('Linear program is degenerate.')

    return min(quotients, key=lambda x: x[1])[0], column

def pivotAbout(tableau, pivot):
    i, j = pivot
    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k, row in enumerate(tableau):
        if k != i:
            pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x, y in zip(tableau[k], pivotRowMultiple)]

def simplex(c, A, b):
    tableau = initialTableau(c, A, b)
    print("Initial tableau:")
    for row in tableau:
        print(row)
    print()

    while canImprove(tableau):
        pivot = findPivotIndex(tableau)
        print("Next pivot index is =", pivot)
        pivotAbout(tableau, pivot)
        print("Tableau after pivot:")
        for row in tableau:
            print(row)
        print()

    return tableau, primalSolution(tableau), objectiveValue(tableau)

def collect_LP_from_user():
    num_variables = int(input("Enter the number of variables: "))
    num_constraints = int(input("Enter the number of constraints: "))

    print("Enter the coefficients of the objective function:")
    c = [float(input(f"c[{i}]: ")) for i in range(num_variables)]

    print("Enter the constraint matrix A (one row at a time):")
    A = [[float(input(f"A[{i}][{j}]: ")) for j in range(num_variables)] for i in range(num_constraints)]

    print("Enter the right-hand side vector b:")
    b = [float(input(f"b[{i}]: ")) for i in range(num_constraints)]

    constraint_types = {}
    for i in range(num_constraints):
        constraint_type = input(f"Enter type of constraint for constraint {i+1} (greater/less/equal): ")
        threshold_value = float(input(f"Enter threshold value for constraint {i+1}: "))
        constraint_types.setdefault(constraint_type, []).append(threshold_value)

    return c, A, b, num_constraints, constraint_types

if __name__ == "__main__":
    c, A, b, num_constraints, constraint_types = collect_LP_from_user()

    new_cost, new_constraints, threshold = standardForm(c, num_constraints, constraint_types)

    t, s, v = simplex(new_cost, new_constraints, b)

    print("Primal Solution:")
    for variable, value in s:
        print(f"x[{variable}] = {value}")
    print("Objective Value:", v)

