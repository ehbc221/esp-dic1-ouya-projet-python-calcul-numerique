from math import *
import requests
import json


def creer_matrice_carree(n):
    return [[0.0 for j in range(n)] for i in range(n)]


def creer_liste(n):
    return [0.0 for i in range(n)]


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


def resolution_gauss(A, b, n):
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


def methode_factorisation_cholesky(A):
    n = len(A)
    B = creer_matrice_carree(n)
    for j in range(n):
        B[j][j]=A[j][j]
        for k in range(j):
            B[j][j] -= B[j][k]*B[j][k]
        B[j][j] = round(sqrt(abs(B[j][j])), 2)
        for i in range(j+1, n):
            B[i][j] = A[i][j]
            for k in range(j):
                B[i][j] -= B[i][k]*B[j][k]
            B[i][j] = round(B[i][j]/B[j][j], 2)
    return B


"""
def factorisation_lu(A,L,U):
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
"""


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


def methode_factorisation_lu(A):
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
    L = methode_factorisation_lu(A)
    if L != 0:
        y = descente_lu(L, b)
        x = remontee_lu(A, y)
        # print("La solution de votre systeme est \n",x)
        return x
    else:
        # print("Ce systeme ne peut pas etre resolu par la methode LU")
        return 0


def envoi_sms(number,message):
    url="http://smsgateway.me/api/v3/messages/send"
    payload = {
        'email': 'ehbc221@gmail.com',
        'password': 'pengriffey',
        'device': 55955,
        'number': '+221778659165',
        'message': 'TEST 123'
    }
    result = requests.post(url, payload)
    result = result.json()
    return result['success'] and len(result['result']['fails']) == 0
