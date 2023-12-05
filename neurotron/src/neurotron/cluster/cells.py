"""
module neurotron.cluster.cells
    class Cluster  # simulate a cluster of Neurotrons
    class Token    # wrapper for token dicts
"""

from neurotron.math.attribute import Attribute
from neurotron.math.matrix import Matrix
from neurotron.math.field import Field
from neurotron.cluster.terminal import Terminal
from neurotron.cluster.setup import Collab,Excite,Predict
from neurotron.cluster.monitor import Monitor, Record

from neurotron.cluster.toy import Toy
from neurotron.cluster.token import Token

import neurotron.math.matfun as mf
import neurotron.math as nm
isa = isinstance

#=========================================================================
# class SynapseErr
#=========================================================================

class SynapseErr(Exception):
    """
    class Synapse: exception to raise if there are no more free synapses
    """
    pass

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
# class Core (Cluster Core)
#=========================================================================

class Core(Attribute):
    def __init__(self,m=2,n=7,d=4,s=3,f=None,verbose=0,rand=False):
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
        self.init()

    def init(self):
        m,n = self.shape[:2]
        self.U = Matrix(m,n)
        self.Q = Matrix(m,n)
        self.D = Matrix(m,n)
        self.B = Matrix(m,n)
        self.X = Matrix(m,n)
        self.Y = Matrix(m,n)
        self.S = Matrix(m,n)
        self.L = Matrix(m,n)

    def zero(self):
        return Matrix(*self.shape[:2])

    def split(self,y):    # split y int context c and feedforward f
        """
        >>> cells = Cluster(3,4,2,5,7)
        >>> y = nm.row([1,1,1,0,0,0,1,1,1,0,0,0],[1,0,1,0,1,0,1])
        >>> cells.split(y)
        ([1 1 1 0 0 0 1 1 1 0 0 0], [1 0 1 0 1 0 1])
        """
        return (y[self.cdx],y[self.fdx])

    def update(self,y):        # update y
        if y is not None:
            y[self.k] = self.Y
        return y

    def relax(self,y=None):
        for x in 'U Q D B Y S'.split(): self.set(x,self.zero())
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
        self.B = nm.AND(nm.NOT(self.D),self.Q)
        self.Y = nm.OR(self.Y,self.B)
        return self.update(y)

    def predict(self,y):
        c,f = self.split(y)
        self.S = self._predict(c)
        self.X = self.S
        return y

    def iterate(self,y):
        y = self.relax(y);
        y = self.stimu(y);
        y = self.react(y);
        y = self.depress(y);
        y = self.excite(y);
        y = self.burst(y);
        y = self.predict(y);
        return y

#=========================================================================
# class Cluster
#=========================================================================

class Cluster(Core):
    verbose = 0
    def __init__(self,m=4,n=10,d=2,s=5,f=None,verbose=0,rand=False):
        super().__init__(m,n,d,s,f,verbose=verbose,rand=rand)

    def __len__(self):
        m,n,d,s = self.shape
        return m*n

    def __getitem__(self,idx):
        if isa(idx,int): idx = self.kappa(idx)
        cell = Cell(self,*idx,self._predict.delta)
        return cell

    def range(self):
        return range(self.sizes[1])

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

    def clear(self,M):
        m,n,d,s = self.shape
        M = Matrix(m,n)

    def plot(self,mon,subplot=0,title=None,label=None):
        m,n,d,s = self.shape
        for i in range(m):
            for j in range(n):
                cell = Cell(self,i,j)
                if label is not None:
                    k = self.kappa(i,j)
                    if n <= 10:
                        size = 7
                    elif n <= 20:
                        size = 5
                    else:
                        size = 0
                    mon(cell,i+subplot*(m+1),j,k,size=size)
                else:
                    mon(cell,i+subplot*(m+1),j)
        if title is not None:
            mon.title(title)

    def draw(self,mon,subplot=0):
        self.plot(mon,subplot=subplot,label=True)

    def step(self,mon,y,tag='',log=None):
        y = self.iterate(y)
        #m,n,d,s = self.shape
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
        return y

    def connect(self,idx,kdx):
        """
        >>> cells = Cluster(2,5,2,3,rand=False)
        >>> cells.connect([0,6,8],[4,6,8])
        >>> cells._predict.map()
        K: +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+
           |  000  |  000  |  068  |  068  |  068  |
           |  000  |  000  |  000  |  000  |  000  |
           +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+
           |  000  |  000  |  000  |  000  |  000  |
           |  000  |  000  |  000  |  000  |  000  |
           +-------+-------+-------+-------+-------+
        P: +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+
           |  000  |  000  |  AAA  |  AAA  |  AAA  |
           |  000  |  000  |  000  |  000  |  000  |
           +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+
           |  000  |  000  |  000  |  000  |  000  |
           |  000  |  000  |  000  |  000  |  000  |
           +-------+-------+-------+-------+-------+
        W: +-000/0-+-002/2-+-004/4-+-006/6-+-008/8-+
           |  000  |  000  |  111  |  111  |  111  |
           |  000  |  000  |  000  |  000  |  000  |
           +-001/1-+-003/3-+-005/5-+-007/7-+-009/9-+
           |  000  |  000  |  000  |  000  |  000  |
           |  000  |  000  |  000  |  000  |  000  |
           +-------+-------+-------+-------+-------+
        """
        assert isa(idx,list)
        assert isa(kdx,list)
        m,n,d,s = self.shape
        if len(idx) > s:
            raise Exception('more than %g indices provided (arg2)'%s)
        predict = self._predict

        for k in kdx:
            done = False
            for ii in range(d):
                if mf.ALL(predict.P[k][ii,:]==0):
                    for jj in range(s):
                        predict.K[k][ii,jj] = 0
                    for jj in range(len(idx)):
                        predict.K[k][ii,jj] = idx[jj]
                        predict.P[k][ii,jj] = 0.5
                    done = True
                    break
                elif mf.ALL(predict.K[k][ii,:]==Matrix(idx)):
                    done = True
                    break
            if not done:
                print('K[%g]' % k, predict.K[k])
                raise SynapseErr('no free synapses to connect: [%g]'%k)
            predict.W[k] = predict.P[k] >= predict.eta

    def decode(self):
        output = self.token.decode(self.Y)
        predict = self.token.decode(self.X)
        return (output,predict)

