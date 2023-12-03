"""
module neurotron.cluster.cluster
    class Cluster  # simulate a cluster of Neurotrons
    class Token    # wrapper for token dicts
"""

from neurotron.math.attribute import Attribute
from neurotron.math.matrix import Matrix
from neurotron.math.field import Field
from neurotron.math.matfun import ROW, SEED, ZEROS, AND, OR, NOT
from neurotron.cluster.terminal import Terminal
from neurotron.cluster.setup import Collab,Excite,Predict
from neurotron.cluster.monitor import Monitor, Record
isa = isinstance

#=========================================================================
# class Token
#=========================================================================

class Token(dict):
    def __init__(self,arg=None):
        self.dict = arg if arg is not None else {}
    def __getitem__(self,key):
        return self.dict[key]

#=========================================================================
# class Out
#=========================================================================

class Out:
    def __init__(self,cluster,i,j,tag):
        self.cluster = cluster
        self.i = i
        self.j = j
        self.tag = tag

    def out(self):
        data = self.cluster.get(self.tag)
        return data[self.i,self.j]

#=========================================================================
# class Cell
#=========================================================================

class Cell(Attribute):
    def __init__(self,cluster,i,j,delta=(0.1,0.1)):
        """
        class Cell: access state attributes of cells[i,j]
        >>> cell = Cell(Cluster(),1,1)
        >>> cell.u = 1
        """
        tags = ['u','q','d','b','x','y','s','l']
        for tag in tags:
            self.set(tag,Out(cluster,i,j,tag.upper()))
        self.predict = None
        self._delta = delta

    def delta(self):
        return self._delta

    def state(self):
        tags = ['b','d','l','q','s','u','x','y']
        dict = {}
        for tag in tags:
            dict[tag] = self.get(tag).out()
        return dict

#=========================================================================
# class Cluster
#=========================================================================

