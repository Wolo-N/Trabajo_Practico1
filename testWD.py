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

# Método iterativo de PageRank con distribución inicial equiprobable
N = 10  
d = 0.85 
p_t = [1 / N for _ in range(N)]  # Initial equiprobable distribution
tolerance = 1e-6
iterations = 0
errores = []

while True:
    p_t_plus_1 = []
    for j in range(N):
        # Calculate the PageRank for page j
        page_rank_sum = 0
        for i in range(N):
            page_rank_sum += (d * (W @ D)[j, i]) * p_t[i]
        page_rank_sum += (1 - d) / N
        p_t_plus_1.append(page_rank_sum)
    
    # Calculate the error for this iteration
    error = max(abs(p_t_plus_1[i] - p_t[i]) for i in range(N))
    errores.append(error)

    # Break the loop if the error is less than the tolerance
    if error < tolerance:
        break
    
    p_t = p_t_plus_1  # Update the current PageRank vector
    iterations += 1

print("\n\nMétodo iterativo de PageRank con distribución inicial equiprobable:")
print(p_t)
print("\n\nErrores en cada iteración:", errores)



