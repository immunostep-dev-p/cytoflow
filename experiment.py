import cytoflow
# import pandas
# import matplotlib
import numpy

f = r"C:\Users\pract\Documents\Practicas\4.fcs"
tube = cytoflow.Tube(file = f)

import_op = cytoflow.ImportOp(tubes = [tube], channels = {"R1-A" : "R1-A", "B8-A" : "B8-A"})
experiment = import_op.apply()
experiment
# print(experiment)

range_2_d = cytoflow.Range2DOp(name = "Test", xchannel = "R1-A", ychannel = "B8-A")

range_2_d.default_view(xscale = "logicle", yscale = "logicle", interactive = True).plot(experiment)
cytoflow.DensityView(xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle").plot(experiment, gridsize = 100, smoothed = True)

k_means = cytoflow.KMeansOp(name = "KMeans", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, num_clusters = 5)
k_means.estimate(experiment)
experiment_kmeans = k_means.apply(experiment)
k_means.default_view().plot(experiment_kmeans)

gaussian_mixture = cytoflow.GaussianMixtureOp(name = "GaussianMixture", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, num_components = 2)

gaussian_mixture.estimate(experiment)
experiment_gaussian_mixture = gaussian_mixture.apply(experiment)

gaussian_mixture.default_view().plot(experiment_gaussian_mixture, alpha = 0.1)

new_experiment = cytoflow.ImportOp(tubes = [tube]).apply()
new_experiment
# print(new_experiment)

flow_peaks = cytoflow.FlowPeaksOp(name = "FlowPeaks", channels = ["R1-A", "B8-A"], scale = {"R1-A" : "logicle", "B8-A" : "logicle"}, h0 = 0.8)

flow_peaks.estimate(new_experiment)
new_experiment_flow_peaks = flow_peaks.apply(new_experiment)
flow_peaks.default_view().plot(new_experiment_flow_peaks)
cytoflow.ScatterplotView(xchannel = "R1-A", xscale = "logicle", ychannel = "B8-A", yscale = "logicle", huefacet = "FlowPeaks").plot(new_experiment_flow_peaks)

new_experiment_flow_peaks.data
# print(new_experiment_flow_peaks.data)

count = new_experiment_flow_peaks[["FlowPeaks"]].groupby(by = new_experiment_flow_peaks["FlowPeaks"]).count()
count
# print(count)

umbral = abs(new_experiment_flow_peaks["R1-A"].max() / new_experiment_flow_peaks["R1-A"].min())
umbral
# print(umbral)

indice = new_experiment_flow_peaks["R1-A"].loc[new_experiment_flow_peaks["R1-A"] < umbral].index
indice
# print(indice)

cluster = new_experiment_flow_peaks[["FlowPeaks"]].drop(indice).groupby(by = new_experiment_flow_peaks["FlowPeaks"].drop(indice)).count()
cluster
# print(cluster)

p_cluster = cluster.index[numpy.argmax(cluster.to_numpy())]
p_cluster
# print(p_cluster)

bead_cluster = new_experiment_flow_peaks[new_experiment_flow_peaks["FlowPeaks"] == p_cluster]
bead_cluster
# print(bead_cluster)

media = bead_cluster["B4-A"].mean()
media
# print(media)

stats = bead_cluster["B4-A"].describe()
stats
# print(stats)

full_stats = bead_cluster.describe()
full_stats
# print(full_stats)