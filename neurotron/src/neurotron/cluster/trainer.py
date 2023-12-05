"""
module neurotron.cluster.trainer
    class Cells  # derived class of Cluster
    class Train  # sequence trainer
"""

from neurotron.cluster.cells import Cluster, Cells, follow
from neurotron.cluster.token import Token
from neurotron.math.matrix import Matrix
from neurotron.cluster.toy import Toy
from neurotron.cluster.monitor import Record, Monitor
import neurotron.math as nm
isa = isinstance

#===============================================================================
# class Train
#===============================================================================

class Train:
    """
    parameter training
    >>> Train()
    Train(Cells(2,5,2,3))
    >>> Train(Cells('Mary'))
    Train(Cells('Mary'))
    """
    def __init__(self,cells=None):
        self.memory = {}
        self._words = {}
        self._contexts = {}
        self.cells = Cells() if cells is None else cells

    def pattern(self,list):
        """
        >>> Train().pattern([1,0,1,0])
        '1010'
        """
        str = ''
        for item in list: str += '1' if item else '0'
        return str

    def hash(self,M):    # hash of a matrix
        """
        Train().hash(Matrix([[1,1,0],[0,1,1]]))
        """
        list = M.list();  str = ''
        m,n = M.shape; sep = ''
        for i in range(m):
            row = list[i]
            str += sep + self.pattern(row); sep = '|'
        return str

    def next(self,M):
        """
        >>> Train().next(Matrix(2,3))
        [1 1 1; 0 0 0]
        >>> Train().next([[0,1,1],[1,0,0]])
        [1 0 1; 0 1 0]
        >>> Train().next([[0,0,0],[1,1,1]])
        """
        if M is None:
            m,n,d,s = self.cells.shape
            return follow(Matrix(m,n))
        return follow(M)

    def token(self,word=None):
        """
        >>> dict = Train(Cells('Mary')).token()
        >>> Train(Cells('Mary')).token('likes')
        [0, 0, 1, 0, 0, 0, 0, 1, 1]
        """
        if word is None: return self.cells.token
#       return self.cells.token[word]
        return self.cells.token(word)

    def number(self,M):
        m,n = M.shape; nmb = 0; base = 1;
        for j in range(n):
            for i in range(m):
                if M[i,j]:
                    nmb += base*i; break
            base *= m
        return nmb

    def code(self,M):
        m,n = M.shape; code = Matrix(1,n)
        for j in range(n):
            for i in range(m):
                if M[i,j]:
                    code[0,j] = i; break
        return code

    def index(self,token):
        """
        >>> train = Train(Cells('Mary'))
        >>> train.index(train.token('likes'))
        [2, 7, 8]
        """
        idx = []
        for k in range(len(token)):
            if token[k]: idx.append(k)
        return idx

    def _word(self,word,new):  # store/update word to ._words
        """
        word 'Mary' is stored as ([0,7,8],'#0',[[1,1,1],[0,0,0]])
        >>> Train(Cells('Mary'))._word('Mary',True)
        ('Mary', ([0, 7, 8], '#0', [0 0 0; 0 0 0]))
        """
        m = self.cells.shape[0]
        n = len(self.index(self.token(word)))
        if not word in self._words:
            assert new
            triple = (self.index(self.token(word)),'#0',Matrix(m,n))
            #print('### triple:',triple)
        else:
            assert not new
            triple = self._words[word]
            idx,key,M = triple
            key = '#%g' % (int(key[1:])+1)
            M = self.next(M)
            if M is None:
                raise Exception('representation overflow (max %g)' % m**n)
            triple = (idx,key,M)
        self._words[word] = triple
        return(word,triple)

    def _train(self,curctx,word):
        """
        >>> train = Train(Cells('Mary'))
        >>> ans = train._train('','Mary')
        >>> train._train('<Mary>','likes')
        '<Mary likes>'
        >>> train.show(token=False)
        words:
            Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
            likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        contexts:
            <Mary>:
               #: ([0, 7, 8], '#0', 'Mary')
               @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
               likes: (1, '<Mary likes>', [2, 7, 8])
            <Mary likes>:
               #: ([2, 7, 8], '#1', 'likes')
               @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
        """
        if not word in self._words: self._word(word,True)
        if curctx == '':
            newctx = '<' + word + '>'
        else:
            newctx = '<' + curctx[1:-1] + ' ' + word + '>'

            # example: curctx = '<Mary>', word = 'likes'
            #          newctx = '<Mary likes>'

        if not newctx in self._contexts:
            if not curctx == '': self._word(word,False) # next word representation
            triple = self._words[word]
            idx,key,M = triple     # triple = ([2, 7, 8], '#1', [1 1 1; 0 0 0])
            idx = self.index(self.token(word))
            dict = {'#':(idx,key,word)}
            code = self.code(M)
            tag = '';  sep = ''
            for k in range(code.shape[1]):
                tag += sep + '%g.%g' % (idx[k],code[0,k]); sep = '-'
            dict['@'] = [key,M,tag]
            self._contexts[newctx] = dict

        if curctx in self._contexts:
            idx = self.index(self.token(word))
            dict = self._contexts[curctx]
            if word in dict:
                count,value,index = dict[word]
                assert value == newctx
                assert index == idx
            else:
                count = 0
            dict[word] = (count+1,newctx,idx)
            self._contexts[curctx] = dict
        return newctx

    def _sequence(self,context,sequence):
        """
        process sequence:
        >>> train = Train(Cells('Mary'))
        >>> train._sequence('',['Mary','likes'])
        '<Mary likes>'
        """
        for word in sequence:
            context = self._train(context,word)
        return context

    def __call__(self,context,arg=None):
        """
        >>> train = Train(Cells('Mary'))
        >>> train('','Mary')
        '<Mary>'
        >>> train('Mary')
        '<Mary>'
        >>> train('<Mary>','likes')
        '<Mary likes>'
        >>> train('','Mary likes'.split())
        '<Mary likes>'
        >>> train('Mary likes')
        '<Mary likes>'
        >>> train('Mary likes',5)
        '<Mary likes>'
        """
        if isa(arg,int):
            sequence = context
            for k in range(arg):
                context = self(sequence)
            return context
        if arg is None:
            arg = context.split() if isa(context,str) else context
            context = ''
        if isa(arg,list):
            sequence = arg  # rename
            return self._sequence(context,sequence)
        return self._train(context,arg)

    def __str__(self):
        if self.cells is None: return 'Train()'
        if self.cells.toy is not None:
            return "Train(Cells('%s'))" % self.cells.toy.tag
        return 'Train(Cells(%g,%g,%g,%g))' % self.cells.shape

    def __repr__(self):
        return self.__str__()

    def show(self,token=True):
        if token:
            print('token:')
            for word in self.cells.token:
                idx = self.index(self.token(word))
                print('   ',idx,'%s:' % word,self.token(word))
        print('words:')
        for word in self._words:
            print('   ','%s:' % word,self._words[word])
        print('contexts:')
        for context in self._contexts:
            dict = self._contexts[context]
            print('   ','%s:' % context)
            for key in dict:
                print('       %s:' % key,dict[key])