#===============================================================================
# class Cells
#===============================================================================

class Cells(Cluster):
    """
    >>> Cells()
    |-|-|-|-|-|-|-|-|-|-|
    >>> Cells('Mary')
    |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
    >>> token = Token({'foo':[0,1,1,0,0],'fee':[1,0,0,0,1]})
    >>> Cells((5,2,4,3),token,verbose=True)
    |-|-|-|-|-|-|-|-|-|-|
    >>> cells = Cells((3,20,10,3),4)  # 4/20 tokenizer
    >>> cells.token.shape, cells.token.range
    ((1, 20), (4, 4))
    """
    def __init__(self,shape=(2,5,2,3),token=2,verbose=0):
        if isa(shape,str):
            tag = shape      # rename
            self.toy = Toy(tag)
            shape = self.toy.shape
            token = self.toy.token
        else:
            self.toy = None

        nm.seed(1)
        cells = super().__init__(*shape,verbose=verbose)
        self.token = self._token_setup(token)
        m,n,d,s = shape

        f = [0,0,0] if self.token is None else self.token('.')
        self.y = nm.row(nm.zeros(1,m*n),f)
        self.record = Record(self)

    def _token_setup(self,token):
        if isa(token,int):
            n = self.shape[1]
            m = token            # rename
            token = Token().create(m,n)
        return token

    def process(self,seq):
        m,n,d,s = self.shape
        seq = seq.split() if isa(seq,str) else seq
        prediction = [seq[0],'->']
        for word in seq:
            mon = Monitor(m,n);
            self.y = nm.row(nm.zeros(1,m*n),self.token[word])
            self.y = self.step(mon,self.y,word)
            output,predict = self.decode()
            mon.xlabel((n-1)/2,output+' -> '+predict)
            prediction.append(predict)
        return prediction

    def run(self,seq):
        m,n,d,s = self.shape
        seq = seq.split() if isa(seq,str) else seq
        prediction = [seq[0],'->']
        for word in seq:
            self.y = nm.row(nm.zeros(1,m*n),self.token[word])
            self.y = self.iterate(self.y)
            output,predict = self.decode()
            prediction.append(predict)
        return prediction

    def predictive(self,list):
        for k in list:
            cells.X[k] = 1;
            cells._predict.I[k] = Matrix([[.1,-.1,.1,-.1,.1],[0,0,0,0,0]])

    def map(self):
        self._predict.map()

    def __str__(self):
        self.record.clear();
        self.record(self)
        return self.record.pattern()

    def __repr__(self):
        return self.__str__()

    def plot(self,mon=None,subplot=0,label=True,title=None):
        m,n,d,s = self.shape
        if isa(mon,str):
            if title is not None: raise Exception('two values for title')
            title = mon; mon = None;
        if mon is None: mon = Monitor(m,n)
        super().plot(mon,subplot=subplot,label=label)
        if title is not None: mon.title(title)


#===============================================================================
# utilities
#===============================================================================


