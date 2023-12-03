"""
neurotron: building blocks for neural computing circuits
   classes:
       Ansi        provide ANSI color sequences
       Attribute   base class to support compact attribute access
       Matrix      matrix class
       Field       field class (matrix of matrices)
       Cluster     cluster of Neurotrons
       Collab      parameters for collaboration terminal
       Excite      parameters for excitation terminal
       Predict     parameters for prediction terminal
       Terminal    neurotron terminal
       Token       wrapper for token dicts
       Cell        access to cluster cell
       Monitor     state monitoring of cells
       Record      recording of cell states
       SynapseErr  Synapse Exception
       Toy         creating toy stuff
       Train       sequence trainer

   functions:
       isa         is object a given class instance (same as isinstance)
       eye         unit matrix
       isnumber    is arg a number?
       zeros       zero matrix
       ones        one matrix
       rand        random matrix
       seed        set random seed
       max         row of column maxima
       min         row of column minima
       size        matrix sizes
       magic       magic matrix
       sum         row of column sum
       any         row of column any's
       all         row of column all's
       length      maximum size
       isempty     check if matrix is empty
       row         concatenate to row
       column      concatenate to column

    logical:
       AND         logical matrix and
       OR          logical matrix or
       NOT         logical matrix not

    utility:
       follow      following matrix during matrix iteration

"""

import neurotron.math.attribute
import neurotron.math.helper
import neurotron.math.matrix
import neurotron.math.matfun
import neurotron.math.field

import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.cluster.cluster
import neurotron.cluster.trainer
import neurotron.ansi

import neurotron.neurotron

#===============================================================================
# class attribute setup
#===============================================================================

Ansi = neurotron.ansi.Ansi
#Record = neurotron.neurotron.Record

Attribute = neurotron.math.attribute.Attribute
Collab = neurotron.cluster.setup.Collab
Excite = neurotron.cluster.setup.Excite
Predict = neurotron.cluster.setup.Predict
Matrix = neurotron.math.matrix.Matrix
Field  = neurotron.math.field.Field
Terminal = neurotron.cluster.terminal.Terminal

Cluster = neurotron.cluster.cluster.Cluster
Token = neurotron.cluster.cluster.Token
Cell = neurotron.cluster.cluster.Cell
SynapseErr = neurotron.cluster.SynapseErr

Monitor = neurotron.cluster.monitor.Monitor
Record = neurotron.cluster.monitor.Record

Toy = neurotron.cluster.toy.Toy

Train = neurotron.cluster.trainer.Train

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

follow = neurotron.cluster.cluster.follow
