"""
module carabao.cluster.setup
    class Collab  # setup collaboration terminal
"""

import neurotron.matrix as mx
from neurotron.matrix import Attribute, Matrix, Field, ones, zeros
isa = isinstance

#===============================================================================
# class Collab
#===============================================================================

class Collab(Attribute):  # to manage collaboration topology
    """
    >>> shape = (3,4,2,5)
    >>> Collab(*shape)
    Collab(3,4)
    >>> Collab(*shape).map()
    K: +-000/0-+-003/3-+-006/6-+-009/9-+
       |  12   |  45   |  78   |  AB   |
       +-001/1-+-004/4-+-007/7-+-010/A-+
       |  02   |  35   |  68   |  9B   |
       +-002/2-+-005/5-+-008/8-+-011/B-+
       |  01   |  34   |  67   |  9A   |
       +-------+-------+-------+-------+
    P: +-000/0-+-003/3-+-006/6-+-009/9-+
       |  11   |  11   |  11   |  11   |
       +-001/1-+-004/4-+-007/7-+-010/A-+
       |  11   |  11   |  11   |  11   |
       +-002/2-+-005/5-+-008/8-+-011/B-+
       |  11   |  11   |  11   |  11   |
       +-------+-------+-------+-------+
    W: +-000/0-+-003/3-+-006/6-+-009/9-+
       |  11   |  11   |  11   |  11   |
       +-001/1-+-004/4-+-007/7-+-010/A-+
       |  11   |  11   |  11   |  11   |
       +-002/2-+-005/5-+-008/8-+-011/B-+
       |  11   |  11   |  11   |  11   |
       +-------+-------+-------+-------+
    """
    def __init__(self,m,n,dummy1=0,dummy2=0):
        self.shape = (m,n)
        self.init()
        self.theta = 0
        self.eta = 0.5

    def __str__(self):
        return 'Collab(%g,%g)' % self.shape

    def __repr__(self):
        return self.__str__()

    def _Kij(self,i,j):
        m,n = self.shape
        Kij = Matrix(1,m-1)
        s = 0
        for l in range(m):
            if l != i:
                Kij[s] = l + m*j;  s += 1
        return Kij

    def init(self):
        m,n = self.shape
        self.K = Field(m,n,1,m-1)
        self.P = Field(m,n,1,m-1)
        self.W = Field(m,n,1,m-1)
        for i in range(m):
            for j in range(n):
                self.K[i,j] = self._Kij(i,j)
                self.P[i,j] = ones(1,m-1)
                self.W[i,j] = ones(1,m-1)
        self.P.map = self.P.vmap

    def map(self):
        self.K.map('K: ')
        self.P.map('P: ')
        self.W.map('W: ')

#===============================================================================
# class Excite
#===============================================================================

class Excite(Attribute):
    """
    >>> shape = (1,3,2,5)
    >>> Excite(*shape)
    Excite(1,3,2,5)
    """
    def __init__(self,m,n,d,s,token=None):
        self.shape = (m,n,d,s)
        self.theta = 1
        self.eta = 0.5
        if isa(token,dict): self.setup(token)

    def setup(self,token):
        """
        >>> token = {'Mary':[1,0,0,0,1], 'John':[0,1,0,0,1], 'likes':[0,0,1,0,1]}
        >>> excite = Excite(1,5,1,5,token); print(excite)
        Excite(1,5,3,5)
        >>> excite.map()
        K: +-000/0-+-001/1-+-002/2-+-003/3-+-004/4-+
           | 01234 | 01234 | 01234 | 00000 | 01234 |
           | 00000 | 00000 | 00000 | 00000 | 01234 |
           | 00000 | 00000 | 00000 | 00000 | 01234 |
           +-------+-------+-------+-------+-------+
        W: +-000/0-+-001/1-+-002/2-+-003/3-+-004/4-+
           | 10001 | 01001 | 00101 | 00000 | 10001 |
           | 00000 | 00000 | 00000 | 00000 | 01001 |
           | 00000 | 00000 | 00000 | 00000 | 00101 |
           +-------+-------+-------+-------+-------+
        >>> (excite.P,excite.theta)
        (None, 2)
        """
        assert isa(token,dict)
        self.theta = max([sum(token[key]) for key in token])

        values = [token[key] for key in token]
        T = Matrix(values)

        m,n,d,s = self.shape
        s = max([len(token[key]) for key in token])
        d = mx.max(mx.sum(T))
        if s != self.shape[3]:
            raise Exception('mismatch of synapses size with token length')
        self.shape = (m,n,d,s)

        self.K = Field(m,n,d,s)
        self.P = None
        self.W = Field(m,n,d,s)

        for j in range(n):
            Kij = zeros(d,s)
            Wij = zeros(d,s)
            mu = 0
            for l in range(T.shape[0]):
                if T[l,j]:
                    Wij[mu,:] = T[l,:]
                    Kij[mu,:] = Matrix(range(s))
                    mu += 1
            for i in range(m):
                self.K[i,j] = Kij
                self.W[i,j] = Wij

    def __str__(self):
        return 'Excite(%g,%g,%g,%g)' % self.shape

    def __repr__(self):
        return self.__str__()

    def map(self):
        self.K.map('K: ')
        self.W.map('W: ')

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
