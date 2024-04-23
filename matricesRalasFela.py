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
        # Inicializa una nueva instancia de la MatrizRala con dimensiones M x N.
        # Se utiliza un diccionario para almacenar las filas de manera eficiente.
        self.filas = {}
        self.shape = (M, N)  # Guarda las dimensiones de la matriz como una tupla.

    def __getitem__(self, idx):
        # Método especial para obtener el valor de la matriz en el índice dado (fila, columna).
        fila, columna = idx  # Desempaqueta el índice en fila y columna.
        if fila in self.filas and columna in self.filas[fila]:
            # Si la fila y la columna existen en el diccionario, devuelve el valor correspondiente.
            return self.filas[fila][columna]
        else:
            # Si no hay una entrada para la fila o la columna, devuelve 0 (asumiendo una matriz dispersa).
            return 0

    def __setitem__(self, idx, value):
        # Método especial para establecer el valor en el índice dado (fila, columna).

        fila, columna = idx  # Desempaqueta el índice en fila y columna.
        if fila not in self.filas:
            # Si la fila no existe en el diccionario, la crea.
            self.filas[fila] = {}
        # Asigna el valor en la posición especificada en el diccionario.
        self.filas[fila][columna] = value

    def __mul__( self, k ):
        # COMPLETAR:
        # Esta funcion implementa el producto matriz-escalar -> A * k
        res = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res.__setitem__((i,j), self.__getitem__((i,j))*k)
        return res

    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k # mismo que poner self.__mul__(k)

    def __add__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            print("Resta no valida")
            raise Exception
        res = MatrizRala(self.shape[0],self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res.__setitem__((i,j),self.__getitem__((i,j)) + other.__getitem__((i,j)))
        return res

    def __sub__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            print("Resta no valida")
            return
        res = MatrizRala(self.shape[0],self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res.__setitem__((i,j),self.__getitem__((i,j)) - other.__getitem__((i,j)))
        return res

    def __matmul__(self, other):
        # Implementa el producto matricial utilizando el operador '@' en Python.
        # Verifica que el número de columnas en la primera matriz ('self') sea igual al número de filas en 'other'.
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")

        res = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                suma = 0
                for k in range(self.shape[1]):
                    suma += self[i, k] * other[k, j]
                res[i, j] = suma
        print(res)
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

def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    pass