class Cluster(Attribute):
    verbose = 0
    def __init__(self,m=4,n=10,d=2,s=5,f=None,verbose=0,rand=True):
        if f is None: f = n
        self.shape = (m,n,d,s)
        self.sizes = (f,n*m)               # (M,N)
        self.cdx = Matrix(range(m*n))      # access context vector
        self.fdx = m*n+Matrix(range(f))    # access feedforward vector
        self.k = Matrix(range(n*m))
        self.verbose = verbose

        self._excite = Terminal(m,n)       # simple excite terminal
        self._collab = Terminal(Collab(m,n,d,s))
        self._predict = Terminal(Predict(m,n,d,s,rand=rand),verbose=verbose)

        self.U = Matrix(m,n)
        self.Q = Matrix(m,n)
        self.D = Matrix(m,n)
        self.B = Matrix(m,n)
        self.X = Matrix(m,n)
        self.Y = Matrix(m,n)
        self.S = Matrix(m,n)
        self.L = Matrix(m,n)

    def __len__(self):
        m,n,d,s = self.shape
        return m*n

    def __getitem__(self,idx):
        if isa(idx,int): idx = self.kappa(idx)
        cell = Cell(self,*idx,self._predict.delta)
        return cell

    def range(self):
        return range(self.sizes[1])

    def zero(self):
        return Matrix(*self.shape[:2])

    def split(self,y):    # split y int context c and feedforward f
        """
        >>> cells = Cluster(3,4,2,5,7)
        >>> y = ROW([1,1,1,0,0,0,1,1,1,0,0,0],[1,0,1,0,1,0,1])
        >>> cells.split(y)
        ([1 1 1 0 0 0 1 1 1 0 0 0], [1 0 1 0 1 0 1])
        """
        return (y[self.cdx],y[self.fdx])

    def kappa(self,i,j=None):
        """
        self.kappa():  convert matrix indices to linear index or vice versa
        >>> o = Cluster(m=4,n=10)
        >>> k = o.kappa(i:=1,j:=3); print(k)  # k = i+j*m
        13
        >>> ij = o.kappa(k:=13);  print(ij)   # i = k%m, j = k//m
        (1, 3)
        """

        m,n,d,s = self.shape
        if j is None:
            k = i
            return (k%m,k//m)
        else:
            return i + j*m

    def state(self,i,j):
        tags = ['B','D','L','Q','S','U','X','Y']
        s = Matrix(1,len(tags))
        for k in range(len(tags)):
            s[k] = self.get(tags[k])[i,j]
        return s

    def smap(self,label=''):
        m,n,d,s = self.shape
        S = Field(m,n,1,8)
        for k in range(m*n):
            S[k] = self.state(*self.kappa(k))
        S.smap(label)

    def map(self):
        self.K.imap('K: ')     # Map(self).Kmap()
        self.P.vmap('P: ')

    def update(self,y):        # update y
        y[self.k] = self.Y
        return y

    def relax(self,y):
        #M,N = self.sizes
        #m,n,d,s = self.shape
        #c = y[:N];  f = y[N:N+M];
        Z = self.zero()
        self.set('U,Q,D,B,Y,S',(Z,Z,Z,Z,Z,Z))
        return self.update(y)

    def stimu(self,y):
        c,f = self.split(y)
        self.U = self._excite(f)
        return y

    def react(self,y):
        self.Y = self.U * self.X
        self.L = self.X * self.Y
        self._predict.learn(self.L)
        return self.update(y)

    def depress(self,y):
        c,f = self.split(y)
        self.D = self._collab(c)
        #self.L = self.zero()
        return y

    def excite(self,y):
        self.Q = self.U.copy()
        return y

    def burst(self,y):
        self.B = AND(NOT(self.D),self.Q)
        self.Y = OR(self.Y,self.B)
        return self.update(y)

    def predict(self,y):
        c,f = self.split(y)
        self.S = self._predict(c)
        self.X = self.S
        #for k in self.range():
        #    if self.S[k]: print('mind I[%g]:'%k,self._predict.I[k])
        return y

    def clear(self,M):
        m,n,d,s = self.shape
        M = Matrix(m,n)

    #def idle(self):
    #    clear(self.B);  clear(self.D);  clear(self.L);  clear(self.Q)
    #    clear(self.S);  clear(self.U);  clear(self.X);  clear(self.Y)
    #    for k in range(self.sizes[1]):
    #        y[k] = self.Y[k]
    #    return y

    def plot(self,mon,subplot=0,title=None,label=None):
        m,n,d,s = self.shape
        for i in range(m):
            for j in range(n):
                cell = Cell(self,i,j)
                if label is not None:
                    k = self.kappa(i,j)
                    mon(cell,i+subplot*(m+1),j,k)
                else:
                    mon(cell,i+subplot*(m+1),j)
        if title is not None:
            mon.title(title)

    def draw(self,mon,subplot=0):
        self.plot(mon,subplot,label=True)

    def iterate(self,y):
        y = self.relax(y);
        y = self.stimu(y);
        y = self.react(y);
        y = self.depress(y);
        y = self.excite(y);
        y = self.burst(y);
        y = self.predict(y);
        return y

    def step(self,mon,y,tag='',log=None):
        y = self.iterate(y)
        m,n,d,s = self.shape
        self.draw(mon);  mon.title(tag)
        return y

    def apply(self,y,tag='',log=None,all=None):
        m,n,d,s = self.shape
        y = self.relax(y);
        y = self.stimu(y);
        prefix = tag + ' - ' if tag != '' else ''
        if log is not None:
            print('stimu ...');  self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            self.draw(mon,0);  mon.title(prefix+'stimu')

        y = self.react(y);
        if log is not None:
            print('ract ...');  self.smap()
        if all is not None:
            self.draw(mon,1);  mon.xlabel(n/2-0.5,prefix+'react')
        else:
            mon = Monitor(2*m+1,n);
            self.draw(mon,0);  mon.title(prefix+'react')

        y = self.depress(y);
        if log is not None:
            print('depress ...');  self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            self.draw(mon,0);  mon.title(prefix+'depress')

        y = self.excite(y);
        if log is not None:
            print('excite ...');   self.smap()
        if all is not None:
            self.draw(mon,1);  mon.xlabel(n/2-0.5,prefix+'excite')

        y = self.burst(y);
        if log is not None:
            print('burst ...');    self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            self.draw(mon,0);  mon.title(prefix+'burst')

        y = self.predict(y);
        if log is not None:
            print('predict ...');  self.smap()
        if all is not None:
            self.draw(mon,1);  mon.xlabel(n/2-0.5,prefix+'predict')
        else:
            self.draw(mon,1);  mon.xlabel(n/2-0.5,prefix+'predict')

        #y = self.relax(y);
        #if log is not None:
        #    print('relax ...');    self.smap()
        #if all is not None:
        #    mon = Monitor(2*m+1,n);
        #    self.plot(mon,0);  mon.title(prefix+'relax')
        return y

#===============================================================================
# unit tests
#===============================================================================

def _test_mary():
    """
    >>> token = {'Mary': [1,0,0,0,0,0,0,1,1]}
    >>> shape = (2,9,2,5); m,n,d,s = shape
    >>> SEED(1);  cells = Cluster(*shape,verbose=1)
    >>> cells.X[0] = 1; cells._predict.I[0] = Matrix([[.1,0,.1,0,.1],[0,0,0,0,0]])
    >>> y = ROW(ZEROS(1,m*n),token['Mary'])
    >>> y = cells.stimu(y);  cells.smap();  print(y)
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | UX--- | ----- | ----- | ----- | ----- | ----- | ----- | U---- | U---- |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | U---- | ----- | ----- | ----- | ----- | ----- | ----- | U---- | U---- |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1]
    >>> y = cells.react(y);  cells.smap();  print(y)
    learn P[0].0: [0.85 1 1 0.6 0.5] by [0.1 0 0.1 0 0.1]
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | UXL-Y | ----- | ----- | ----- | ----- | ----- | ----- | U---- | U---- |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | U---- | ----- | ----- | ----- | ----- | ----- | ----- | U---- | U---- |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1]
    >>> y = cells.excite(y);  cells.smap();  print(y)
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | QXL-Y | ----- | ----- | ----- | ----- | ----- | ----- | Q---- | Q---- |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | Q---- | ----- | ----- | ----- | ----- | ----- | ----- | Q---- | Q---- |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1]
    >>> y = cells.burst(y);  cells.smap();  print(y)
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | QXLBY | ----- | ----- | ----- | ----- | ----- | ----- | Q--BY | Q--BY |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | Q--BY | ----- | ----- | ----- | ----- | ----- | ----- | Q--BY | Q--BY |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 1 1]
    >>> y = cells.predict(y);  cells.smap();  print(y)
    mind I[11].0: [0.1 0.1 -0.1 0.1 -0.1]
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | Q-LBY | ----- | ----- | ----- | ----- | ----- | ----- | Q--BY | Q--BY |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | Q--BY | ----- | ----- | ----- | ----- | -XS-- | ----- | Q--BY | Q--BY |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 1 1]
    >>> y = cells.relax(y);  cells.smap();  print(y)
    +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+-010/A-+-012/C-+-014/E-+-016/G-+
    | --L-- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
    +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+-011/B-+-013/D-+-015/F-+-017/H-+
    | ----- | ----- | ----- | ----- | ----- | -X--- | ----- | ----- | ----- |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1]
    """

def test_record():
    """
    >>> cells = Cluster(2,7,2,5)
    >>> cells.U[0] = cells.X[0] = 1
    >>> record = Record(cells)
    >>> record(cells)
    >>> record.pattern()
    '|UX|-|-|-|-|-|-|-|-|-|-|-|-|-|'
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
