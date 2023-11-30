"""
module field:
- class Field          # matrix of matrices

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

from neurotron.math.matrix import Matrix

#===============================================================================
# class Field
#===============================================================================

class Field:
    """
    class Field: implements a matrix of matrices (4-tensor)
    >>> T = Field(3,4,2,5)
    >>> T.map()
    +-000/0-+-003/3-+-006/6-+-009/9-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-001/1-+-004/4-+-007/7-+-010/A-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-002/2-+-005/5-+-008/8-+-011/B-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-------+-------+-------+-------+
    >>> K = Matrix(2,5)
    >>> T = Field([[K,K,K,K],[K,K,K,K],[K,K,K,K]])
    >>> T.map()
    +-000/0-+-003/3-+-006/6-+-009/9-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-001/1-+-004/4-+-007/7-+-010/A-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-002/2-+-005/5-+-008/8-+-011/B-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-------+-------+-------+-------+
    """

    def __init__(self,arg=None,n=None,d=None,s=None):
        arg = 1 if arg is None else arg
        if isinstance(arg,list):
            assert len(arg) > 0
            assert isinstance(arg[0],list) and len(arg[0]) > 0
            self.data = np.array(arg)
            m = len(arg); n = len(arg[0])
            d,s = self.data[0,0].shape
        else:
            m = arg
            if n is None: n = 1
            if d is None: d = 1
            if s is None: s = 1
            lst = [[Matrix(d,s) for j in range(n)] for i in range(m)]
            self.data = np.array(lst)
        self.shape = (m,n,d,s)
        self.map = self.imap

    def __getitem__(self,idx):
        """
        >>> T = Field(2,3,1,3); seed(0)
        >>> T[1,1] = rand((1,3))
        >>> T.vmap()
        +-000/0-+-002/2-+-004/4-+
        |  000  |  000  |  000  |
        +-001/1-+-003/3-+-005/5-+
        |  000  |  CKF  |  000  |
        +-------+-------+-------+
        >>> T[1,1]
        [0.548814 0.715189 0.602763]
        >>> T[3]
        [0.548814 0.715189 0.602763]
        """
        if isinstance(idx,int):
            i,j = self.kappa(idx)
        else:
            i,j = idx
        return Matrix(self.data[i,j])

    def __setitem__(self,idx,M):
        """
        >>> T = Field(2,3,1,3); seed(0)
        >>> T[1,1] = rand((1,3))
        >>> T[4] = rand((1,3))
        >>> T.vmap()
        +-000/0-+-002/2-+-004/4-+
        |  000  |  000  |  CdH  |
        +-001/1-+-003/3-+-005/5-+
        |  000  |  CKF  |  000  |
        +-------+-------+-------+
        """
        #isa = isinstance
        if isa(idx,int):
            i,j = self.kappa(idx)
        else:
            i,j = idx
        assert isa(i,int) and isa(j,int)
        if isnumber(M): M = Matrix([M])
        assert isa(M,Matrix)
        if self.data[i,j].shape != M.shape:
            raise Exception('Field.__setitem__(): size mismatch')
        self.data[i,j] = M.copy()

    def set(self,M):  # set field with flat matrix
        """
        >>> F = Field(m:=1,n:=2,d:=3,s:=4)
        >>> M = rand((m*d,n*s),10); print(M)
        [4 7 6 8 8 1 6 7; 7 8 1 5 9 8 9 4; 3 0 3 5 0 2 3 8]
        >>> F.set(M); F.imap()
        +-000/0-+-001/1-+
        | 4768  | 8167  |
        | 7815  | 9894  |
        | 3035  | 0238  |
        +-------+-------+
        """
        assert isinstance(M,Matrix)
        m,n,d,s = self.shape
        if (m*d,n*s) != M.shape:
            raise Exception('incompatible sizes')
        for i in range(m):
            for j in range(n):
                Mij = M[i*d:i*d+d,j*s:j*s+s]
                self[i,j] = Mij


    def kappa(self,i,j=None):
        """
        self.kappa():  convert matrix indices to linear index or vice versa
        >>> Field(4,10).kappa(i:=1,j:=3)   # k = i + j*m
        13
        >>> Field(4,10).kappa(k:=13)       # i = k%m, j = k//m
        (1, 3)
        """

        m,n,d,s = self.shape
        if j is None:
            k = i
            return (k%m,k//m)
        else:
            return i + j*m

    def range(self):
        m,n,d,s = self.shape
        return range(m*n)

    def permanence(self,p):    # encode permanence
        """
        self.permanence(p): convert permanence to symbolic string
        >>> o = Field(1,1)
        >>> o.permanence(0.52)
        'B'
        >>> o.permanence([-1,0,0.01,0.49,0.5,0.99,1,2])
        '<0yaAY1>'
        """
        def upper(x):
            return chr(int(65+(x-0.5)*100//2))
        def lower(x):
            return chr(int(65+32+(0.5-x)*100//2))

        if isinstance(p,list):
            s = ''
            for k in range(len(p)):
                s += self.permanence(p[k])
            return s

        if p < 0:
            return '<'
        elif p == 0:
            return '0'
        elif p == 1:
            return '1'
        elif p > 1:
            return '>'
        elif p < 0.5:
            return lower(p)
        elif p >= 0.5:
            return upper(p)
        else:
            return '?'

    def symbol(self,x):
        """
        self.symbol(x): convert index to symbol or vice versa
        >>> o = Field(1,1)
        >>> o.symbol(11)
        'B'
        >>> o.symbol([0,1,10,11,35,36,37,61,62])
        '01ABZabz062'
        """
        def symb(x):
            if x < 10:
                return chr(48+x)
            if x < 36:
                return chr(55+x)
            elif x < 62:
                return chr(61+x)
            else:
                return '%03g' % x

        if isinstance(x,int):
            return symb(x)
        elif isinstance(x,float):
           return symb(int(x))
        elif isinstance(x,list):
            s = ''
            for k in range(len(x)):
                s += self.symbol(x[k])
            return s

    def bar(self,n,label='',k=-1):          # bar string of length n
            if n >= 5:
                if k >= 0:
                    str = '%03g' % k
                    if len(label) > 0:
                        str += '/' + label
                else:
                    str = '---'
                while len(str) < n:
                    str += '-'
                    if len(str) < n: str = '-' + str
                return str
            if n >= 3:
                label = '-' + label
            elif n >= 5:
                label = '-' + label
            str = label
            for k in range(n-len(label)): str += '-'
            return str

    def head(self,i,n,s,width=0):
        line = '+'
        #s = _max(s,width)
        s = s if width == 0 else width
        for j in range(n):
            if i < 0:
                sym = ''
                line += self.bar(s,'') + '+'
            else:
                k = self.kappa(i,j)
                sym = self.symbol(k)
                line += self.bar(s,sym,k) + '+'
        return line

    def state(self,s):        # state string from state matrix
        B = s[0];  D = s[1];  L = s[2];  Q = s[3];
        S = s[4];  U = s[5];  X = s[6];  Y = s[7];

        UQ = 'Q' if Q else 'U'
        SL = 'L' if L else 'S'
        DB = 'B' if B else 'D'

        str = ''
        str += UQ if U or Q else '-'
        str += 'X' if X else '-'
        str += SL if S or L else '-'
        str += DB if D or B else '-'
        str += 'Y' if Y else '-'

        return str

    def _table(self,kind,I,m,n,width=0,label=''):    # print table
        """
        self.table('i',...) # for indices
        self.table('p',...) # for permanences
        self.table('w',...) # for synaptic weights
        self.table('s',...) # for state matrices
        """
        def title(n,x):
            return '-%03g-' % x

        def row(kind,I,i,j,d,s,width):
            #return '12345'
            if kind == 's':
                #print('##### I:',I)
                str = self.state(I)
            else:
                str = ''
                for nu in range(s):
                   if kind == 'i':   # index
                       str += self.symbol(I[nu])
                   elif kind == 'p': # permanence
                       str += self.permanence(I[nu])
                   elif kind == 'w': # permanence
                       str += '1' if I[nu] > 0.5 else '0'
                   else:
                       str += '?'

            while len(str) < width:
                str = str + ' '
                if len(str) < width: str = ' ' + str
            return str

        #cells = self.cluster
        d = len(I[0][0])
        s = len(I[0][0][0])

        tab = ''
        for k in range(len(label)):
            tab += ' '

        str = ''
        for i in range(m):
            head = self.head(i,n,s,width)
            trailer = label if i == 0 else tab
            print(trailer+head)
            for mu in range(d):
                line = tab + '|'
                for j in range(n):
                    line += row(kind,I[i][j][mu],i,j,mu,s,width) + '|'
                print(line)
        print(tab+self.head(-1,n,s,width))

    def vmap(self,label=''):
        m,n,d,s = self.shape
        self._table('p',self.data,m,n,width=_max(s,7),label=label)

    def imap(self,label=''):
        m,n,d,s = self.shape
        self._table('i',self.data,m,n,width=_max(s,7),label=label)

    def smap(self,label=''):  # state map
        m,n,d,s = self.shape
        self._table('s',self.data,m,n,width=7,label=label)

    def _Gmap(self):
        m,n,d,s = self.shape
        self._table('i',self.cluster.G,m,n,width=_max(s,7),label='')

    def _Wmap(self):
        m,n,d,s = self.shape
        self._table('w',self.cluster.P,m,n,width=_max(s,7),label='')

#===============================================================================
# unit tests
#===============================================================================

def _case4a():
    """
    >>> T = Field(1)
    >>> T.imap()
    +-000/0-+
    |   0   |
    +-------+
    >>> K = Matrix(2,5)
    >>> T = Field([[K,K,K,K],[K,K,K,K],[K,K,K,K]])
    >>> T.imap()
    +-000/0-+-003/3-+-006/6-+-009/9-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-001/1-+-004/4-+-007/7-+-010/A-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-002/2-+-005/5-+-008/8-+-011/B-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-------+-------+-------+-------+
    >>> M = T[1,1]; print(M)
    [0 0 0 0 0; 0 0 0 0 0]
    >>> M[1,2] = 8
    >>> T[1,1] = M; T.imap()
    +-000/0-+-003/3-+-006/6-+-009/9-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-001/1-+-004/4-+-007/7-+-010/A-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00800 | 00000 | 00000 |
    +-002/2-+-005/5-+-008/8-+-011/B-+
    | 00000 | 00000 | 00000 | 00000 |
    | 00000 | 00000 | 00000 | 00000 |
    +-------+-------+-------+-------+
    >>> P = Field(2,2,1,3);
    >>> m,n,d,s = P.shape; seed(0)
    >>> P[0,0] = rand((1,3))
    >>> P[0,1] = rand((1,3))
    >>> P[1,0] = rand((1,3))
    >>> P[1,1] = rand((1,3))
    >>> P.map = P.vmap; P.map()
    +-000/0-+-002/2-+
    |  CKF  |  CdH  |
    +-001/1-+-003/3-+
    |  dTX  |  fOB  |
    +-------+-------+
    """

def _case6b():
    """
    >>> F = Field(1,3,1,1); F.map()
    +-000/0-+-001/1-+-002/2-+
    |   0   |   0   |   0   |
    +-------+-------+-------+
    >>> F[0] = 1; F.map()
    +-000/0-+-001/1-+-002/2-+
    |   1   |   0   |   0   |
    +-------+-------+-------+
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
