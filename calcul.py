from math import *
import requests, json


######################
# Méthodes Générales #
######################


def creer_matrice_carree(n):
    return [[0.0 for j in range(n)] for i in range(n)]


def creer_liste(n):
    return [0.0 for i in range(n)]


####################
# Résolution Gauss #
####################


def rechercher_pivot_gauss(k, A, n):
    i = k
    while i != n and A[i][k] == 0:
        i += 1
    if i != n:
        return i
    else:
        return -1


def permutation_gauss(i0, i, A, b):
    A[i], A[i0] = A[i0], A[i]
    b[i], b[i0] = b[i0], b[i]
    return A, b


def elimination_gauss(k, A, b, n):
    i = k+1
    while i < n:
        r = A[i][k]/A[k][k]        
        b[i] -= r*b[k]
        j = k
        while j < n:
            A[i][j] -= r*A[k][j]
            j += 1
        i += 1
    return A, b


def remontee_gauss(A, b, n):
    x = []
    i = 0
    while i < n:
        x.append(0)
        i += 1
    x[n-1] = b[n-1]/A[n-1][n-1]
    i = n-2
    while i >= 0:
        x[i] = b[i]            
        j = i+1
        while j < n:
            x[i] -= A[i][j]*x[j]
            j += 1
        x[i] /= A[i][i]
        i -= 1
    return x


def methode_resolution_gauss(A, b, n):
    k = 0
    arret = 0
    while k != n and arret != 1:
        i0 = rechercher_pivot_gauss(k, A, n)
        if i0 == -1:
            arret = 1
        else:
            if i0 == k:
                A, b = elimination_gauss(k, A, b, n)
                k += 1
            else: 
                A, b = permutation_gauss(i0, k, A, b)
                A, b = elimination_gauss(k, A, b, n)
                k += 1
    if k == n and A[n-1][n-1] != 0:
        # solutions de l'équation
        x = remontee_gauss(A, b, n)
        for i in range(n):
            x[i] = round(x[i], 4)
        result = ""
        for i in range(n):
            if (i != n) & (i != 0):
                result += "\n"
            result += "x{} = {}".format(i+1, x[i])          
    else:
        # pas de solution unique
        result = "0"
    return result


##################
# Résolution  LU #
##################


def descente_lu(L, b):
    y = creer_liste(n)
    for i in range(n):
        y[i] = b[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]
    return y


