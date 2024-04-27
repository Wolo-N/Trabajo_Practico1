import csv

from matricesRalas import MatrizRala

def cargar_citas_csv():
    archivo_citas = "papers/citas.csv"
    lista_citas = []
    with open(archivo_citas, newline='', encoding='utf-8') as csvfile:
        lector_citas = csv.reader(csvfile)
        for cita, citado in lector_citas:
            lista_citas.append((cita,citado))
    return lista_citas

def cargar_papers():
    archivo_papers = "papers/papers.csv"
    # Lista para almacenar los datos de los papers
    lista_papers = []

    # Abrir el archivo CSV para leer los datos
    with open(archivo_papers, mode='r', encoding='utf-8') as csvfile:
        # Crear un objeto reader de CSV
        reader = csv.DictReader(csvfile)
        
        # Recorrer las filas del archivo CSV
        for fila in reader:
            # Añadir cada fila como un diccionario a la lista
            lista_papers.append([
                fila['id'],
                fila['title'],
                fila['authors'],
                fila['year']
            ])

    return lista_papers


def genW(lista_citas, lista_papers):
    W = MatrizRala(len(lista_papers),len(lista_papers))
    for citador, cita in lista_citas:
        print("Valores de citador y cita:", citador, cita)  # Agregar este print para rastrear los valores
        W[citador, cita] = 1
    print("Valores de citador y cita después del bucle:", citador, cita)  # Agregar este print para verificar los valores al salir del bucle
    return W


def genD(W):
    D = MatrizRala(W.shape[0], W.shape[1])
    
    for i in range(W.shape[1]):
        cj = 0
        if i in W.filas:
            for j in range(W.shape[0]):
                cj += W[j,i]
        if cj != 0:
            D[i,i] = 1 if (round(1/cj, 3) == 1) else round(1/cj , 3)
        else:
            D[i,i] = 0
    return D

def matriz_de_unos(n,m):
    # Inicializamos la matriz de uno 
    matriz = MatrizRala(n,m)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            matriz[i,j] = 1
    return matriz

def P_it(d,N,W,D):
    p_t = MatrizRala(N,1)
    for i in range(N):
        p_t[i,0] = 1/N

    #print(p_t) ¿porqué nos da lo mismo?
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
    # Llamar a la función y pasar la ruta al archivo CSV
    lista_citas = cargar_citas_csv()
    #print(lista_citas)  # Imprimir la lista de citas para verificar
    lista_papers = cargar_papers()

    W = genW(lista_citas,lista_papers)
    D = genD(W)
    N = len(lista_papers)
    d = 0.85

    # Calculate PageRank vector
    page_ranks = P_it(d, N, W, D)
    #print(page_ranks)

    # Prepare list of (paper_id, paper_title, PageRank score) tuples
    papers_scores = [(lista_papers[i][0], lista_papers[i][1], page_ranks[i, 0]) for i in range(N)]  # Assuming paper ID is the first element and title is the second

    # Sort papers by PageRank score in descending order
    sorted_papers = sorted(papers_scores, key=lambda x: x[2], reverse=True)

    # Print the top 10 papers
    print("Top 10 Papers by PageRank:")
    for rank, (paper_id, title, score) in enumerate(sorted_papers[:10], start=1):
        print(f"{rank}. Paper ID: {paper_id}, Title: \"{title}\", Score: {score}")

if __name__ == "__main__":
    main()