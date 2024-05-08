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
        "z":request.form["z"],
        "symb":[
            request.form["symb0"],
            request.form["symb1"],
            request.form["symb2"]
        ]
    }
    session["data"]=data
    return redirect("/result")

@app.route("/result")
def result():
    res={"x":32,"y":48}
    return render_template("result.html",data=session["data"],res=res)