import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

threshold_op = cytoflow.ThresholdOp(name = "Threshold", channel = "R1-A", threshold = 2000)

threshold_op.default_view(scale = "logicle", interactive = True).plot(experiment)

experiment2 = threshold_op.apply(experiment)
experiment2.data.groupby('Threshold').size()

threshold_op = cytoflow.ThresholdOp(name = "Threshold2", channel = "R1-A", threshold = 2000)
threshold_op.default_view(interactive = True).plot(experiment2)
experiment3 = threshold_op.apply(experiment2)