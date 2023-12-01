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
import neurotron.math.helper
import neurotron.math.matrix
import neurotron.math.matfun
import neurotron.math.field

#===============================================================================
# classes
#===============================================================================

Attribute = attribute.Attribute
Matrix = matrix.Matrix
Field  = field.Field

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
eye = matfun.EYE
isnumber = helper.isnumber
zeros = matfun.ZEROS
ones = matfun.ONES
rand = matfun.RAND
seed = matfun.SEED
max = matfun.MAX
min = matfun.MIN
size = matfun.SIZE
magic = matfun.MAGIC
sum = matfun.SUM
row = matfun.ROW
column = matfun.COLUMN
all = matfun.ALL
any = matfun.ANY

AND = matfun.AND
OR  = matfun.OR
NOT = matfun.NOT
