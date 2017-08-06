from flask import Flask, render_template, url_for, request, redirect
from calcul import *

app = Flask(__name__)


@app.route('/')
@app.route('/accueil')
def index():
    return render_template('index.html')


@app.route('/resolution_lu')
def resolution_lu():
    if request.args.get('taille') is None:
        return render_template('resolution_lu.html')
    t = int(request.args.get('taille'))
    return render_template('resolution_lu.html', taille=t)


@app.route('/resolution_lu/resultats', methods=['GET', 'POST'])
def resolution_lu_results():
    if request.method != 'POST':
        return redirect(url_for('resolution_lu'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    b = creer_liste(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    for k in range(0, taille):
        b[k] = float(request.form['b'+str(k)])
    x = creer_liste(taille)
    x = methode_resolution_lu(A, b)
    envoi_sms('778659165', 'hello world')
    return render_template('resolution_lu_resultat.html', taille=taille, x=x)


@app.route('/factorisation_lu')
def factorisation_lu():
    if request.args.get('taille') is None:
        return render_template('factorisation_lu.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_lu.html', taille=t)


@app.route('/factorisation_lu/resultats', methods=['GET', 'POST'])
def factorisation_lu_results():
    if request.method != 'POST':
        return redirect(url_for('factorisation_lu'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    L = creer_matrice_carree(taille)
    L = methode_factorisation_lu(A)
    return render_template('factorisation_lu_results.html', L=L, taille=taille)


@app.route('/factorisation_cholesky')
def factorisation_cholesky():
    if request.args.get('taille') is None:
        return render_template('factorisation_cholesky.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_cholesky.html', taille=t)


@app.route('/factorisation_cholesky/resultats', methods=['GET', 'POST'])
def factorisation_cholesky_results():
    if request.method != 'POST':
        return redirect(url_for('factorisation_cholesky'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    B = creer_matrice_carree(taille)
    B = methode_factorisation_cholesky(A)
    return render_template('factorisation_cholesky_results.html', B=B, taille=taille)


@app.route('/aide')
def aide():
    return render_template('aide.html')


if __name__ == '__main__':
    app.run(debug=True)
