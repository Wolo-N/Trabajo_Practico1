import csv
import time

from matricesRalas import MatrizRala

def cargar_citas_csv():
    archivo_citas = "papers/citas.csv"
    lista_citas = []
    with open(archivo_citas, newline='', encoding='utf-8') as csvfile:
        lector_citas = csv.reader(csvfile)
        next(lector_citas)  # Skip the header row
        for cita, citado in lector_citas:
            if int(citado) < 79008 and int(cita) < 79008:
                lista_citas.append((int(cita),int(citado)))
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
    contador =0
    for citador, cita in lista_citas:
        if citador < len(lista_papers) and cita < len(lista_papers):
            W[citador, cita] = 1
            contador+=1
    print(contador)
    return W

def genD(W):
    D = MatrizRala(W.shape[0], W.shape[1])

    for i in W.filas:  # Iterate only through indices that have rows initialized
        cj = 0
        current_node = W.filas[i].raiz
        while current_node:
            cj += current_node.valor[1] # Assume that valor is a tuple (column_index, value)
            current_node = current_node.siguiente
        if cj == 1:
            D[i, i] = 1
        elif cj > 1:
            D[i, i] = 1/cj

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
    return p_t, errores


def main():
    
    # Llamar a la función y pasar la ruta al archivo CSV
    lista_citas = cargar_citas_csv()
    print(len(lista_citas))
    #print(lista_citas)  # Imprimir la lista de citas para verificar
    lista_papers = cargar_papers()

    W = genW(lista_citas,lista_papers)
    
    D = genD(W)
    N = len(lista_papers)
    d = 0.85

    page_ranks = P_it(d, N, W, D)
    print(D[41943, 41943])
    print(D[72257, 72257])

    
    lista = []
    for i in range(79008):
        lista.append((page_ranks[0][i,0],i))
    
    maxi = []
    for i in range(10):
        maxi.append(max(lista))
        lista.remove(max(lista))
    print(maxi)



if __name__ == "__main__":
    main()