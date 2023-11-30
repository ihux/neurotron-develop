"""
module matfun: Matrix functions:
- EYE                   # unit matrix
- ZEROS                 # zero matrix
- ONES                  # one matrix
- RAND                  # random matrix
- SEED                  # set random seed
- MAX                   # row of column maxima
- MIN                   # row of column minima
- SIZE                  # matrix sizes
- MAGIC                 # magic matrix
- SUM                   # row of column sum
- ANY                   # row of column any's
- ALL                   # row of column all's
- length                # maximum size
- isempty               # check if matrix is empty
- NOT                   # logical not
- AND                   # logical and
- OR                    # logical OR
"""

import numpy as np
#import matrix as mx
from neurotron.math.matrix import Matrix
from neurotron.math.helper import isa, isnumber

#===============================================================================
# matrix functions
#===============================================================================

def EYE(n):
    """
    >>> EYE(3)
    [1 0 0; 0 1 0; 0 0 1]
    """
    I = Matrix(n,n)
    for k in range(n):
        I[k,k] = 1
    return I

def ZEROS(m,n=None):
    """
    >>> ZEROS(3)
    [0 0 0; 0 0 0; 0 0 0]
    >>> ZEROS(2,4)
    [0 0 0 0; 0 0 0 0]
    """
    n = m if n is None else n
    if m == 0 or n == 0:
        return Matrix(m,n)
    return Matrix(m,n)

def ONES(m,n=None):
    """
    >>> ONES(3)
    [1 1 1; 1 1 1; 1 1 1]
    >>> ONES(2,3)
    [1 1 1; 1 1 1]
    >>> ONES(0,0)
    []
    """
    n = m if n is None else n
    if m == 0 or n == 0:
        return Matrix(m,n)
    return Matrix(m,n) + 1

def RAND(arg=None,modulus=None):
    """
    >>> SEED(0)
    >>> RAND((2,2))
    [0.548814 0.715189; 0.602763 0.544883]
    >>> RAND((2,3))
    [0.423655 0.645894 0.437587; 0.891773 0.963663 0.383442]
    >>> RAND((0,0))
    []
    >>> RAND(8)
    6
    >>> RAND()
    0.8121687287754932
    >>> RAND((2,3),40)
    [24 17 37; 25 13 8]
    """
    #isa = isinstance
    if arg is None:
        return np.random.rand()
    elif isa(arg,int):
        modulus = int(arg)
        return np.random.randint(modulus)
    elif isa(arg,tuple):
        if len(arg) != 2:
            raise Exception('2-tuple expected as arg1')
        m,n = arg

    R = Matrix(m,n)
    if m == 0 or n == 0:
        return R

    if modulus is None:
        for i in range(m):
            for j in range(n):
                R[i,j] = np.random.rand()
    else:
        modulus = int(modulus)
        for i in range(m):
            for j in range(n):
                R[i,j] = np.random.randint(modulus)
    return R

def SEED(s):
    """
    SEED(): set random seed
    >>> SEED(0)
    """
    np.random.seed(s)

def SIZE(arg):
    """
    SIZE(): matrix sizes
    >>> SIZE(3.14)
    (1, 1)
    >>> SIZE(Matrix(3,5))
    (3, 5)
    >>> SIZE([])
    (0, 0)
    """
    if isinstance(arg,list) and len(arg) == 0:
        return (0,0)
    elif isinstance(arg,int) or isinstance(arg,float):
        return (1,1)
    elif isinstance(arg,Matrix):
        m,n = arg.shape
        return (m,n)
    else:
        raise Exception('bad type')

def MAX(arg1,arg2=None):
    """
    >>> MAX(2,3)
    3
    >>> MAX(2,3.6)
    3.6
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> MAX(A,B)
    [8 3 -2; 1 2 -1]
    >>> MAX(A)
    [1 3 -1]
    >>> MAX(2,A)
    [2 3 2; 2 2 2]
    >>> MAX(B,1)
    [8 2 1; 1 1 1]
    >>> x = MAGIC(2)();  print(x)
    [1; 4; 3; 2]
    >>> MAX(x)
    4
    >>> MAX(x.T)
    4
    """
    scalar1 = isinstance(arg1,int) or isinstance(arg1,float)
    scalar2 = isinstance(arg2,int) or isinstance(arg2,float)

    if scalar1:
        if arg2 is None:
            return arg1
        elif scalar2:
            return max(arg1,arg2)
        else:
            arg1 = arg1 + 0*arg2
    elif scalar2:
        arg2 = arg2 + 0*arg1

    m,n = arg1.shape
    if arg2 is None:
        if m == 1:
            s = arg1[0,0]
            for j in range(1,n): s = max(s,arg1[0,j])
            return int(s) if s == int(s) else s
        elif n == 1:
            s = arg1[0,0]
            for i in range(m): s = max(s,arg1[i,0])
            return int(s) if s == int(s) else s
        M = Matrix(1,n)
        for j in range(n):
            maxi = arg1[0,j]
            for i in range(1,m):
                maxi = max(arg1[i,j],maxi)
            M[0,j] = maxi
    else:
        assert arg1.shape == arg2.shape
        M = Matrix(m,n)
        for i in range(m):
            for j in range(n):
                M[i,j] = max(arg1[i,j],arg2[i,j])
    m,n = M.shape
    if m != 1 or n != 1:
        return M
    result = M.item()
    iresult = int(result)
    return iresult if iresult == result else result

