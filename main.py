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
    # Si on a reçu un numéro de téléphone, c'est qu'on est dans la partie envoi_sms
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
        envoi_sms_babacar(tel, message)
        flash = 'Message envoyé avec succès au ' + tel
        status = 'success'
        return render_template('resolution_lu.html', flash=flash, status=status)
    # Pour tout autre accès avec GET, on envoie le formulaire de saisie de la taille de la matrice
    if request.method == 'GET':
        return redirect(url_for('resolution_lu'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    b = creer_liste(taille)
    for i in range(taille):
        for j in range(taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    for k in range(taille):
        b[k] = float(request.form['b'+str(k)])
    x = creer_liste(taille)
    x = methode_resolution_lu(A, b)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = 'Résolution LU (x): '
    try:
        for i in range(taille):
            message += 'x[' + str(i) + ']=' + str(x[i]) + ', '
    except TypeError:
        message = "impossible de résoudre le système"
        return render_template('resolution_lu_resultats.html', taille=taille, x=0, message=message)
    return render_template('resolution_lu_resultats.html', taille=taille, x=x, message=message)


@app.route('/factorisation_lu')
def factorisation_lu():
    if request.args.get('taille') is None:
        return render_template('factorisation_lu.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_lu.html', taille=t)


@app.route('/factorisation_lu/resultats', methods=['GET', 'POST'])
def factorisation_lu_results():
    # Si on a reçu un numéro de téléphone, c'est qu'on est dans la partie envoi_sms
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
    # Pour tout autre accès avec GET, on envoie le formulaire de saisie de la taille de la matrice
    if request.method == 'GET':
        return redirect(url_for('factorisation_lu'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(taille):
        for j in range(taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    L = creer_matrice_carree(taille)
    U = creer_matrice_carree(taille)
    L, U, ok = methode_factorisation_lu(A, L, U)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = 'Factorisation LU (L): '
    for i in range(taille):
        for j in range(taille):
            message += 'L[' + str(i) + ',' + str(j) + ']=' + str(L[i][j]) + ', '
    message += 'et (U): '
    for i in range(taille):
        for j in range(taille):
            message += 'U[' + str(i) + ',' + str(j) + ']=' + str(U[i][j]) + ', '
    return render_template('factorisation_lu_resultats.html', L=L, U=U, taille=taille, message=message, ok=ok)


@app.route('/factorisation_cholesky')
def factorisation_cholesky():
    if request.args.get('taille') is None:
        return render_template('factorisation_cholesky.html')
    t = int(request.args.get('taille'))
    return render_template('factorisation_cholesky.html', taille=t)


@app.route('/factorisation_cholesky/resultats', methods=['GET', 'POST'])
def factorisation_cholesky_results():
    # Si on a reçu un numéro de téléphone, c'est qu'on est dans la partie envoi_sms
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
    # Pour tout autre accès avec GET, on envoie le formulaire de saisie de la taille de la matrice
    if request.method == 'GET':
        return redirect(url_for('factorisation_cholesky'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(taille):
        for j in range(taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    B = creer_matrice_carree(taille)
    B = methode_factorisation_cholesky(A)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = 'Factorisation Cholesky (B): '
    for i in range(taille):
        for j in range(taille):
            message += 'B[' + str(i) + ',' + str(j) + ']=' + str(B[i][j]) + ', '
    return render_template('factorisation_cholesky_resultats.html', taille=taille, B=B, message=message)


@app.route('/inversion_matrice')
def inversion_matrice():
    if request.args.get('taille') is None:
        return render_template('inversion_matrice.html')
    t = int(request.args.get('taille'))
    return render_template('inversion_matrice.html', taille=t)


@app.route('/inversion_matrice/resultats', methods=['GET', 'POST'])
def inversion_matrice_resultats():
    # Si on a reçu un numéro de téléphone, c'est qu'on est dans la partie envoi_sms
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
    # Pour tout autre accès avec GET, on envoie le formulaire de saisie de la taille de la matrice
    if request.method == 'GET':
        return redirect(url_for('inversion_matrice'))
    taille = int(request.form['taille'])
    A = creer_matrice_carree(taille)
    for i in range(taille):
        for j in range(taille):
            A[i][j] = float(request.form['A'+str(i)+'_'+str(j)])
    I = creer_matrice_carree(taille)
    I = methode_inversion_matrice(A)
    # On converti d'bord le resultat en chaine de caractère(au cas où on devrai l'envoyer par sms)
    message = 'Inversion Matrice (I): '
    for i in range(taille):
        for j in range(taille):
            message += 'I[' + str(i) + ',' + str(j) + ']=' + str(I[i][j]) + ', '
    return render_template('inversion_matrice_resultats.html', taille=taille, I=I, message=message)


@app.route('/aide')
def aide():
    return render_template('aide.html')


if __name__ == '__main__':
    app.run(debug=True)
