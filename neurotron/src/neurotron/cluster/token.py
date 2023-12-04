"""
module neurotron.cluster.token
    class Token  # deal with tokens
"""

from neurotron.math.matrix import Matrix
import neurotron.math.matfun as mf

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
        for key in self:
            pat = self.pattern(self[key])
            self._decoder[pat] = key

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

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
