"""
module neurotron.cluster.cluster
    class Cluster  # simulate a cluster of Neurotrons
"""

from neurotron.math.attribute import Attribute
from neurotron.math.matrix import Matrix
from neurotron.math.matfun import ROW
from neurotron.cluster.terminal import Terminal
from neurotron.cluster.setup import Collab,Excite,Predict

#=========================================================================
# class Cluster
#=========================================================================

class Cluster(Attribute):
    verbose = 0
    def __init__(self,m=4,n=10,d=2,s=5,f=None,verbose=0):
        if f is None: f = n
        self.shape = (m,n,d,s)
        self.sizes = (f,n*m)               # (M,N)
        self.cdx = Matrix(range(m*n))      # access context vector
        self.fdx = m*n+Matrix(range(f))    # access feedforward vector
        self.k = Matrix(range(n*m))
        self.verbose = verbose

        self._excite = Terminal(m,n)       # simple excite terminal
        self._collab = Terminal(Collab(m,n,d,s))
        self._predict = Terminal(Predict(m,n,d,s,rand=True),verbose=verbose)

        self.U = Matrix(m,n)
        self.Q = Matrix(m,n)
        self.D = Matrix(m,n)
        self.B = Matrix(m,n)
        self.X = Matrix(m,n)
        self.Y = Matrix(m,n)
        self.S = Matrix(m,n)
        self.L = Matrix(m,n)

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
        self.L = self.zero()
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
        for k in self.range():
            if self.S[k]: print('#### I[%g]:'%k,self._predict.I[k])
        return y

    def relax(self,y):
        M,N = self.sizes
        m,n,d,s = self.shape
        c = y[:N];  f = y[N:N+M]; Z = self.zero()
        self.set('U,Q,D,B,Y,S',(Z,Z,Z,Z,Z,Z))
        return self.update(y)

    def clear(self,M):
        m,n,d,s = self.shape
        M = Matrix(m,n)

    def idle(self):
        clear(self.B);  clear(self.D);  clear(self.L);  clear(self.Q)
        clear(self.S);  clear(self.U);  clear(self.X);  clear(self.Y)
        for k in range(self.sizes[1]):
            y[k] = self.Y[k]
        return y

    def plot(self,mon,subplot=0,title=None):
        m,n,d,s = self.shape
        for i in range(m):
            for j in range(n):
                cell = Cell(self,i,j)
                mon(cell,i+subplot*(m+1),j)
        if title is not None:
            mon.title(title)

    def apply(self,y,tag='',log=None,all=None):
        m,n,d,s = self.shape
        y = self.stimu(y);
        prefix = tag + ' - ' if tag != '' else ''
        if log is not None:
            print('stimu ...');  self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            cells.plot(mon,0);  mon.title(prefix+'stimu')

        y = self.react(y);
        if log is not None:
            print('ract ...');  self.smap()
        if all is not None:
            cells.plot(mon,1);  mon.xlabel(n/2-0.5,prefix+'react')
        else:
            mon = Monitor(2*m+1,n);
            cells.plot(mon,0);  mon.title(prefix+'react')

        y = cells.depress(y);
        if log is not None:
            print('depress ...');  self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            cells.plot(mon,0);  mon.title(prefix+'depress')

        y = cells.excite(y);
        if log is not None:
            print('excite ...');   self.smap()
        if all is not None:
            cells.plot(mon,1);  mon.xlabel(n/2-0.5,prefix+'excite')

        y = cells.burst(y);
        if log is not None:
            print('burst ...');    self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            cells.plot(mon,0);  mon.title(prefix+'burst')

        y = cells.predict(y);
        if log is not None:
            print('predict ...');  self.smap()
        if all is not None:
            cells.plot(mon,1);  mon.xlabel(n/2-0.5,prefix+'predict')
        else:
            cells.plot(mon,1);  mon.xlabel(n/2-0.5,prefix+'predict')

        y = cells.relax(y);
        if log is not None:
            print('relax ...');    self.smap()
        if all is not None:
            mon = Monitor(2*m+1,n);
            cells.plot(mon,0);  mon.title(prefix+'relax')
        return y

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
