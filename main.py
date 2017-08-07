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
    if request.method == 'GET' and request.args.get('numero_telephone') is not None:
        tel = request.args.get('numero_telephone')
        try:  # On essaie de convertir le numero pour voir s'il est au bon format
            tel = int(tel)
        except ValueError:  # Si ce n'est pas le cas, on envoie un message d'erreur
            flash = "Echec de l'envoi. Numéro incorrect."
            status = 'danger'
            return render_template('resolution_lu.html', flash=flash, status=status)
        # Sinon, on envoie le message au destinataire
        tel = str(tel)
        message = request.args.get('message')
        return message
        envoi_sms_babacar(tel, message)
        flash = 'Message envoyé avec succès au ' + tel
        status = 'success'
        return render_template('resolution_lu.html', flash=flash, status=status)
    if request.method == 'GET':
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
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = [z for y in str(x) for z in str(y)]
    message = 'Résolution LU (taille=' + str(taille) + '): ' + ', '.join(map(str, message))
    return render_template('resolution_lu_resultats.html', taille=taille, x=x, message=message)


@app.route('/factorisation_lu')
def factorisation_lu():
    if request.args.get('taille') is None:
        return render_template('factorisation_lu.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_lu.html', taille=t)


@app.route('/factorisation_lu/resultats', methods=['GET', 'POST'])
def factorisation_lu_results():
    if request.method == 'GET' and request.args.get('numero_telephone') is not None:
        tel = request.args.get('numero_telephone')
        try:  # On essaie de convertir le numero pour voir s'il est au bon format
            tel = int(tel)
        except ValueError:  # Si ce n'est pas le cas, on envoie un message d'erreur
            flash = "Echec de l'envoi. Numéro incorrect."
            status = 'danger'
            return render_template('factorisation_lu.html', flash=flash, status=status)
        # Sinon, on envoie le message au destinataire
        tel = str(tel)
        message = request.args.get('message')
        envoi_sms_babacar(tel, message)
        flash = 'Message envoyé avec succès au ' + tel
        status = 'success'
        return render_template('factorisation_lu.html', flash=flash, status=status)
    if request.method == 'GET':
        return redirect(url_for('factorisation_lu'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    L = creer_matrice_carree(taille)
    L = methode_factorisation_lu(A)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = [z for y in str(L) for z in y]
    message = 'Factorisation LU (taille=' + str(taille) + '): ' + ', '.join(map(str, message))
    return render_template('factorisation_lu_resultats.html', L=L, taille=taille, message=message)


@app.route('/factorisation_cholesky')
def factorisation_cholesky():
    if request.args.get('taille') is None:
        return render_template('factorisation_cholesky.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_cholesky.html', taille=t)


@app.route('/factorisation_cholesky/resultats', methods=['GET', 'POST'])
def factorisation_cholesky_results():
    if request.method == 'GET' and request.args.get('numero_telephone') is not None:
        tel = request.args.get('numero_telephone')
        try:  # On essaie de convertir le numero pour voir s'il est au bon format
            tel = int(tel)
        except ValueError:  # Si ce n'est pas le cas, on envoie un message d'erreur
            flash = "Echec de l'envoi. Numéro incorrect."
            status = 'danger'
            return render_template('factorisation_cholesky.html', flash=flash, status=status)
        # Sinon, on envoie le message au destinataire
        tel = str(tel)
        message = request.args.get('message')
        envoi_sms_babacar(tel, message)
        flash = 'Message envoyé avec succès au ' + tel
        status = 'success'
        return render_template('factorisation_cholesky.html', flash=flash, status=status)
    if request.method == 'GET':
        return redirect(url_for('factorisation_cholesky'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    B = creer_matrice_carree(taille)
    B = methode_factorisation_cholesky(A)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = [z for y in str(B) for z in y]
    message = 'Factorisation Cholesky (taille=' + str(taille) + '): ' + ', '.join(map(str, message))
    return render_template('factorisation_cholesky_resultats.html', taille=taille, B=B, message=message)


@app.route('/inversion_matrice')
def inversion_matrice():
    if request.args.get('taille') is None:
        return render_template('inversion_matrice.html')
    t = int(request.args.get('taille'))
    return render_template('inversion_matrice.html', taille=t)


@app.route('/inversion_matrice/resultats', methods=['GET', 'POST'])
def inversion_matrice_resultats():
    if request.method == 'GET' and request.args.get('numero_telephone') is not None:
        tel = request.args.get('numero_telephone')
        try:  # On essaie de convertir le numero pour voir s'il est au bon format
            tel = int(tel)
        except ValueError:  # Si ce n'est pas le cas, on envoie un message d'erreur
            flash = "Echec de l'envoi. Numéro incorrect."
            status = 'danger'
            return render_template('inversion_matrice.html', flash=flash, status=status)
        # Sinon, on envoie le message au destinataire
        tel = str(tel)
        message = request.args.get('message')
        envoi_sms_babacar(tel, message)
        flash = 'Message envoyé avec succès au ' + tel
        status = 'success'
        return render_template('inversion_matrice.html', flash=flash, status=status)
    if request.method == 'GET':
        return redirect(url_for('inversion_matrice'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(0, taille):
        for j in range(0, taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    I = creer_matrice_carree(taille)
    I = methode_inversion_matrice(A)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = [z for y in str(I) for z in y]
    message = 'Inversion Matrice (taille=' + str(taille) + '): ' + ', '.join(map(str, message))
    return render_template('inversion_matrice_resultats.html', taille=taille, I=I, message=message)


@app.route('/aide')
def aide():
    return render_template('aide.html')


@app.route('/test/')
def test():
    envoi_sms_babacar('778659165', 'KINGGOLDCHAINS')
    return 'TEST'


if __name__ == '__main__':
    app.run(debug=True)