def MIN(arg1,arg2=None):
    """
    >>> MIN(2,3)
    2
    >>> MIN(2.1,3)
    2.1
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> MIN(A,B)
    [1 2 -3; 0 0 -2]
    >>> MIN(A)
    [0 2 -2]
    >>> MIN(2,B)
    [2 2 -3; 1 0 -2]
    >>> MIN(A,1)
    [1 1 -2; 0 1 -1]
    >>> x = MAGIC(2)();  print(x)
    [1; 4; 3; 2]
    >>> MIN(x)
    1
    >>> MIN(x.T)
    1
    """
    scalar1 = isinstance(arg1,int) or isinstance(arg1,float)
    scalar2 = isinstance(arg2,int) or isinstance(arg2,float)

    if scalar1:
        if arg2 is None:
            return arg1
        elif scalar2:
            return min(arg1,arg2)
        else:
            arg1 = arg1 + 0*arg2
    elif scalar2:
        arg2 = arg2 + 0*arg1

    m,n = arg1.shape
    if arg2 is None:
        if m == 1:
            s = arg1[0,0]
            for j in range(1,n): s = min(s,arg1[0,j])
            return int(s) if s == int(s) else s
        elif n == 1:
            s = arg1[0,0]
            for i in range(m): s = min(s,arg1[i,0])
            return int(s) if s == int(s) else s
        M = Matrix(1,n)
        for j in range(n):
            maxi = arg1[0,j]
            for i in range(1,m):
                maxi = min(arg1[i,j],maxi)
            M[0,j] = maxi
    else:
        assert arg1.shape == arg2.shape
        M = Matrix(m,n)
        for i in range(m):
            for j in range(n):
                M[i,j] = min(arg1[i,j],arg2[i,j])
    m,n = M.shape
    if m != 1 or n != 1:
        return M
    result = M.item()
    iresult = int(result)
    return iresult if iresult == result else result

def ALL(arg):
    """
    >>> M = Matrix([[2,0,-1],[2,-1,0]])
    >>> ALL(M)
    [1 0 0]
    >>> ALL([1,2,3])
    1
    >>> ALL(Matrix([0,1,2]).T)
    0
    >>> ALL(5)
    1
    >>> ALL(0.0)
    0
    >>> ALL([])
    1
    >>> ALL(None)
    []
    """

    if isnumber(arg):
        return int(arg != 0)
    elif arg is None:
        return []
    elif isa(arg,list):
        arg = Matrix(arg)
    elif not isa(arg,Matrix):
        raise Exception('cannot handle arg')

    m,n = arg.shape
    if m == 1 or n == 1:
        return all(arg) + 0
    elif m == 0 or n == 0:
        return 1

    M = Matrix(1,n)
    for j in range(n):
        M[0,j] = all(arg[:,j])

    m,n = M.shape
    if m != 1 or n != 1:
        return M
    return M.item()+0

def MAGIC(n):
    """
    >>> MAGIC(0)
    []
    >>> MAGIC(1)
    1
    >>> MAGIC(2)
    [1 3; 4 2]
    >>> MAGIC(3)
    [8 1 6; 3 5 7; 4 9 2]
    >>> MAGIC(4)
    [16 2 3 13; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    """
    if n == 0:
        return []
    elif n == 1:
        return 1
    elif n == 2:
        return Matrix([[1,3],[4,2]])
    elif n == 3:
        return Matrix([[8,1,6],[3,5,7],[4,9,2]])
    elif n == 4:
        return Matrix([[16,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,1]])
    else:
        raise Exception('n > 4 not supported')

