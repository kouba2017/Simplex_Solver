## Simplex Solver Implementations
This repository contains two implementations of the Simplex algorithm for solving linear programming problems:

* C++ Implementation: Designed for Canonical Linear Programs. The source code for this implementation can be found in the cpp_solution folder.
* Python Implementation: Uses NumPy for matrix operations. The source code and an example can be found in the algo folder.
  
**Features**

  * C++ Implementation
     - Efficient and suitable for large-scale problems.
      - Code is organized in the cpp_solution folder.
        
  * Python Implementation
    
      -Easy to understand and modify.
   
      -Leverages the powerful NumPy library for numerical computations.
   
       -Example usage is provided in the algo folder.
    
**Web Application**

We have developed a web application to test the Python version of the Simplex solver. The application allows you to input variables and constraints, then solve the linear programming problem to find the optimal solution, which is highlighted in yellow.

*Running the Web Application*

1-Navigate to the web_app folder:
    Open your terminal and navigate to the web_app directory:
                    ```cd web_app```

2- Install Dependencies:
      Ensure you have pipenv and flask installed:
                 ``` pip install pipenv flask ```
                 
3- Run the Server:
      Start the web server by running:
                 ``` py server.py```
                 
4- Access the Application:
     Open your web browser and navigate to http://localhost:5000 to access the web application.

**Prerequisites**

  - Ensure you have Python installed.
  - Install dependencies using pipenv:
              ``` pip install pipenv ```
                     
**Installation**

To get started, clone this repository and navigate to the relevant folders to explore the C++ and Python implementations.


**Acknowledgments**

  - NumPy for providing powerful numerical operations.
  - Flask for the web framework used in the Python implementation.
