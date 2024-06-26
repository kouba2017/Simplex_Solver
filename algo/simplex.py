import heapq
import numpy as np

def simplex(c, A, b,z):
    m, n = A.shape
    tableau = np.zeros((m+1, n+m+1))
    tableau[:-1, :-1] = np.hstack((A, np.eye(m)))
    tableau[:-1, -1] = b
    # Ajustement de la dimension de c ici
    c_adjusted = np.zeros(n+m)
    c_adjusted[:len(c)] = -c
    tableau[-1, :-1] = c_adjusted
    tableau[-1, -1] = 0

    while np.any(tableau[-1, :-1] < 0):
        entering_variable = np.argmin(tableau[-1, :-1])
        if np.all(tableau[:-1, entering_variable] <= 0):
            raise Exception('Le programme n\'a pas de solution finie.')
        ratios = tableau[:-1, -1] / tableau[:-1, entering_variable]
        leaving_variable = np.argmin(ratios[ratios > 0])
        
        pivot = tableau[leaving_variable, entering_variable]
        tableau[leaving_variable, :] /= pivot
        for i in range(m+1):
            if i != leaving_variable:
                ratio = tableau[i, entering_variable]
                tableau[i, :] -= ratio * tableau[leaving_variable, :]
    
    variables_decision = tableau[:-1, -1]
    solution = {
      'valeur_objectif': tableau[-1, -1],
      'tableau_simplexe': tableau
    }
    for i in range(n):
        solution[f'variable_decision_{i+1}'] = variables_decision[i]
    if(z=="max"):
      solution['valeur_objectif']=-solution['valeur_objectif']
    bf=premier_member(A,solution['tableau_simplexe'])
    return solution,bf 

def convert_standard_pl(c,A,b,z,op):
  c = np.array(c)  # Coefficients de la fonction objectif
  A = np.array(A)  # Coefficients des contraintes
  b = np.array(b) 
  if z == "max":
        return A, b, c
  else:
        c = -c  # Inverser les coefficients de la fonction objectif pour la minimisation
  for i in range(3):
        if op[i] == ">=" or op[i] == ">":
            A[i, :] = -A[i, :]  # Inverser les coefficients des contraintes
            b[i] = -b[i]  # Inverser les valeurs des contraintes
  return A,b,c
def premier_member(A, tableau):
    m, n = A.shape
    T = tableau[:-1, -1][::-1] 
    T = [T[1],T[2]] 
    bf = np.zeros(m)
    print(T)
    for i in range(m):
        bf[i] = np.dot(A[i, :], T[:n])
    return bf


  
# Exemple d'utilisation
z = "min"
op=["<=",">=","<="]
c = np.array([-2, -3])  # Coefficients de la fonction objectif
A = np.array([[1,6], [-2,-2], [4,1]])  # Coefficients des contraintes
b = np.array([30, -15, 24])  # Valeurs des contraintes
A,b,c=convert_standard_pl(c,A,b,z,op)
resultat,bf = simplex(c, A, b,z)
print("Solution optimale:")
print("Valeur de la fonction objectif:", resultat['valeur_objectif'])
for i in range(2):
    print(f"Valeur de la variable de decision {i+1}: {resultat[f'variable_decision_{2-i}']}")
print(bf)