def remontee_lu(A, b):
    x = creer_liste(n)
    x[n - 1] = round(b[n - 1] / A[n - 1][n - 1], 3)
    for i in range(n - 2, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
        x[i] = round(x[i], 3)
    return x


def methode_resolution_lu(A, b):
    L = methode_factorisation_lu_2(A)
    if L != 0:
        y = descente_lu(L, b)
        x = remontee_lu(A, y)
        # print("La solution de votre systeme est \n",x)
        return x
    else:
        # print("Ce systeme ne peut pas etre resolu par la methode LU")
        return 0


####################
# Factorisation LU #
####################


def elimination_lu(k, A):
    i = k + 1
    while i < n:
        r = A[i][k] / A[k][k]
        j = k
        while j < n:
            A[i][j] -= r * A[k][j]
            A[i][j] = round(A[i][j], 2)
            j += 1
        i += 1
    return A


def methode_factorisation_lu_2(A):
    global n
    n = len(A)
    k = 0
    arret = 0
    L = creer_matrice_carree(n)
    while k != n and arret != 1:
        L[k][k] = 1
        if A[k][k] != 0:
            for i in range(k + 1, n):
                L[i][k] = round(A[i][k] / A[k][k], 2)
            A = elimination_lu(k, A)
            k += 1
        else:
            arret = 1
    if arret == 0 and A[n-1][n-1] != 0:
        return L
    else:
        print("Les conditions ne sont pas reunies")
        return 0


def methode_factorisation_lu(A,L,U):
    n = len(A)
    ok = 0
    for i in range(n):
        U[0][i] = A[0][i]
        for j in range(n):
            if i <= j:
                L[i][j] = 0
                s = float(0)
                for k in range(i):
                    s += L[i][k]*U[k][j]
                U[i][j] = A[i][j] - s
            else:
                U[i][j] = 0
                t = float(0)
                for k in range(j):
                    t += L[i][k]*U[k][j]
                if U[j][j] != 0:
                    L[i][j] = (A[i][j] - t)/U[j][j]
                else:
                    ok = 1
    for i in range(n):
        L[i][i] = 1
    return L, U, ok


##########################
# Factorisation Cholesky #
##########################


def methode_factorisation_cholesky(A):
    n = len(A)
    B = creer_matrice_carree(n)
    for j in range(n):
        B[j][j] = A[j][j]
        for k in range(j):
            B[j][j] -= B[j][k] * B[j][k]
        B[j][j] = round(sqrt(abs(B[j][j])), 2)
        for i in range(j + 1, n):
            B[i][j] = A[i][j]
            for k in range(j):
                B[i][j] -= B[i][k] * B[j][k]
            B[i][j] = round(B[i][j] / B[j][j], 2)
    return B


###################
# Inverse Matrice #
###################


def recopier_matrice(A):
    # Recopie la matrice A pour eviter des problemes de pointeurs
    B = creer_matrice_carree(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            B[i][j] = A[i][j]
    return B


def echanger_lignes(A, i, j):
    # Operation elementaire, echange des lignes i et j de la matrice A
    # modifiee par pointeur, la fonction ne retourne donc rien
    """
    Attention, indexage a partir de 0 (ligne 1 = ligne 0)
    """
    I = A[i]
    J = A[j]
    A[i] = J
    A[j] = I


def pivot_partiel(A, j0):
    # Recherche de pivots partiels en commencant au rang j0 de la matrice A
    # La fonction renvoi l'index du pivot suivant
    pivot = A[j0][j0]
    index = j0
    for k in range(j0 + 1, len(A)):
        if pivot <= abs(A[k][j0]):
            pivot = abs(A[k][j0])
            index = k
    return index


def creer_matrice_identite(n):
    # Cree une matrice creer_matrice_identite de taille n
    A = creer_matrice_carree(n)
    for i in range(n):
        A[i][i] = 1
    return A


def transvection(A, i, j, mu):
    # Operation elementaire, transvection des lignes i et j de la matrice
    # A avec un coeficient multiplicateur de mu
    for k in range(len(A)):
        A[i][k] += mu * A[j][k]


def methode_inversion_matrice(A):
    n = len(A)
    A0 = recopier_matrice(A)
    global I
    I = creer_matrice_identite(n)
    i = 0
    for i in range(n - 1):  # triangularisation de la matrice
        index_pivot = pivot_partiel(A0, i)
        echanger_lignes(A0, i, index_pivot)
        echanger_lignes(I, i, index_pivot)
    for k in range(i + 1, n):
        mu = float(A0[k][i]) / float(A0[i][i])
        transvection(A0, k, i, -mu)
        transvection(I, k, i, -mu)
    for i in range(n):  # coef diagonaux a 1
        mu = A0[i][i]
        for j in range(n):
            if mu != 0:
                A0[i][j] = float(A0[i][j]) / float(mu)
                I[i][j] = float(I[i][j]) / float(mu)
    for i in range(1, n):  # annulation des autres coef
        for j in range(n - i):
            mu = A0[j][n - i]
            transvection(I, j, n - i, -mu)
    return A0


#############
# Envoi SMS #
#############


def envoi_sms_babacar(number, message):
    url="http://smsgateway.me/api/v3/messages/send"
    payload = {
        'email': 'ehbc221@gmail.com',
        'password': 'pengriffey221',
        'device': 55955,
        'number': number,
        'message': message
    }
    result = requests.post(url, payload)
    result = result.json()
    return result['success'] and len(result['result']['fails']) == 0


def envoi_sms_moctar(number, message):
    url="http://smsgateway.me/api/v3/messages/send"
    payload = {'email': 'moctardiallo568@gmail.com', 'password': 'passer', 'device': 55748, 'number': number, 'message': message}
    result = requests.post(url, payload)
    result = result.json()
    return result['success'] and len(result['result']['fails']) == 0
