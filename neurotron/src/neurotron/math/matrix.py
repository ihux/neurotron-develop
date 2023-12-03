"""
module matrix:
- class Matrix         # MATLAB style matrix class (NumPy based)
- class Field          # matrix of matrices

Matrix methods:
- construct             # Matrix construction
- kappa                 # conversion between linear <-> quadratic index
- transpose             # matrix transposition
- indexing              # by scalar index or index pair
- slicing               # indexing by slices
- column                # convert matrix to column
- reshape               # reshape matrix
- string representation # represent matrix as a string
- mul                   # element wise matrix multiplication
- matmul                # algebraic matrix multiplication

Field methods:
- construct             # Field construction
- kappa                 # conversion between linear <-> quadratic index
- permanence            # cnvert permanence to symbolic string
- symbol                # convert symbol to index or vice versa
- bar                   # create a labeled bar
- head                  # create a cell head
- imap                  # create index map
- vmap                  # create value map
"""

import numpy as np
#import neurotron.matrix.matfun as mf
isa = isinstance        # shorthand

#===============================================================================
# class Matrix
#===============================================================================

class Matrix(np.ndarray):
    """
    class Matrix: matrix wrapper for NumPy arrays
    >>> Matrix(0,0)
    []
    >>> Matrix(2,3)
    [0 0 0; 0 0 0]
    >>> Matrix([1,2,3])
    [1 2 3]
    >>> Matrix([[1,2,3],[4,5,6]])
    [1 2 3; 4 5 6]
    >>> Matrix(range(5))
    [0 1 2 3 4]

    See also: Matrix, eye, zeros, ones
    """
    def __new__(cls, arg1=None, arg2=None, data=None):
        #isa = isinstance
        arg1 = [] if arg1 is None else arg1
        if isa(arg1,int) and arg2 is None:
            arg1 = [[arg1]]
        elif isa(arg1,float) and arg2 is None:
            arg1 = [[arg1]]
        elif isa(arg1,np.ndarray):
            if len(arg1.shape) == 1:
                arg1 = [arg1]
        elif isa(arg1,int) and isa(arg2,int):
            arg1 = np.zeros((arg1,arg2))
        elif isa(arg1,list):
            if arg1 == []:
                arg1 = np.zeros((0,0))  #[[]]
            elif not isa(arg1[0],list):
                arg1 = [arg1]
        elif isa(arg1,range):
            arg1 = np.array([arg1])
            #print('### arg1:',arg1)
            return Matrix(arg1)
        else:
            raise Exception('bad arg')

        obj = np.asarray(arg1).view(cls)
        obj.custom = data
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.custom = getattr(obj, 'custom', None)

    def kappa(self,i,j=None):
        """
        Matrix.kappa():  convert matrix indices to linear index or vice versa
        >>> Matrix(4,10).kappa(i:=1,j:=3)   # k = i + j*m
        13
        >>> Matrix(4,10).kappa(k:=13)       # i = k%m, j = k//m
        (1, 3)
        """
        m,n = self.shape
        if j is None:
            k = i
            return (k%m,k//m)
        else:
            return i + j*m

    def range(self):
        m,n = self.shape
        return range(m*n)

    def _isa(self,obj,typ=None):
        if typ is None:
            print(type(obj),type(obj).__name__)
        return (type(obj).__name__ == typ)

    def __str__(self,wide=False):   # string representation of list or matrix
        m,n = self.shape
        txt = '[';  sepi = ''
        for i in range(0,m):
            txt += sepi;  sepi = '; ';  sepj = ''
            for j in range(0,n):
                if wide == False:
                    txt += sepj + "%g" % self[i,j]
                else:
                    s = "%4g" %M[i,j].item()
                    s = s if s[0:2] != '0.' else s[1:]
                    s = s if s[0:3] != '-0.' else '-'+s[2:]
                    txt += "%5s" % s
                sepj = ' '
        txt += ']'
        return txt

    def __repr__(self):
        return self.__str__()

    def _transpose(self):
        return np.transpose(self)

#    def __max__(self):
#       m,n = self.shape
#        return 0

    def __getitem__(self,idx):
        """
        >>> A = _magic(4)[:3,:]; print(A.T)
        [16 5 9; 2 11 7; 3 10 6; 13 8 12]
        >>> K = Matrix([[2,1,0],[5,4,3]]); print(K)
        [2 1 0; 5 4 3]
        >>> A[K]
        [9 5 16; 7 11 2]
        >>> A[1,:]
        [5 11 10 8]
        >>> A[:,2]
        [3; 10; 6]
        """
        #isa = isinstance  # shorthand
        if isa(idx,int):
            i,j = self.kappa(idx)
            result = super().__getitem__((i,j))
            iresult = int(result)
            if result == iresult: return iresult
            return result
        elif isa(idx,tuple):
            i,j = idx;
            m,n = self.shape
            if isa(i,int) and isa(j,slice):
                if i < 0 or i >= m:
                    raise Exception('row index out of range')
                idx = (slice(i,i+1,None),j)
            elif isa(i,slice) and isa(j,int):
                if j < 0 or j >= n:
                    raise Exception('column index out of range')
                idx = (i,slice(j,j+1,None))
        elif isa(idx,Matrix):
            #print('Matrix:',idx)
            m,n = idx.shape
            result = Matrix(m,n)
            for i in range(m):
                for j in range(n):
                    k = idx[i,j]
                    mu,nu = self.kappa(k)
                    result[i,j] = super().__getitem__((mu,nu))
                    #print('result[%g,%g]'%(i,j), 'k:',k,'(mu,nu)',(mu,nu))
            return result
        result = super().__getitem__(idx)
        if isa(result,np.int64) or isa(result,np.float64):
            iresult = int(result)
            if result == iresult: return iresult
        return result

    def __setitem__(self,idx,value):
        """
        >>> M = Matrix(2,3)
        >>> M[1,0] = 5; print(M)
        [0 0 0; 5 0 0]
        >>> M[3] = -2; print(M)
        [0 0 0; 5 -2 0]
        >>> idx = Matrix(range(4))
        >>> M[idx] = idx; print(M)
        [0 2 0; 1 3 0]
        """
        if isinstance(idx,Matrix):
            if not isinstance(value,Matrix):
                raise Exception('Matrix expected for assigned value')
            #print('idx:',idx)
            mx,nx = idx.shape;  mv,nv = value.shape
            if mv*nv != mx*nx:
                raise Exception('mismatching number of elements')
            for k in range(mv*nv):
                self[idx[k]] = value[k]
            return
        elif isinstance(idx,int):
            idx = self.kappa(idx)
        super().__setitem__(idx,value)

    def __call__(self): # convert to column vector
        """
        A = _magic(2)
        A()
        [1; 3; 4; 2]
        """
        m,n = self.shape
        out = Matrix(m*n,1)
        for i in range(m):
            for j in range(n):
                k = self.kappa(i,j)
                out[k,0] = super().__getitem__((i,j))
        return out

    def __mul__(self,other):
        """
        >>> A = _magic(2); B = A.T; print(A)
        [1 3; 4 2]
        >>> A*B
        [1 12; 12 4]
        >>> A*5
        [5 15; 20 10]
        >>> 3*A
        [3 9; 12 6]
        """
        #isa = isinstance
        if isa(other,Matrix):
            if self.shape != other.shape:
                raise Exception('Matrix.__mul__: incompatible sizes')
        return super().__mul__(other)

    def _not(self):
        """
        >>> Matrix([[1,-1,2],[0,0,0]])._not()
        [0 0 0; 1 1 1]
        """
        return 1 - (self != 0)

    def reshape(self,m,n): # convert to column vector
        """
        >>> A = _magic(4)[:3,:]; print(A)
        [16 2 3 13; 5 11 10 8; 9 7 6 12]
        >>> B = A(); print(B)
        [16; 5; 9; 2; 11; 7; 3; 10; 6; 13; 8; 12]
        >>> B[2]
        9
        >>> B.reshape(3,4)
        [16 2 3 13; 5 11 10 8; 9 7 6 12]
        >>> B.reshape(6,2)
        [16 3; 5 10; 9 6; 2 13; 11 8; 7 12]
        >>> B.reshape(2,6)
        [16 9 11 3 6 8; 5 2 7 10 13 12]
        >>> B.reshape(1,12)
        [16 5 9 2 11 7 3 10 6 13 8 12]
        """
        v = self()  # convert to column
        #print('### shape:',v.shape,'v:',v)
        mn = v.shape[0]
        if mn != m*n:
            raise Exception('incompatible dimensions for reshape')
        out = Matrix(m,n)
        for k in range(mn):
            i,j = out.kappa(k)
            #print('### i,j:',i,j)
            out[i,j] = v[k,0]
        return out

    def list(self):
        """
        convert to list
        >>> _magic(3).list()
        [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        """
        m,n = self.shape
        return [[self[i,j] for j in range(n)] for i in range(m)]

    T = property(fget=_transpose)
    N = property(fget=_not)

#===============================================================================
# helper
#===============================================================================

def _magic(n):
    """
    >>> _magic(0)
    []
    >>> _magic(1)
    1
    >>> _magic(2)
    [1 3; 4 2]
    >>> _magic(3)
    [8 1 6; 3 5 7; 4 9 2]
    >>> _magic(4)
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

def _MAX(arg1,arg2=None):
    """
    >>> _MAX(2,3)
    3
    >>> _MAX(2,3.6)
    3.6
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> _MAX(A,B)
    [8 3 -2; 1 2 -1]
    >>> _MAX(A)
    [1 3 -1]
    >>> _MAX(2,A)
    [2 3 2; 2 2 2]
    >>> _MAX(B,1)
    [8 2 1; 1 1 1]
    >>> x = _magic(2)();  print(x)
    [1; 4; 3; 2]
    >>> _MAX(x)
    4
    >>> _MAX(x.T)
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

def _MIN(arg1,arg2=None):
    """
    >>> _MIN(2,3)
    2
    >>> _MIN(2.1,3)
    2.1
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> B = Matrix([[8,2,-3],[1,0,-2]])
    >>> _MIN(A,B)
    [1 2 -3; 0 0 -2]
    >>> _MIN(A)
    [0 2 -2]
    >>> _MIN(2,B)
    [2 2 -3; 1 0 -2]
    >>> _MIN(A,1)
    [1 1 -2; 0 1 -1]
    >>> x = _magic(2)();  print(x)
    [1; 4; 3; 2]
    >>> _MIN(x)
    1
    >>> _MIN(x.T)
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
                mini = min(arg1[i,j],maxi)
            M[0,j] = mini
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

#===============================================================================
# unit tests
#===============================================================================

def _case1():
    """
    >>> Matrix([])
    []
    >>> Matrix(0,0)
    []
    >>> Matrix(0,1)
    []
    >>> Matrix(0,0)
    []
    """

def _case2():
    """
    >>> Matrix()
    []
    >>> Matrix([])
    []
    >>> Matrix(0,0)
    []
    >>> Matrix(0,1)
    []
    >>> Matrix(17)
    [17]
    >>> Matrix(3.14)
    [3.14]
    """

def _case3():
    """
    >>> A = Matrix([[1,2,3],[4,5,6]])
    >>> A
    [1 2 3; 4 5 6]
    >>> A._transpose()
    [1 4; 2 5; 3 6]
    >>> A.T
    [1 4; 2 5; 3 6]
    """

def _case4b():
    """
    >>> A = Matrix([[1,3,-2],[0,2,-1]])
    >>> _MAX(0,_MIN(A,1))
    [1 1 0; 0 1 0]
    """

def _case5a():  # indexing with slices
    """
    >>> A = _magic(4); print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    >>> A[0,0]
    16
    >>> B = A[:3,:]; print(B)
    [16 2 3 13; 5 11 10 8; 9 7 6 12]
    >>> B[0,:]
    [16 2 3 13]
    >>> B[1,:]
    [5 11 10 8]
    >>> B[2,:]
    [9 7 6 12]
    >>> B[:,0]
    [16; 5; 9]
    >>> B[:,1]
    [2; 11; 7]
    >>> B[:,2]
    [3; 10; 6]
    >>> B[:,3]
    [13; 8; 12]
    """

def _case5b():  # indexing with slices, column ranges
    """
    >>> A = _magic(4); print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    >>> B = A[:3,:]; print(B)
    [16 2 3 13; 5 11 10 8; 9 7 6 12]
    >>> B[:,:]
    [16 2 3 13; 5 11 10 8; 9 7 6 12]
    >>> B[:,:2]
    [16 2; 5 11; 9 7]
    >>> B[:,1:4:2]
    [2 13; 11 8; 7 12]
    """
def _case5c():  # indexing with slices, row ranges
    """
    >>> A = _magic(4); print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    >>> C = A[:3,:].T; print(C)
    [16 5 9; 2 11 7; 3 10 6; 13 8 12]
    >>> C[:,:]
    [16 5 9; 2 11 7; 3 10 6; 13 8 12]
    >>> C[:2,:]
    [16 5 9; 2 11 7]
    >>> C[1:4:2,:]
    [2 11 7; 13 8 12]
    """
def _case5d():  # indexing with slices, row & column ranges
    """
    >>> A = _magic(4); print(A)
    [16 2 3 13; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    >>> A[:2,:2]
    [16 2; 5 11]
    >>> A[1:4:2,1:3]
    [11 10; 14 15]
    >>> A[1:3,1:4:2]
    [11 8; 7 12]
    """

def _case5e():
    """
    >>> M=_magic(4)
    >>> M[0,:4] = Matrix(range(4)); print(M)
    [0 1 2 3; 5 11 10 8; 9 7 6 12; 4 14 15 1]
    >>> M[:4,1]= 5+Matrix(range(4)).T; print(M)
    [0 5 2 3; 5 6 10 8; 9 7 6 12; 4 8 15 1]
    """

def _case6a():
    """
    >>> Matrix(True)
    [1]
    >>> Matrix(False)
    [0]
    >>> Matrix(2)
    [2]
    >>> Matrix(1.5)
    [1.5]
    """

#===============================================================================
# unit tests logical matrix operations
#===============================================================================

def _case7a():
    """
    >>> A = Matrix([[1,-1,2],[0,0,0]]); print(A)
    [1 -1 2; 0 0 0]
    >>> A.N
    [0 0 0; 1 1 1]
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
