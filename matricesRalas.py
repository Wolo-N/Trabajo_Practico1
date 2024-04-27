# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None
        self.longitud = 0
        
        self.current = self.Nodo(None, self.raiz)
 
    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)    
    
        nuevoNodo = self.Nodo( valor, self.raiz )
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:      
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self
    
    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None
        
        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')
        
        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')
            
        return nodoActual
        
    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor
    
    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor
            self.siguiente = siguiente


class MatrizRala:
    def __init__( self, M, N ):
        self.filas = {}
        self.shape = (M, N)

    """def __getitem__(self, Idx):
    # Esta función implementa la indexación (Idx es una tupla (m,n)) -> A[m,n]
    # tupla m = filas y n = columnas
        m, c = Idx
        if m in self.filas:
            fila = self.filas[m]
            actual = fila.nodoPorCondicion(lambda n: n.valor[0] == c) # 
            return actual.valor[1]
        else:
            return 0"""
        
    def __getitem__( self, Idx ):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        # tupla m= filas y n = columnas
        m,c = Idx
        if m in self.filas:
            fila = self.filas[m]
            actual = fila.raiz
            while actual is not None:
                if actual.valor[0] == c:
                    return actual.valor[1]
                actual = actual.siguiente
        return 0
        
    def __setitem__(self, Idx, v):
        # Esta función implementa la asignación durante indexación (Idx es una tupla (m,n)) -> A[m,n] = v
        m, c = Idx # m filas, c columnas
        if m in self.filas:
            fila = self.filas[m]
            actual = fila.raiz
            anterior = None
            while actual is not None:
                if actual.valor[0] == c:
                    # Si la columna ya existe en la fila, actualizamos el valor
                    actual.valor = (c, v)
                    return 
                elif actual.valor[0] > c:
                    # Si encontramos una columna mayor que la que buscamos, insertamos el nuevo valor antes
                    nuevo_nodo = ListaEnlazada.Nodo((c, v), actual)
                    if anterior is None:
                        fila.raiz = nuevo_nodo
                    else:
                        anterior.siguiente = nuevo_nodo
                        nuevo_nodo.siguiente = actual  # Actualizamos el puntero siguiente del nuevo nodo
                    return 
                anterior = actual
                actual = actual.siguiente
            # Si la columna no existe en la fila, la insertamos al final de la fila
            fila.insertarDespuesDeNodo((c, v), anterior)  # Pasamos el valor y el nodo anterior
        else:
            # Si la fila no existe, creamos una nueva fila con el valor asignado
            fila = ListaEnlazada()
            fila.push((c, v))
            self.filas[m] = fila


    def __mul__(self, k):
    # Esta función implementa el producto matriz-escalar -> A * k
        matriz_resultado = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                valor = self[i,j] * k
                if valor != 0:
                    matriz_resultado[i,j] = valor  # Asignar el valor multiplicado a la matriz resultante
        return matriz_resultado

    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            raise ValueError("Suma no valida")
        res = MatrizRala(self.shape[0],self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                suma = self[i,j] + other[i,j]
                if suma != 0:
                    res[i,j] = suma  # Asignar el valor multiplicado a la matriz resultante
        return res
    
    def __sub__( self, other ):
    # COMPLETAR:
    # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            raise ValueError("Resta no valida")
        res = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                resta = self[i, j] - other[i, j]
                if resta != 0:
                    res[i, j] = resta  # Asignar el valor de la resta solo si no es cero
        return res

    
    def __matmul__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise Exception
        res = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                suma = 0
                for k in range(self.shape[1]):
                    suma += self[i,k] * other[k,j]
                res[i,j] = suma
        return res


    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res

def GaussJordan(A, b):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    if A.shape[0] != len(b):
        raise ValueError("Los tamaños de b y A no son compatibles")

    M = MatrizRala(A.shape[0], A.shape[1] + 1)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            M[i, j] = A[i, j]
        M[i, A.shape[1]] = b[i]  # La última columna es b

    for i in range(A.shape[0]):  # Gauss-Jordan elimination
        if M[i, i] == 0:
            for k in range(i + 1, A.shape[0]):
                if M[k, i] != 0:
                    # Swap rows if necessary
                    for j in range(A.shape[1] + 1):
                        M[i, j], M[k, j] = M[k, j], M[i, j]  # Intercambiar filas
                    break
            if M[i, i] == 0:
                if M[i, -1] == 0:
                    raise ValueError("El sistema tiene infinitas soluciones.")
                else:
                    raise ValueError("El sistema no tiene solución.")

        divisor = M[i, i]
        for j in range(A.shape[1] + 1):
            M[i, j] /= divisor

        for k in range(A.shape[0]):
            if k != i:
                factor = M[k, i]
                for j in range(i, A.shape[1] + 1):
                    M[k, j] -= factor * M[i, j]

    # Check for free variables by looking for rows that are all zeros except for the right-hand side
    for i in range(A.shape[0]):
        if all(M[i, j] == 0 for j in range(A.shape[1])) and M[i, A.shape[1]] != 0:
            raise ValueError("El sistema no tiene solución.")

    # Check if the number of pivots (non-zero leading terms) is less than the number of variables
    pivot_count = sum(1 for i in range(min(A.shape[0], A.shape[1])) if M[i, i] != 0)
    if pivot_count < A.shape[1]:
        raise ValueError("El sistema tiene infinitas soluciones debido a las variables libres.")

    x = [0] * A.shape[0]
    for i in range(A.shape[0]):
        x[i] = M[i, A.shape[1]]
    return x

def suma_matriz_constante(matriz, constante):
    # Suma de una constante a cada elemento
    result = MatrizRala(matriz.shape)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            result[i, j] = matriz[i, j] + constante
    return result


def multiplicar_matriz_vector(matriz, vector):
    resultado = [0] * len(vector)
    for i in range(len(vector)):
        suma = 0
        for j in range(len(vector)):
            suma += matriz[i, j] * vector[j]
        resultado[i] = suma
    return resultado


def main():
    a = MatrizRala(3,3)
    print(a)
    
if __name__ == "__main__":
    main()