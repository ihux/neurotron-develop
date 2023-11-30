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

import neurotron.math.attribute
import neurotron.math.matrix
import neurotron.math.field
import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.ansi

#===============================================================================
# class attribute setup
#===============================================================================

Ansi = neurotron.ansi.Ansi
#Attribute = neurotron.math.attribute.Attribute
Collab = neurotron.cluster.setup.Collab
Excite = neurotron.cluster.setup.Excite
Predict = neurotron.cluster.setup.Predict
Matrix = neurotron.math.matrix.Matrix
Field  = neurotron.math.field.Field
Terminal = neurotron.cluster.terminal.Terminal

#===============================================================================
# function attribute setup
#===============================================================================

isa = isinstance
eye = neurotron.math.eye
isnumber = neurotron.math.isnumber
zeros = neurotron.math.zeros
ones = neurotron.math.ones
rand = neurotron.math.rand
seed = neurotron.math.seed
max = neurotron.math.max
min = neurotron.math.min
size = neurotron.math.size
magic = neurotron.math.magic
sum = neurotron.math.sum
row = neurotron.math.row
column = neurotron.math.column
