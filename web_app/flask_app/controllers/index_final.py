from flask_app import app
from flask import render_template,redirect,request,session
import heapq
import numpy as np

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
        "constraint_name":[
            request.form["name_1"],
            request.form["name_2"],
            request.form["name_3"],
        ],
        "a": [
            [float(request.form["ax0"]), float(request.form["ay0"])],
            [float(request.form["ax1"]), float(request.form["ay1"])],
            [float(request.form["ax2"]), float(request.form["ay2"])]
        ],
        "b": [
            float(request.form["b0"]),
            float(request.form["b1"]),
            float(request.form["b2"])
        ],
        "c": [
            float(request.form["c0"]),
            float(request.form["c1"])
        ],
        "z":request.form["z"],
        "symb":[
            request.form["symb0"],
            request.form["symb1"],
            request.form["symb2"]
        ]
    }
    # keep the data in the session so it will reappear with the routing
    session["data"]=data
    print(session["data"]["z"])
    return redirect("/result")

@app.route("/result")
def result():
    A,b,c=convert_standard_pl(session["data"]["c"],session["data"]["a"],session["data"]["b"],session["data"]["z"],session["data"]["symb"])
    res=[]
    result,bf = simplex(c, A, b,session["data"]["z"])
    for i in range(2):
        res.append("%.2f" % float(result[f'variable_decision_{2-i}']))
    v=result['valeur_objectif']
    
    return render_template("result.html",data=session["data"],res=res,z="%.2f" % float(v),premier_member=bf)


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
    c = np.array([c[0], c[1]])  # Coefficients de la fonction objectif
    A = np.array([A[0], A[1], A[2]])  # Coefficients des contraintes
    b = np.array([b[0],b[1],b[2]]) 
    if z == "min":
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
        bf[i] ="%.2f" % float(np.dot(A[i, :], T[:n]))
    return bf



