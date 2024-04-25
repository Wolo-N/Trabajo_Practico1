import numpy as np
from matricesRalas import ListaEnlazada, MatrizRala, GaussJordan
# a = 0
# b = 1
# c = 2
# d = 3
# e = 4
# f = 5
# g = 6
# h = 7
# i = 8
# j = 9
# k = 10

w = MatrizRala(10,10)

assignments = {
    (1, 0): 1, (5, 0): 1, (6, 0): 1, # B, F y G citan a A
    (0, 2): 1,
    (0, 3): 1, (0, 4): 1,
    (8, 5): 1,
    (5, 6): 1,
    (6, 7): 1,
    (6, 8): 1, (7, 8): 1, (9, 8): 1,
    (4, 10): 1
}

def build_w(matriz, citas):
    for indices, value in assignments.items():
        w[indices] = value
    return w

W = build_w(w, assignments)

def build_d(matriz_w):
    D = MatrizRala(matriz_w.shape[0], matriz_w.shape[1])
    
    for i in range(matriz_w.shape[1]):
        cj = 0
        for j in range(matriz_w.shape[0]):
            cj += matriz_w[j,i]
        if cj != 0:
            D[i,i] = 1 if (round(1/cj, 3) == 1) else round(1/cj , 3)
        else:
            D[i,i] = 0

    return D

def matriz_identidad(n,m):
    matriz = MatrizRala(n,m)

    for i in range(matriz.shape[1]):
        matriz[i,i] = 1
    return matriz

def matriz_de_unos(n,m):
    matriz = MatrizRala(n,m)

    for i in range(matriz.shape[1]):
        for j in range(matriz.shape[0]):
            matriz[i,j] = 1
    return matriz


D = build_d(W)

# (identidad - d*W*D)*pestrella = (1-d)/N * 1|
# d = 0.85
matriz_identidad = matriz_identidad(10,10)
matriz_de_unos = [1,1,1,1,1,1,1,1,1,1]

d = 0.85
N = 10

A = (matriz_identidad - (d*W)@D)
b = []
for i in range(10):
    b.append((1 - d)/N)

pestrella = GaussJordan(A,b)
print(pestrella)

# Definición de constantes
d = 0.85
N = 10

# Construcción de la matriz A y el vector b
identidad = matriz_identidad(10, 10)
b = [((1 - d) / N) for _ in range(10)]

A = (identidad - d * W @ D)

# Resolución del sistema lineal utilizando Gauss-Jordan
pestrella = GaussJordan(A, b)
print("Solución del sistema lineal utilizando Gauss-Jordan:")
print(pestrella)

# Método iterativo de PageRank con distribución inicial equiprobable
p_t = [1 / N for _ in range(10)]  # Distribución inicial equiprobable
iterations = 0
max_iterations = 1000
tolerance = 1e-6
errors = []

# Iteraciones del método iterativo de PageRank
while True:
    p_t_plus_1 = [sum(d * W[j,i] * D[i,i] * p_t[i] for i in range(10)) + ((1 - d) / N) for j in range(10)]
    error = max(abs(p_t_plus_1[i] - p_t[i]) for i in range(10))
    errors.append(error)
    if error < tolerance or iterations >= max_iterations:
        break
    p_t = p_t_plus_1
    iterations += 1

print("\nMétodo iterativo de PageRank con distribución inicial equiprobable:")
print(p_t)