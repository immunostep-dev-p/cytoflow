import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

flow_peaks_op = cytoflow.FlowPeaksOp(name = "FlowPeaks", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, h0 = 3)

flow_peaks_op.estimate(experiment)

flow_peaks_op.default_view(density = True).plot(experiment)

experiment2 = flow_peaks_op.apply(experiment)

flow_peaks_op.default_view().plot(experiment2)