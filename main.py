from flask import Flask, render_template, url_for, request, redirect
from calcul import *
app = Flask(__name__)

@app.route('/')
@app.route('/accueil')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/aide')
def aide():
	return render_template('aide.html')
@app.route('/resol_lu')
def resol_lu():
	if request.args.get('taille') is None:
		return render_template('resol_lu.html')
	t = int(request.args.get('taille'))
	return render_template('resol_lu.html', taille=t)

@app.route('/resol_lu/results', methods=['GET', 'POST'])
def resol_lu_results():
	if request.method != 'POST':
		return redirect(url_for('resol_lu'))
	taille = int(request.form['taille'])
	A = CreeMatCar(taille)
	b = CreerListe(taille)
	for i in range(0,taille):
		for j in range(0,taille):
			A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
	for k in range(0,taille):
		b[k] = float(request.form['b'+str(k)])
	x = CreerListe(taille)
	x = solveSystLU(A, b)
	return render_template('resol_lu_results.html', taille=taille, x=x)

@app.route('/fact_lu')
def fact_lu():
	if request.args.get('taille') is None:
		return render_template('fact_lu.html')
	t = int(request.args.get('taille'))
	return render_template('fact_lu.html', taille=t)

@app.route('/fact_lu/results', methods=['GET', 'POST'])
def fact_lu_results():
	if request.method != 'POST':
		return redirect(url_for('fact_lu'))
	taille = int(request.form['taille'])
	A = CreeMatCar(taille)
	for i in range(0,taille):
		for j in range(0,taille):
			A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
	L = CreeMatCar(taille)
	L = factLU(A)
	return render_template('fact_lu_results.html', L=L, taille=taille)

@app.route('/fact_chol')
def fact_chol():
	if request.args.get('taille') is None:
		return render_template('fact_chol.html')
	t = int(request.args.get('taille'))
	return render_template('fact_chol.html', taille=t)

@app.route('/fact_chol/results', methods=['GET', 'POST'])
def fact_chol_results():
	if request.method != 'POST':
		return redirect(url_for('fact_chol'))
	taille = int(request.form['taille'])
	A = CreeMatCar(taille)
	for i in range(0,taille):
		for j in range(0,taille):
			A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
	B = CreeMatCar(taille)
	B = factCholesky(A)
	return render_template('fact_chol_results.html', B=B, taille=taille)

if __name__ == '__main__':
	app.run(debug=True)
