from matricesRalas import MatrizRala, GaussJordan
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

w = MatrizRala(11,11)

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
matriz_identidad = matriz_identidad(11,11)

d = 0.85
N = 10

A = (matriz_identidad - (d*W)@D)
b = []
for i in range(11):
    b.append((1 - d)/N)

pestrella = GaussJordan(A,b)
print(pestrella)


def P_it(d,N,W,D):
    p_t = MatrizRala(N,1)
    for i in range(N):
        p_t[i,0] = 1/N

    #print(p_t) ¿porqué nos da lo mismo para todos?
    tolerance = 1e-6
    #print(tolerance)
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
    return p_t

def main():
    # Define variables iniciales
    N = 11
    d = 0.85

    # Construir matriz W
    w = MatrizRala(N, N)
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
    W = build_w(w, assignments)

    # Construir matriz D
    D = build_d(W)

    # Calcular PageRank vector
    page_ranks = P_it(d, N, W, D)

    # Preparar lista de tuplas (paper_id, paper_title, PageRank score)
    # Aquí simplemente vamos a utilizar un rango de 1 a N como IDs de los papers, ya que no se proporciona una lista de papers.
    papers_scores = [(str(i+1), f"Paper {i+1}", page_ranks[i, 0]) for i in range(N)]

    # Ordenar papers por PageRank score en orden descendente
    sorted_papers = sorted(papers_scores, key=lambda x: x[2], reverse=True)

    # Imprimir los 10 mejores papers según PageRank
    print("Top 10 Papers by PageRank:")
    for rank, (paper_id, title, score) in enumerate(sorted_papers[:10], start=1):
        print(f"{rank}. Paper ID: {paper_id}, Title: \"{title}\", Score: {score}")

if __name__ == "__main__":
    main()

