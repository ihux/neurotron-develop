"""
module matfun: Matrix functions:
- eye                   # unit matrix
- isnumber              # is arg a number?
- zeros                 # zero matrix
- one                   # one matrix
- rand                  # random matrix
- seed                  # set random seed
- max                   # row of column maxima
- min                   # row of column minima
- size                  # matrix sizes
- magic                 # magic matrix
- sum                   # row of column sum
- any                   # row of column any's
- all                   # row of column all's
- length                # maximum size
- isempty               # check if matrix is empty
- NOT                   # logical not
- AND                   # logical and
- OR                    # logical OR

"""

import numpy as np
#import matrix as mx
from neurotron.matrix.matrix import Matrix
isa = isinstance

#===============================================================================
# helper functions
#===============================================================================

def _max(x,y):
    return x if x > y else y

def _min(x,y):
    return x if x < y else y

#===============================================================================
# matrix functions
#===============================================================================

def eye(n):
    """
    >>> eye(3)
    [1 0 0; 0 1 0; 0 0 1]
    """
    I = Matrix(n,n)
    for k in range(n):
        I[k,k] = 1
    return I

def isnumber(arg):
    """
    >>> isnumber(5) and isnumber(3.14)
    True
    >>> isnumber(True) and isnumber(False)
    True
    >>> isnumber('abc') or isnumber([])
    False
    """
    if isa(arg,int) or isa(arg,float): return True
    if isa(arg,np.int64) or isa(arg,np.float64): return True
    if isa(arg,bool): return True
    return False

def zeros(m,n=None):
    """
    >>> zeros(3)
    [0 0 0; 0 0 0; 0 0 0]
    >>> zeros(2,4)
    [0 0 0 0; 0 0 0 0]
    """
    n = m if n is None else n
    if m == 0 or n == 0:
        return Matrix(m,n)
    return Matrix(m,n)

def ones(m,n=None):
    """
    >>> ones(3)
    [1 1 1; 1 1 1; 1 1 1]
    >>> ones(2,3)
    [1 1 1; 1 1 1]
    >>> ones(0,0)
    []
    """
    n = m if n is None else n
    if m == 0 or n == 0:
        return Matrix(m,n)
    return Matrix(m,n) + 1

def rand(arg=None,modulus=None):
    """
    >>> seed(0)
    >>> rand((2,2))
    [0.548814 0.715189; 0.602763 0.544883]
    >>> rand((2,3))
    [0.423655 0.645894 0.437587; 0.891773 0.963663 0.383442]
    >>> rand((0,0))
    []
    >>> rand(8)
    6
    >>> rand()
    0.8121687287754932
    >>> rand((2,3),40)
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

def seed(s):
    """
    seed(): set random seed
    >>> seed(0)
    """
    np.random.seed(s)

def size(arg):
    """
    size(): matrix sizes
    >>> size(3.14)
    (1, 1)
    >>> size(Matrix(3,5))
    (3, 5)
    >>> size([])
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

def max(arg1,arg2=None):
    """
    >>> max(2,3)
    3
    >>> max(2,3.6)
    3.6
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> max(A,B)
    [8 3 -2; 1 2 -1]
    >>> max(A)
    [1 3 -1]
    >>> max(2,A)
    [2 3 2; 2 2 2]
    >>> max(B,1)
    [8 2 1; 1 1 1]
    >>> x = magic(2)();  print(x)
    [1; 4; 3; 2]
    >>> max(x)
    4
    >>> max(x.T)
    4
    """
    scalar1 = isinstance(arg1,int) or isinstance(arg1,float)
    scalar2 = isinstance(arg2,int) or isinstance(arg2,float)

    if scalar1:
        if arg2 is None:
            return arg1
        elif scalar2:
            return _max(arg1,arg2)
        else:
            arg1 = arg1 + 0*arg2
    elif scalar2:
        arg2 = arg2 + 0*arg1

    m,n = arg1.shape
    if arg2 is None:
        if m == 1:
            s = arg1[0,0]
            for j in range(1,n): s = _max(s,arg1[0,j])
            return int(s) if s == int(s) else s
        elif n == 1:
            s = arg1[0,0]
            for i in range(m): s = _max(s,arg1[i,0])
            return int(s) if s == int(s) else s
        M = Matrix(1,n)
        for j in range(n):
            maxi = arg1[0,j]
            for i in range(1,m):
                maxi = _max(arg1[i,j],maxi)
            M[0,j] = maxi
    else:
        assert arg1.shape == arg2.shape
        M = Matrix(m,n)
        for i in range(m):
            for j in range(n):
                M[i,j] = _max(arg1[i,j],arg2[i,j])
    m,n = M.shape
    if m != 1 or n != 1:
        return M
    result = M.item()
    iresult = int(result)
    return iresult if iresult == result else result

