"""
neurotron.cluster.terminal.py:
    class Terminal
"""

from neurotron.math import Attribute, Matrix, Field
from neurotron.math.matfun import SUM,SEED,ROW,ZEROS,ONES,MAX,MIN
#from neurotron.cluster import Collab
from neurotron.cluster.setup import Collab, Excite, Predict
from neurotron.math.helper import isa

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
    def __init__(self,K,P=None,eta=0.5,theta=None,delta=(0.1,0.1),verbose=0):
        if isa(K,int) and isa(P,int):
            m = K;  n = P
            self.shape = (m,n)
            self.K = self.P = self.W = self.eta = self.theta = None
            return
        if isa(K,Collab) or isa(K,Excite) or isa(K,Predict):
            K,P,W,theta = K.get('K,P,W,theta')
        else:
            W = K.copy()
        self.K = K;  assert isa(K,Field)
        self.P = P;  assert P is None or isa(P,Field)
        self.W = W;  assert isa(W,Field)
        self.eta = eta
        self.theta = theta if theta is not None else 3
        self.delta = delta
        self.verbose = verbose

        if self.P is not None:
            self.I = Field(*self.K.shape)  #  learning increment

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

    def mind(self,sk,V):
        m,n,d,s = self.P.shape
        pdelta,ndelta = self.delta
        S = sk.T @ ONES(1,s)
        return S * (2*pdelta*V - ndelta)

    def learn(self,L):
        for k in self.P.range():
            if L[k]:
                self.P[k] = MAX(0,MIN(1,self.P[k]+self.I[k]))
                if self.verbose > 0:
                    print('learn P[%g]:' % k,self.P[k],'by',self.I[k])

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
            S[k] = SUM(E.T) >= self.theta
            self.I[k] = self.mind(S[k],V)
            #if any(S[k]):
            #    print('##### spike L:   ',S[k].T@ONES(1,s))
            #    print('##### spike V:   ',V)
            #    print('##### spike I[k]:',self.I[k])
        return S

    def clear(self):
        """
        >>> predict = Terminal(Predict(1,3,2,5,rand=True))
        >>> predict.map()
        K: +-000/0-+-001/1-+-002/2-+
           | 00212 | 12020 | 11100 |
           | 00001 | 02211 | 12110 |
           +-------+-------+-------+
        P: +-000/0-+-001/1-+-002/2-+
           | rkkHH | rPeeE | UheWE |
           | 1UAMA | WwAEU | AwRCm |
           +-------+-------+-------+
        W: +-000/0-+-001/1-+-002/2-+
           | 00011 | 01001 | 10011 |
           | 11111 | 10111 | 10110 |
           +-------+-------+-------+
        >>> predict.clear();  predict.map()
        K: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        P: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        W: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        """
        m,n,d,s = self.K.shape
        zero = ZEROS(d,s)
        for k in self.K.range():
            self.K[k] = self.W[k] = zero
            if self.P is not None:
                self.P[k] = zero

    def __call__(self,v):
        if self.K is None: return self._simple(v)
        S = self.spike(v)
        J = Matrix(*S.shape[:2])
        for k in J.range():
            J[k] = max(S[k])
        return J

#===============================================================================
# unit tests
#===============================================================================

class __TestTerminal__:
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

    def test_predict():
        """
        >>> SEED(0); predict = Terminal(Predict(3,7,2,5,rand=True))
        >>> predict.map()
        K: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | CF033 | 79JI4 | 6C167 | EH5D8 | 9KJGJ | 5FF0I | 3HJJJ |
           | E7019 | 0AK3B | I2004 | 568KH | F49A1 | 17936 | BEI0E |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | 3CAKB | 464FK | 3C4K8 | EFK3F | DGH59 | 3050H | I42G3 |
           | 2ADG7 | 90AIB | 2233I | E3KHI | E914A | B8B2J | G006J |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | EAJ8D | 232BD | G88J8 | 2K3CE | 043DB | DDBGE | GJ180 |
           | 46D7F | 9I8FB | 6F1C3 | IF3AC | 635B0 | B8KAB | 5F82J |
           +-------+-------+-------+-------+-------+-------+-------+
        P: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | 1Mppe | AAApM | WHpAC | JeeuH | rrukc | mwErk | RcuUR |
           | pcmRp | epWUu | WUrkk | HHrPe | eEUhe | WE1UA | MAWwA |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | EUAwR | Cmp1c | Mw1ce | JUwEm | wCMWm | p1ecJ | kwcPP |
           | EmeJC | MU1pA | Wr1EW | JuhCR | RpUCA | HJhhe | cJeRP |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | cphUe | rRWJm | mHUuk | u11eA | UAw1m | URpCu | mmRRP |
           | CJcEh | APp1H | WUCru | EpHmu | Uwemp | khprc | umwJ1 |
           +-------+-------+-------+-------+-------+-------+-------+
        W: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | 11000 | 11101 | 11011 | 10001 | 00000 | 00100 | 10011 |
           | 00010 | 00110 | 11000 | 11010 | 01100 | 11111 | 11101 |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | 11101 | 10010 | 10100 | 11010 | 01110 | 01001 | 00011 |
           | 10011 | 11101 | 10111 | 10011 | 10111 | 11000 | 01011 |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | 00010 | 01110 | 01100 | 01101 | 11010 | 11010 | 00111 |
           | 11010 | 11011 | 11100 | 10100 | 10000 | 00000 | 00011 |
           +-------+-------+-------+-------+-------+-------+-------+
        >>> c = ROW([1,0,0,1,1,0,0],ONES(1,20))
        >>> predict(c)
        [0 0 0 0 0 1 1; 1 1 1 1 0 0 0; 0 1 0 0 0 1 0]
        >>> predict.spike(c).map('S: ')
        S: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  00   |  00   |  00   |  00   |  00   |  01   |  10   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  10   |  01   |  01   |  11   |  00   |  00   |  00   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  00   |  01   |  00   |  00   |  00   |  10   |  00   |
           +-------+-------+-------+-------+-------+-------+-------+
        """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