def follow(M):
    """
    >>> follow([[0,0,0],[0,0,0]])
    [1 1 1; 0 0 0]
    >>> follow([[1,1,1],[0,0,0]])
    [0 1 1; 1 0 0]
    >>> follow([[0,0,0],[1,1,1]])
    """
    def next(N,m,n,j):
        #print('##### next(N,%g,%g,%g)' % (m,n,j),'N:',N)
        if j >= n: return None
        for i in range(m):
            if N[i,j]:
                N[i,j] = 0;  N[(i+1)%m,j] = 1
                if i+1 < m:
                    return N
                else:
                    return next(N,m,n,j+1)

    if isa(M,list): M = Matrix(M)
    m,n = M.shape;
    N = M.copy()
    if N.any() == 0:
        for j in range(n): N[0,j] = 1
        return N
    return next(N,m,n,0)

#===============================================================================
# unit tests
#===============================================================================

def _test_mary():
    """
    >>> token = {'Mary': [1,0,0,0,0,0,0,1,1]}
    >>> shape = (2,9,2,5); m,n,d,s = shape
    >>> nm.seed(1);  cells = Cluster(*shape,verbose=1,rand=True)
    >>> cells.X[0] = 1; cells._predict.I[0] = Matrix([[.1,0,.1,0,.1],[0,0,0,0,0]])
    >>> y = nm.row(nm.zeros(1,m*n),token['Mary'])
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

def test_follow1():
    """
    >>> follow([[0,0,0],[0,0,0]])
    [1 1 1; 0 0 0]
    >>> follow([[1,1,1],[0,0,0]])
    [0 1 1; 1 0 0]
    >>> follow([[0,1,1],[1,0,0]])
    [1 0 1; 0 1 0]
    >>> follow([[1,0,1],[0,1,0]])
    [0 0 1; 1 1 0]
    >>> follow([[0,0,1],[1,1,0]])
    [1 1 0; 0 0 1]
    >>> follow([[1,1,0],[0,0,1]])
    [0 1 0; 1 0 1]
    >>> follow([[0,1,0],[1,0,1]])
    [1 0 0; 0 1 1]
    >>> follow([[1,0,0],[0,1,1]])
    [0 0 0; 1 1 1]
    >>> follow([[0,0,0],[1,1,1]])
    """

def test_follow2():
    """
    >>> follow([[0,0,0],[0,0,0],[0,0,0]])
    [1 1 1; 0 0 0; 0 0 0]
    >>> follow([[1,1,1],[0,0,0],[0,0,0]])
    [0 1 1; 1 0 0; 0 0 0]

    >>> follow([[0,1,1],[1,0,0],[0,0,0]])
    [0 1 1; 0 0 0; 1 0 0]
    >>> follow([[0,1,1],[0,0,0],[1,0,0]])
    [1 0 1; 0 1 0; 0 0 0]
    >>> follow([[1,0,1],[0,1,0],[0,0,0]])
    [0 0 1; 1 1 0; 0 0 0]
    >>> follow([[0,0,1],[1,1,0],[0,0,0]])
    [0 0 1; 0 1 0; 1 0 0]
    >>> follow([[0,0,1],[0,1,0],[1,0,0]])
    [1 0 1; 0 0 0; 0 1 0]
    >>> follow([[1,0,1],[0,0,0],[0,1,0]])
    [0 0 1; 1 0 0; 0 1 0]
    >>> follow([[0,0,1],[1,0,0],[0,1,0]])
    [0 0 1; 0 0 0; 1 1 0]
    >>> follow([[0,0,1],[0,0,0],[1,1,0]])
    [1 1 0; 0 0 1; 0 0 0]
    >>> follow([[1,0,0],[0,0,0],[0,1,1]])
    [0 0 0; 1 0 0; 0 1 1]
    >>> follow([[0,0,0],[1,0,0],[0,1,1]])
    [0 0 0; 0 0 0; 1 1 1]
    >>> follow([[0,0,0],[0,0,0],[1,1,1]])
    """

def test_connect():
    """
    >>> cells = Cluster(1,5,2,3)
    >>> cells._predict.K.map()
    +-000/0-+-001/1-+-002/2-+-003/3-+-004/4-+
    |  000  |  000  |  000  |  000  |  000  |
    |  000  |  000  |  000  |  000  |  000  |
    +-------+-------+-------+-------+-------+
    >>> cells.connect([1,2,3],[2,3,4])
    >>> cells._predict.K.map()
    +-000/0-+-001/1-+-002/2-+-003/3-+-004/4-+
    |  000  |  000  |  123  |  123  |  123  |
    |  000  |  000  |  000  |  000  |  000  |
    +-------+-------+-------+-------+-------+
    >>> cells.connect([1,2,3],[2,3,4]) # same again
    >>> cells._predict.K.map()
    +-000/0-+-001/1-+-002/2-+-003/3-+-004/4-+
    |  000  |  000  |  123  |  123  |  123  |
    |  000  |  000  |  000  |  000  |  000  |
    +-------+-------+-------+-------+-------+
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
