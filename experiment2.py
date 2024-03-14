import cytoflow

f = r"1.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

threshold_op = cytoflow.ThresholdOp(name = "Threshold", channel = "R1-A", threshold = 2000)

threshold_op.default_view(scale = "logicle", interactive = True).plot(experiment)

experiment_threshold = threshold_op.apply(experiment)
# experiment_threshold.data.groupby('Threshold').size()
experiment_threshold = experiment_threshold.query("Threshold")

density_gate_op = cytoflow.DensityGateOp(name = "DensityGate", xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", keep = 0.5)

density_gate_op.estimate(experiment_threshold)

density_gate_op.default_view().plot(experiment_threshold)

experiment_density_gate = density_gate_op.apply(experiment_threshold)
experiment_threshold = experiment_threshold.query("DensityGate")

flow_peaks_op = cytoflow.FlowPeaksOp(name = "FlowPeaks", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, h0 = 3)

flow_peaks_op.estimate(experiment_density_gate)

flow_peaks_op.default_view(density = True).plot(experiment_density_gate)

experiment_flow_peaks = flow_peaks_op.apply(experiment_density_gate)
experiment_threshold = experiment_threshold.query("FlowPeaks")

flow_peaks_op.default_view().plot(experiment_flow_peaks)