def min(arg1,arg2=None):
    """
    >>> min(2,3)
    2
    >>> min(2.1,3)
    2.1
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> min(A,B)
    [1 2 -3; 0 0 -2]
    >>> min(A)
    [0 2 -2]
    >>> min(2,B)
    [2 2 -3; 1 0 -2]
    >>> min(A,1)
    [1 1 -2; 0 1 -1]
    >>> x = magic(2)();  print(x)
    [1; 4; 3; 2]
    >>> min(x)
    1
    >>> min(x.T)
    1
    """
    scalar1 = isinstance(arg1,int) or isinstance(arg1,float)
    scalar2 = isinstance(arg2,int) or isinstance(arg2,float)

    if scalar1:
        if arg2 is None:
            return arg1
        elif scalar2:
            return _min(arg1,arg2)
        else:
            arg1 = arg1 + 0*arg2
    elif scalar2:
        arg2 = arg2 + 0*arg1

    m,n = arg1.shape
    if arg2 is None:
        if m == 1:
            s = arg1[0,0]
            for j in range(1,n): s = _min(s,arg1[0,j])
            return int(s) if s == int(s) else s
        elif n == 1:
            s = arg1[0,0]
            for i in range(m): s = _min(s,arg1[i,0])
            return int(s) if s == int(s) else s
        M = Matrix(1,n)
        for j in range(n):
            maxi = arg1[0,j]
            for i in range(1,m):
                maxi = _min(arg1[i,j],maxi)
            M[0,j] = maxi
    else:
        assert arg1.shape == arg2.shape
        M = Matrix(m,n)
        for i in range(m):
            for j in range(n):
                M[i,j] = _min(arg1[i,j],arg2[i,j])
    m,n = M.shape
    if m != 1 or n != 1:
        return M
    result = M.item()
    iresult = int(result)
    return iresult if iresult == result else result

def magic(n):
    """
    >>> magic(0)
    []
    >>> magic(1)
    1
    >>> magic(2)
    [1 3; 4 2]
    >>> magic(3)
    [8 1 6; 3 5 7; 4 9 2]
    >>> magic(4)
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

def sum(arg):
    """
    >>> sum(2)
    2
    >>> sum(3.14)
    3.14
    >>> sum([1,2,3])
    6
    >>> A = magic(4)[:3,:];  print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12]
    >>> sum(A)
    [30 20 19 33]
    >>> sum(A[:,1])
    20
    >>> sum(A[2,:])
    34
    >>> sum(True)
    1
    >>> C=ones(1,4)
    >>> sum(C>0)
    4
    """
    #isa = isinstance
    if isa(arg,int) or isa(arg,np.int64) or isa(arg,float):
        return arg
    elif isa(arg,list):
        M = Matrix(arg)
        return sum(M)
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

def row(*args):
    """
    >>> M = magic(4)
    >>> M1 = M[0:2,:];  print(M1)
    [16 2 3 13; 5 11 10 8]
    >>> M2 = M[2:4,:];  print(M2)
    [9 7 6 12; 4 14 15 1]
    >>> row(M1,M2)
    [16 2 3 13 9 7 6 12; 5 11 10 8 4 14 15 1]
    >>> row([1,2],[3,4])
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

def column(*args):
    """
    >>> M = magic(4)
    >>> M1 = M[:,0:2];  print(M1)
    [16 2; 5 11; 9 7; 4 14]
    >>> M2 = M[:,2:4];  print(M2)
    [3 13; 10 8; 6 12; 15 1]
    >>> column(M1,M2)
    [16 2; 5 11; 9 7; 4 14; 3 13; 10 8; 6 12; 15 1]
    >>> column(Matrix([1,2]).T,Matrix([3,4]).T)
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
    return min(1,(x!=0)+(y!=0))
