import csv
import numpy as np

def cargar_citas_csv():
    archivo_citas = "papers/citas.csv"
    lista_citas = []
    with open(archivo_citas, newline='', encoding='utf-8') as csvfile:
        lector_citas = csv.reader(csvfile)
        next(lector_citas)  # Saltar el encabezado
        for cita, citado in lector_citas:
            lista_citas.append((cita, citado))  # Tratar como cadenas
    return lista_citas

def cargar_papers():
    archivo_papers = "papers/papers.csv"
    lista_papers = []
    with open(archivo_papers, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            lista_papers.append([
                fila['id'],  # Tratar como cadena
                fila['titulo'],
                fila['autores'],
                int(fila['anio'])  # Convertir a entero
            ])
    return lista_papers

def genW(lista_citas, lista_papers):
    id_to_index = {paper[0]: idx for idx, paper in enumerate(lista_papers)}
    N = len(lista_papers)
    W = np.zeros((N, N))
    for citador, citado in lista_citas:
        if citador in id_to_index and citado in id_to_index:
            W[id_to_index[citador], id_to_index[citado]] = 1
    return W

def genD(W):
    N = W.shape[0]
    D = np.zeros((N, N))
    for i in range(N):
        suma_columna = np.sum(W[:, i])
        if suma_columna != 0:
            D[i, i] = 1 / suma_columna
    return D

def P_it(d, N, W, D):
    p_t = np.ones((N, 1)) / N

    tolerance = 1e-6
    error = 1

    unoMenosDeSobreEne = ((1 - d) / N)
    d_W = d * W

    while error > tolerance:
        p_t_plus_1 = unoMenosDeSobreEne + d_W @ (D @ p_t)
        error = np.max(np.abs(p_t_plus_1 - p_t))
        p_t = p_t_plus_1

    return p_t

def main():
    lista_citas = cargar_citas_csv()
    lista_papers = cargar_papers()

    W = genW(lista_citas, lista_papers)
    D = genD(W)
    N = len(lista_papers)
    d = 0.85

    page_ranks = P_it(d, N, W, D)

    papers_scores = [(lista_papers[i][0], lista_papers[i][1], page_ranks[i, 0]) for i in range(N)]

    sorted_papers = sorted(papers_scores, key=lambda x: x[2], reverse=True)

    print("Top 10 Papers by PageRank:")
    for rank, (paper_id, title, score) in enumerate(sorted_papers[:10], start=1):
        print(f"{rank}. Paper ID: {paper_id}, Title: \"{title}\", Score: {score}")

if __name__ == "__main__":
    main()
