from matricesRalas import ListaEnlazada, MatrizRala, GaussJordan, multiplicar_matriz_vector, suma_matriz_constante
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
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            matriz[i,j] = 1
    return matriz


D = build_d(W)

# (identidad - d*W*D)*pestrella = (1-d)/N * 1|
# d = 0.85
matriz_identidad = matriz_identidad(10,10)

d = 0.85
N = 10

A = (matriz_identidad - (d*W)@D)
b = []
for i in range(10):
    b.append((1 - d)/N)

pestrella = GaussJordan(A,b)
print(pestrella)

# Define variables iniciales
# N = 10
# d = 0.85
# p_t = [1 / N for _ in range(N)]  # Distribución inicial equiprobable de PageRank

# tolerance = 1e-6  # Tolerancia para el criterio de parada del algoritmo
# errores = []
# error = 1

# matriz_de_unoss = matriz_de_unos(10,10)

# while error > tolerance:
#     p_t_plus_1 = []  # Lista para almacenar los nuevos valores de PageRank
#     for j in range(N):
#         # Calcula el PageRank para la página j
#         page_rank_sum = 0
#         for i in range(N):
#             # Suma contribuciones de todas las páginas i a la página j
#             page_rank_sum += (d * (W @ D)) * p_t
#         # Añade la probabilidad de teletransporte (reinicio aleatorio)
#         page_rank_sum += ((1 - d) / N ) * matriz_de_unoss
#         p_t_plus_1.append(page_rank_sum)

#     # Calcula el error máximo en esta iteración comparando el nuevo vector de PageRank con el anterior
#     error = max(abs(p_t_plus_1[i] - p_t[i]) for i in range(N))
#     errores.append(error)  # Añade el error a la lista de errores

#     p_t = p_t_plus_1  # Actualiza el vector de PageRank para la próxima iteración

# print("\n\nMétodo iterativo de PageRank con distribución inicial equiprobable:")
# print(p_t)
# print("\n\nErrores en cada iteración:", errores)

N = 10
d = 0.85
p_t = MatrizRala(N,1)     # Initial equiprobable distribution
for i in range(N):
    p_t[i,0] = 1/N

tolerance = 1e-6
errores = []
error = 1

mat_unos = matriz_de_unos(N,1)
unoMenosDeSobreEne = ((1-d)/N) * mat_unos

d_W = d * W
d_WD = d_W @ D


while error > tolerance:
    # Multiplica la matriz W_D por el vector p_t y escala por d
    p_t_plus_1 = d_WD @ p_t
    p_t_plus_1 = unoMenosDeSobreEne + p_t_plus_1
    # Calcula el error máximo en esta iteración comparando el nuevo vector de PageRank con el anterior
    error = max(abs(p_t_plus_1[i,0] - p_t[i,0]) for i in range(N))
    errores.append(error)

    # Actualiza el vector de PageRank para la próxima iteración
    p_t = p_t_plus_1

print("\n\nMétodo iterativo de PageRank con distribución inicial equiprobable:")
print(p_t)
print("\n\nErrores en cada iteración:", errores)