#===============================================================================
# unit tests
#===============================================================================

def test_train():
    """
    >>> train = Train(Cells('Mary'))
    >>> train.show()
    token:
        [0, 7, 8] Mary: [1, 0, 0, 0, 0, 0, 0, 1, 1]
        [1, 7, 8] John: [0, 1, 0, 0, 0, 0, 0, 1, 1]
        [0, 6, 7] Lisa: [1, 0, 0, 0, 0, 0, 1, 1, 0]
        [1, 6, 7] Andy: [0, 1, 0, 0, 0, 0, 1, 1, 0]
        [2, 7, 8] likes: [0, 0, 1, 0, 0, 0, 0, 1, 1]
        [3, 7, 8] to: [0, 0, 0, 1, 0, 0, 0, 1, 1]
        [4, 7, 8] sing: [0, 0, 0, 0, 1, 0, 0, 1, 1]
        [4, 6, 7] dance: [0, 0, 0, 0, 1, 0, 1, 1, 0]
        [5, 7, 8] hike: [0, 0, 0, 0, 0, 1, 0, 1, 1]
        [5, 6, 7] paint: [0, 0, 0, 0, 0, 1, 1, 1, 0]
        [4, 6, 7] climb: [0, 0, 0, 0, 1, 0, 1, 1, 0]
        [6, 7, 8] .: [0, 0, 0, 0, 0, 0, 1, 1, 1]
    words:
    contexts:
    """

def test_train_mary():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('','Mary')
    '<Mary>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
    """

def test_train_mary_likes_1():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
    """

def test_train_mary_likes_2():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (3, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
    """

def test_train_mary_likes_to():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> ans = train('<Mary>','likes')
    >>> train('<Mary likes>','to')
    '<Mary likes to>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
    """

def test_train_mary_likes_to_sing():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('Mary likes to sing .')
    '<Mary likes to sing .>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
    """

def test_train_mary_john():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans = train('Mary likes to sing .')
    >>> train('John')
    '<John>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
        John: ([1, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
        <John>:
           #: ([1, 7, 8], '#0', 'John')
           @: ['#0', [0 0 0; 0 0 0], '1.0-7.0-8.0']
    """

def test_train_mary_john_likes():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans = train('Mary likes to sing .')
    >>> train('John likes')
    '<John likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#2', [0 1 1; 1 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
        John: ([1, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
        <John>:
           #: ([1, 7, 8], '#0', 'John')
           @: ['#0', [0 0 0; 0 0 0], '1.0-7.0-8.0']
           likes: (1, '<John likes>', [2, 7, 8])
        <John likes>:
           #: ([2, 7, 8], '#2', 'likes')
           @: ['#2', [0 1 1; 1 0 0], '2.1-7.0-8.0']
    """

def test_sequence():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('Mary likes')
    '<Mary likes>'
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
