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
    len_lista_papers = len(lista_papers)
    W = MatrizRala(len_lista_papers,len_lista_papers)
    for citador, cita in lista_citas:
        W[citador, cita] = 1
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
    matriz = MatrizRala(n,m)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            matriz[i,j] = 1
    return matriz

def P_it(d,N,W,D):
    p_t = MatrizRala(N,1)     # Initial equiprobable distribution
    for i in range(N):
        p_t[i,0] = 1/N

    tolerance = 1e-6
    errores = []
    error = 1

    mat_unos = matriz_de_unos(N,1)
    unoMenosDeSobreEne = ((1-d)/N) * mat_unos
    print(1)
    d_W = d * W
    print(2)
    d_WD = d_W @ D
    print(3)


    while error > tolerance:
        # Multiplica la matriz W_D por el vector p_t y escala por d
        print('hola')
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

    # Get the top 10 papers
    top_papers = P_it(d, N, W, D)[:10]
    for i, paper in enumerate(top_papers, start=1):
        print(f"Top {i}: Paper ID {paper[0]} with PageRank score {paper[1]}")





if __name__ == "__main__":
    main()