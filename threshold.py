import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f, conditions = {"Dox" : 10.0})

import_op = cytoflow.ImportOp()
import_op.tubes = [tube]
import_op.conditions = {"Dox" : "float"}
experiment = import_op.apply()

threshold_op = cytoflow.ThresholdOp(name = "Threshold", channel = "R1-A", threshold = 2000)

threshold_view = threshold_op.default_view(scale = "log", interactive = True)
threshold_view.plot(experiment)

# print(experiment)