def SUM(arg):
    """
    >>> SUM(2)
    2
    >>> SUM(3.14)
    3.14
    >>> SUM([1,2,3])
    6
    >>> A = MAGIC(4)[:3,:];  print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12]
    >>> SUM(A)
    [30 20 19 33]
    >>> SUM(A[:,1])
    20
    >>> SUM(A[2,:])
    34
    >>> SUM(True)
    1
    >>> C=ONES(1,4)
    >>> SUM(C>0)
    4
    """
    #isa = isinstance
    if isa(arg,int) or isa(arg,np.int64) or isa(arg,float):
        return arg
    elif isa(arg,list):
        M = Matrix(arg)
        return SUM(M)
    elif isa(arg,Matrix):
        #print('##### Matrix:',arg)
        m,n = arg.shape
        if m == 0 or n == 0:
            return []
        elif m == 1:
            s = 0
            #print('##### row:',arg,'s:',s)
            for j in range(n): s += arg[0,j]
            return s
        elif n == 1:
            s = 0
            for i in range(m): s += arg[i,0]
            return s
        else:
            out = Matrix(1,n)
            for j in range(n):
                s = 0
                for i in range(m):
                    s += arg[i,j]
                out[0,j] = s
            return out
    else:
        return arg.sum()

def ROW(*args):
    """
    >>> M = MAGIC(4)
    >>> M1 = M[0:2,:];  print(M1)
    [16 2 3 13; 5 11 10 8]
    >>> M2 = M[2:4,:];  print(M2)
    [9 7 6 12; 4 14 15 1]
    >>> ROW(M1,M2)
    [16 2 3 13 9 7 6 12; 5 11 10 8 4 14 15 1]
    >>> ROW([1,2],[3,4])
    [1 2 3 4]
    """
    if len(args) == 0:
        return Matrix([])
    else:
        M0 = args[0]
        if not isinstance(M0,Matrix): M0 = Matrix(M0)
        m,n = M0.shape
        n = 0
        for k in range(len(args)):
            Mk = args[k]
            if not isinstance(Mk,Matrix): Mk = Matrix(Mk)
            mk,nk = Mk.shape
            n += nk
            if mk != m:
                raise Exception('equal number of rows expected')
        M = Matrix(m,n)
        off = 0
        for k in range(len(args)):
            Mk = args[k];
            if not isinstance(Mk,Matrix): Mk = Matrix(Mk)
            mk,nk = Mk.shape
            #print('##### Mk:',Mk)
            assert mk == m
            for i in range(mk):
                for j in range(nk):
                    M[i,off+j] = Mk[i,j]
            off += nk
        return M

def COLUMN(*args):
    """
    >>> M = MAGIC(4)
    >>> M1 = M[:,0:2];  print(M1)
    [16 2; 5 11; 9 7; 4 14]
    >>> M2 = M[:,2:4];  print(M2)
    [3 13; 10 8; 6 12; 15 1]
    >>> COLUMN(M1,M2)
    [16 2; 5 11; 9 7; 4 14; 3 13; 10 8; 6 12; 15 1]
    >>> COLUMN(Matrix([1,2]).T,Matrix([3,4]).T)
    [1; 2; 3; 4]
    """
    if len(args) == 0:
        return Matrix([])
    else:
        M0 = args[0]
        if not isinstance(M0,Matrix): M0 = Matrix(M0)
        m,n = M0.shape
        m = 0
        for k in range(len(args)):
            Mk = args[k]
            if not isinstance(Mk,Matrix): Mk = Matrix(Mk)
            mk,nk = Mk.shape
            m += mk
            if nk != n:
                raise Exception('equal number of columns expected')
        M = Matrix(m,n)
        off = 0
        for k in range(len(args)):
            Mk = args[k]
            if not isinstance(Mk,Matrix): Mk = Matrix(Mk)
            mk,nk = Mk.shape
            assert nk == n
            for i in range(mk):
                for j in range(nk):
                    M[off+i,j] = Mk[i,j]
            off += mk
        return M

def NOT(x):
    """
    >>> A = Matrix([0,2,-1])
    >>> NOT(A)
    [1 0 0]
    """
    return 1 - (x!=0)

def AND(x,y):
    """
    >>> A = Matrix([0,1,0]);  B = Matrix([1,1,0]);
    >>> AND(A,B)
    [0 1 0]
    """
    return (x!=0)*(y!=0)

def OR(x,y):
    """
    >>> A = Matrix([0,1,0]);  B = Matrix([1,1,0]);
    >>> OR(A,B)
    [1 1 0]
    """
    return MIN(1,(x!=0)+(y!=0))

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
