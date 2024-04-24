import pytest
from matricesRalas import MatrizRala
import numpy as np

class TestIndexacionMatrices:
    def test_indexarCeros( self ):
        A = MatrizRala(3,3)
        
        assert np.allclose( np.zeros(9), [A[i,j] for i in range(3) for j in range(3)] )

    def test_asignarValor( self ):
        A = MatrizRala(3,3)
        A[0,0] = 1

        assert A[0,0] == 1

    def test_asignarDejaCeros(self):
        A = MatrizRala(3,3)
        A[0,0] = 1

        assert np.allclose( np.zeros(9), [A[i,j] if (i != j and i != 0) else 0 for i in range(3) for j in range(3)] )

    def test_asignarEnMismaFila( self ):
        A = MatrizRala(3,3)
        A[0,1] = 2
        A[0,0] = 1

        assert A[0,1] == 2 and A[0,0] == 1

    def test_reasignar( self ):
        A = MatrizRala(3,3)
        A[1,0] = 1
        A[1,0] = 3

        assert A[1,0] == 3

class TestSumaMatrices:
    def test_distintasDimensiones( self ):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)
        with pytest.raises(Exception) as e_info:
            C = A + B

    def test_sumaCorrectamente( self ):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        B[0,2]=3
        B[1,1]=2

        C = A+B
        assert C[0,0] == 1 and C[0,2] == 6 and C[2,2] == 4 and C[1,1] == 2
        
class TestRestaMatrices:
    def test_distintasRestaDimensiones( self ):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)
        with pytest.raises(Exception) as e_info:
            C = A - B

    def test_restaCorrectamente( self ):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[1,1]=4
        A[0,2]=3
        A[2,2]=4

        B[0,2]=3
        B[1,1]=2

        C = A-B
        assert C[0,0] == 1 and C[2,2] == 4 and C[1,1] == 2

class TestProductoPorEscalar:
    def test_escalaCorrectamente( self ):
        A = MatrizRala(3,3)
        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        C = A * 13
        assert C[0,0] == (1*13) and C[0,2] == (3*13) and C[2,2] == (4*13)

class TestProductoMatricial:
    def test_dimensionesEquivocadas(self):
        A = MatrizRala(2,3)
        B = MatrizRala(4,3)
        with pytest.raises(Exception) as e_info:
            C = A @ B

    def test_productoAndaBien(self):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        B[2,0]=3
        B[1,1]=2

        C = A @ B

        assert C.shape[0] == 2 and C.shape[1]==3 and C[0,0] == 9 and all( [C[i,i] == 0 for i in range(3) for j in range(4) if (i!=j and i!=0)] )

    def test_productoPorIdentidad( self ):
        A = MatrizRala(3,3)
        Id = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        Id[0,0] = 1
        Id[1,1] = 1
        Id[2,2] = 1

        C1 = A @ Id
        C2 = Id @ A
        assert C1[0,0] == 1 and C1[0,2] == 3 and C1[1,2] == 4 and C2[0,0] == 1 and C2[0,2] == 3 and C2[1,2] == 4 and C1.shape == C2.shape and C1.shape == A.shape

class TestGaussJordan:
    def test_unique_solution(self):
        # System: x + y = 2, 2x + y = 3
        A = MatrizRala(2, 2)
        A[0, 0] = 1  # x coefficient
        A[0, 1] = 1  # y coefficient
        A[1, 0] = 2
        A[1, 1] = 1
        b = [2, 3]  # Results vector
        expected_solution = [1, 1]  # x = 1, y = 1
        assert GaussJordan(A, b) == expected_solution, "Test for unique solution failed."

    def test_no_solution(self):
        # System: x + y = 2, x + y = 3 (clearly inconsistent)
        A = MatrizRala(2, 2)
        A[0, 0] = 1
        A[0, 1] = 1
        A[1, 0] = 1
        A[1, 1] = 1
        b = [2, 3]
        with pytest.raises(ValueError):
            GaussJordan(A, b)
    
    def test_dimension_mismatch(self):
        # Dimension mismatch between A (2x2) and b (3x1)
        A = MatrizRala(2, 2)
        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 0] = 3
        A[1, 1] = 4
        b = [1, 2, 3]
        with pytest.raises(ValueError):
            GaussJordan(A, b)

    def test_singular_matrix(self):
        # Test a singular matrix where determinant should be zero (no unique solution)
        A = MatrizRala(2, 2)
        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 0] = 2
        A[1, 1] = 4
        b = [1, 2]
        with pytest.raises(ValueError):
            GaussJordan(A, b)
