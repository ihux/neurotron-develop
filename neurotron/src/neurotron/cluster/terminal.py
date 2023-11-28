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
    def __init__(self,K,P=None,eta=0.5,theta=None):
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
        self.K.map('K: ')
        if self.P is None:
            print('P: None')
        else:
            self.P.map('P: ')
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

    def spike(self,v):              # calculate spike vectors
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
        if not isa(v,Matrix): v = Matrix(v)
        S = self.spike(v)
        M = Matrix(*S.shape[:2])
        for k in M.range():
            M[k] = max(S[k])
        return M

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
