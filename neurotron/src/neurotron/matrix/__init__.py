"""
matrix: matrix building blocks
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
"""
neurotron: building blocks for neural computing circuits
   classes:
       Ansi      provide ANSI color sequences
       Attribute base class to support compact attribute access
       Matrix    matrix class
       Field     field class (matrix of matrices)
       Collab    parameters for collaboration terminal
       Excite    parameters for excitation terminal
       Predict   parameters for prediction terminal
       Terminal  neurotron terminal

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

import neurotron.matrix
import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.ansi

#===============================================================================
# class attribute setup
#===============================================================================

#Attribute = neurotron.matrix.attribute.Attribute
Matrix = matrix.Matrix
Field  = field.Field

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
eye = matfun.eye
isnumber = matfun.isnumber
zeros = matfun.zeros
ones = matfun.ones
rand = matfun.rand
seed = matfun.seed
max = matfun.max
min = matfun.min
size = matfun.size
magic = matfun.magic
sum = matfun.sum
row = matfun.row
column = matfun.column
