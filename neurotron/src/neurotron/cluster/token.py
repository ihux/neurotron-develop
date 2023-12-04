"""
module neurotron.cluster.token
    class Token  # deal with tokens
"""

from neurotron.math.matrix import Matrix
from neurotron.math.matfun import SEED as seed, RAND as rand
import neurotron.math.matfun as mf
isa = isinstance

#=========================================================================
# class Token
#=========================================================================

class Token(dict):
    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self._init()

    def pattern(self,list):
        """
        >>> Token().pattern([1,0,1,0])
        '1010'
        """
        str = ''
        for item in list: str += '1' if item else '0'
        return str

    def _init(self):
        self._decoder = {}  # inverse map's dictionary
        low = 999999999; high = -1
        for key in self:
            bits = self[key]
            pat = self.pattern(bits)
            self._decoder[pat] = key
            n = sum(bits)
            low = min(low,n);  high = max(high,n)
        self.range = (low,high)

    def decode(self,arg=None):
        """
        >>> token = Token({'word1':[0,1,0],'word2':[1,0,1]})
        >>> print(token)
        {'word1': [0, 1, 0], 'word2': [1, 0, 1]}
        >>> token.decode([0,1,0])
        'word1'
        >>> token.decode(Matrix([[1,0,0],[0,0,1]]))
        'word2'
        >>> token.decode([0,0,0])
        ''
        >>> token.decode('junk')
        ''
        """
        decoder = self._decoder
        if arg is None:
            return decoder
        elif isa(arg,list):
            key = self.pattern(arg)
            return decoder[key] if key in decoder else ''
        elif isa(arg,Matrix):
            row = mf.MAX(arg).list()[0]
            key = self.pattern(row)
            return decoder[key] if key in decoder else ''
        else:
            return ''

    def upgrade(self,word):
        """
        >>> token = Token({'word1':[0,1,0,1],'word2':[1,0,1,0]})
        >>> seed(0); token.upgrade('word3')
        [1, 0, 0, 1]
        """
        if len(self) == 0: raise Exception('cannot upgrade empty tokenizer')
        key = next(iter(self))        # 1st key
        n = len(self[key])
        zero = [0 for k in range(n)]  # zero token
        low,high = self.range

        for k in range(100000):       # max 100000 trials
            m = low + rand(1+high-low)
            pattern = zero.copy()
            count = 0
            while count < m:          # while not all m bits set
                idx = rand(n)
                if pattern[idx] == 0:
                    pattern[idx] = 1
                    count += 1

                # is this a new pattern?

            for key in self:
                if self[key] != pattern:   # cool - found pattern
                    self[word] = pattern
                    return pattern

    def __call__(self,word):
        """
        return token pattern (with auto-upgrade)
        >>> token = Token({'word1':[0,1,0,1],'word2':[1,0,1,0]})
        >>> seed(0); token('word3')
        [1, 0, 0, 1]
        """
        if word in self: return self[word]
        return self.upgrade(word)          # upgrade if not found

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
