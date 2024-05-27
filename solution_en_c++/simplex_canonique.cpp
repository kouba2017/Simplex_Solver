#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

const double EPSILON = 1.0e-8;

class Simplex {
public:
    Simplex(const vector<vector<double>>& A, const vector<double>& b, const vector<double>& c)
        : m(A.size()), n(A[0].size()), a(m + 1, vector<double>(n + m + 1)), basis(m) {
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                a[i][j] = A[i][j];
            }
        }
        for (int i = 0; i < m; i++) {
            a[i][n + i] = 1.0;
        }
        for (int i = 0; i < m; i++) {
            a[i][n + m] = b[i];
        }
        for (int j = 0; j < n; j++) {
            a[m][j] = c[j];
        }
        for (int i = 0; i < m; i++) {
            basis[i] = n + i;
        }
    }

    double solve() {
        while (true) {
            int q = -1;
            for (int j = 0; j < n + m; j++) {
                if (a[m][j] > EPSILON) {
                    q = j;
                    break;
                }
            }
            if (q == -1) break;

            int p = -1;
            for (int i = 0; i < m; i++) {
                if (a[i][q] > EPSILON) {
                    if (p == -1 || (a[i][n + m] / a[i][q] < a[p][n + m] / a[p][q])) {
                        p = i;
                    }
                }
            }
            if (p == -1) throw "Linear program is unbounded.";

            pivot(p, q);
            basis[p] = q;
        }

        vector<double> x(n);
        for (int i = 0; i < m; i++) {
            if (basis[i] < n) {
                x[basis[i]] = a[i][n + m];
            }
        }
        for (int i = 0; i < n; i++) {
            cout << "x[" << i << "] = " << x[i] << endl;
        }
        return a[m][n + m];
    }

private:
    int m, n;
    vector<vector<double>> a;
    vector<int> basis;

    void pivot(int p, int q) {
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n + m; j++) {
                if (i != p && j != q) {
                    a[i][j] -= a[p][j] * a[i][q] / a[p][q];
                }
            }
        }
        for (int i = 0; i <= m; i++) {
            if (i != p) {
                a[i][q] = 0.0;
            }
        }
        for (int j = 0; j <= n + m; j++) {
            if (j != q) {
                a[p][j] /= a[p][q];
            }
        }
        a[p][q] = 1.0;
    }
};
void donner(vector<vector<double>>& A,vector<double>&b,vector<double>& c){
    int x;
cout<<"c'est le temps pour resoudre un pl standard pour le tp RO "<<endl;
cout<<"donner le nombre des variable decisives"<<endl;
int n;
cin>>n;
c.resize(n);
//---------------------lecture de fonction objectif --------------------------------------
cout<<"donner les coefficients de fonction objectif"<<endl;
for (int i=0;i<n;i++){
      x=i+1;
    cout<<"coef"<<x<<" ="<<endl;
    cin>>c[i];
};
//---------------------les contraintes--------------------------------------------

int y;
cout<<"donner le nombre de contraintes"<<endl;
cin>>y;
b.resize(y);
A.resize(y, vector<double>(n));
int j;
for (int i=0;i<y;i++){
    cout<<"remplir la contraintes"<<i+1<<endl;
    for(j=0;j<n;j++){
        cout<<"x"<<j+1<<"*";
        cin>>A[i][j];
        if(j!=n-1){
            cout<<" +"<<endl;
        }

    };
    cout<<" <= ";
    cin>>b[i];
};
cout<<"merci de remplir le PL"<<endl;

}

int main() {
    vector<vector<double>> A ;
    vector<double> b ;
    vector<double> c ;
    donner(A,b,c);
    Simplex simplex(A, b, c);
    cout << "solution optimale est : " << (simplex.solve())*-1 << endl;

    return 0;
}
