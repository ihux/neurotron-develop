"""
neurotron.cluster: neural cluster computing
    classes:
        Cluster     cluster of Neurotrons
        Collab      parameters for collaboration terminal
        Excite      parameters for excitation terminal
        Predict     parameters for prediction terminal
        Terminal    neurotron terminal
        Token       wrapper for token dicts
        SynapseErr  Synapse Exception
        Toy         creating toy stuff
        Train       sequence trainer

    functions:
        follow      following matrix during matrix iteration
"""

import neurotron.cluster.cells
import neurotron.cluster.setup
import neurotron.cluster.terminal
import neurotron.cluster.monitor
import neurotron.cluster.toy
import neurotron.cluster.trainer

#===============================================================================
# classes
#===============================================================================

Collab = setup.Collab
Excite = setup.Excite
Predict = setup.Predict
Terminal = terminal.Terminal

Cluster = cells.Cluster
Cell = cells.Cell
Token = cells.Token
SynapseErr = cells.SynapseErr

Toy = toy.Toy

Record = monitor.Record

Train = trainer.Train

#===============================================================================
# functions
#===============================================================================

follow = cells.follow
