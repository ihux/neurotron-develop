"""
neurotron.math: matrix algebra for neural computing
   classes:
       Attribute base class to support compact attribute access
       Matrix    matrix class
       Field     field class (matrix of matrices)

   functions:
       isa       is object a given class instance (same as isinstance)
       eye       unit matrix
       isnumber  is arg a number?
       zeros     zero matrix
       ones      one matrix
       rand      random matrix
       seed      set random seed
       max       row of column maxima
       min       row of column minima
       size      matrix sizes
       magic     magic matrix
       sum       row of column sum
       any       row of column any's
       all       row of column all's
       length    maximum size
       isempty   check if matrix is empty
       row       concatenate to row
       column    concatenate to column
"""

import neurotron.math.attribute
#import neurotron.math.helper
#import neurotron.math.matrix
#import neurotron.math.matfun
#import neurotron.math.field

#===============================================================================
# classes
#===============================================================================

Attribute = attribute.Attribute
"""
Matrix = neurotron.math.matrix.Matrix
Field  = neurotron.math.field.Field

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
eye = neurotron.math.matfun.EYE
isnumber = neurotron.math.helper.isnumber
zeros = neurotron.math.matfun.ZEROS
ones = neurotron.math.matfun.ONES
rand = neurotron.math.matfun.RAND
seed = neurotron.math.matfun.SEED
max = neurotron.math.matfun.MAX
min = neurotron.math.matfun.MIN
size = neurotron.math.matfun.SIZE
magic = neurotron.math.matfun.MAGIC
sum = neurotron.math.matfun.SUM
row = neurotron.math.matfun.ROW
column = neurotron.math.matfun.COLUMN
all = neurotron.math.matfun.ALL
any = neurotron.math.matfun.ANY

AND = neurotron.math.matfun.AND
OR  = neurotron.math.matfun.OR
NOT = neurotron.math.matfun.NOT
"""
