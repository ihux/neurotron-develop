"""
terminal.py:
    class Terminal
"""

from neurotron.matrix import Attribute, Matrix, Field, sum, isa
from neurotron.cluster.setup import Collab, Excite

#===============================================================================
# class Terminal
#===============================================================================

class Terminal(Attribute):
    """
    class Terminal:
    >>> collab = Terminal(Collab(3,7,2,5))
    >>> c = Matrix(1,3*7); c[0] = c[1] = c[2] = 1
    >>> collab(c)
    [1 0 0 0 0 0 0; 1 0 0 0 0 0 0; 1 0 0 0 0 0 0]
    >>> excite = Terminal(3,7)
    >>> excite._simple([1,0,0,1,1])
    [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
    """
    def __init__(self,K,P=None,eta=0.5,theta=None):
        if isa(K,int) and isa(P,int):
            m = K;  n = P
            self.shape = (m,n)
            self.K = self.P = self.W = self.eta = self.theta = None
            return
        if isa(K,Collab) or isa(K,Excite):
            K,P,W,theta = K.get('K,P,W,theta')
        else:
            W = K.copy()
        self.K = K;  assert isa(K,Field)
        self.P = P;  assert P is None or isa(P,Field)
        self.W = W;  assert isa(W,Field)
        self.eta = eta
        self.theta = theta if theta is not None else 3

    def map(self):
        if self.K is None:
            print('K: None')
        else:
            self.K.map('K: ')
        if self.P is None:
            print('P: None')
        else:
            self.P.map('P: ')
        if self.W is None:
            print('W: None')
        else:
            self.W.map('W: ')

    def weight(self):
        if self.P is not None:
            m,n,d,s = self.K.shape
            for k in range(m*n):
                self.W[k] = self.P[k] > self.eta
        return self.W

    def empower(self,v):
        m,n,d,s = self.K.shape
        E = Field(m,n,d,s)
        self.weight()               # refresh weight
        for k in range(m*n):
            V = v[self.K[k]]
            E[k] = V * self.W[k]
        return E

    def _simple(self,v):            # simple spiking
        if not isa(v,Matrix): v = Matrix(v)
        S = Matrix(*self.shape)
        m,n = self.shape
        for j in range(min(n,v.shape[1])):
            for i in range(m):
                s = (v[j] > 0);  S[i,j] = s
        return S

    def spike(self,v):              # calculate spike vectors
        if not isa(v,Matrix): v = Matrix(v)
        if self.K is None:
            J = self._simple(v)
            S = Field(*self.shape,1,1)
            for k in S.range(): S[k] = J[k]
            return S
        m,n,d,s = self.K.shape
        S = Field(m,n,1,d)
        self.weight()               # refresh weight
        for k in range(m*n):
            V = v[self.K[k]]
            E = V * self.W[k]
            S[k] = sum(E.T) >= self.theta
            #print('#### k:',k,'sum(E.T)',sum(E.T),'> theta:',S[k])
        return S

    def __call__(self,v):
        if self.K is None: return self._simple(v)
        S = self.spike(v)
        M = Matrix(*S.shape[:2])
        for k in M.range():
            M[k] = max(S[k])
        return M

#===============================================================================
# unit tests
#===============================================================================

class TestTerminal:
    def test_construction():
        """
        >>> collab = Terminal(Collab(3,7,2,5))
        >>> collab.map()
        K: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  12   |  45   |  78   |  AB   |  DE   |  GH   |  JK   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  02   |  35   |  68   |  9B   |  CE   |  FH   |  IK   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  01   |  34   |  67   |  9A   |  CD   |  FG   |  IJ   |
           +-------+-------+-------+-------+-------+-------+-------+
        P: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-------+-------+-------+-------+-------+-------+-------+
        W: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-------+-------+-------+-------+-------+-------+-------+
        >>> c = Matrix(1,3*7); c[0] = c[1] = c[2] = 1
        >>> collab(c)
        [1 0 0 0 0 0 0; 1 0 0 0 0 0 0; 1 0 0 0 0 0 0]
        """

    def test_simple1():
        """
        >>> excite = Terminal(3,7)
        >>> excite.map()
        K: None
        P: None
        W: None
        >>> excite._simple([1,0,0,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite([1,0,0,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite.spike([1,0,0,1,1]).map()
        +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-------+-------+-------+-------+-------+-------+-------+
        """

    def test_simple2():
        """
        >>> excite = Terminal(3,7)
        >>> excite.map()
        K: None
        P: None
        W: None
        >>> excite._simple([1,0,0,1,1,0,0,1,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite([1,0,0,1,1,0,0,1,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite.spike([1,0,0,1,1,0,0,1,1,1]).map()
        +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-------+-------+-------+-------+-------+-------+-------+
        """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
