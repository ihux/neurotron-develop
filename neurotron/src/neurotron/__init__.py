"""
neurotron: building blocks for neural computing circuits
   classes:
       Ansi      provide ANSI color sequences
       Attribute base class to support compact attribute access
       Matrix    matrix class
       Field     field class (matrix of matrices)
       Collab    parameters for collaboration terminal
       Excite    parameters for excitation terminal
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

Ansi = neurotron.ansi.Ansi
Attribute = neurotron.matrix.Attribute
Collab = neurotron.cluster.setup.Collab
Excite = neurotron.cluster.setup.Excite
Matrix = neurotron.matrix.Matrix
Field  = neurotron.matrix.Field
Terminal = neurotron.cluster.terminal.Terminal

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
eye = neurotron.matrix.eye
isnumber = neurotron.matrix.isnumber
zeros = neurotron.matrix.zeros
ones = neurotron.matrix.ones
rand = neurotron.matrix.rand
seed = neurotron.matrix.seed
max = neurotron.matrix.max
min = neurotron.matrix.min
size = neurotron.matrix.size
magic = neurotron.matrix.magic
sum = neurotron.matrix.sum
row = neurotron.matrix.row
column = neurotron.matrix.column
