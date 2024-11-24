#@ OpEnvironment ops
#@ Img (label = "Input image:", autofill = false) img
#@ Integer (label = "Lifetime axis:", value = 2) lt_axis
#@ Float (label = "Intensity threshold:", min = 0) int_thresh
#@ Float (label = "Time base (ns)", min = 12.5) time_base
#@ Integer (label = "Time bins", min = 0, value = 256) time_bins
#@ Integer (label = "Bin kernel radius:", value = 1) radius 
#@output Img output

from org.scijava.ops.flim import FitParams
from org.scijava.ops.flim import Pseudocolor

# set FLIM parameter config
param = FitParams()
param.transMap = img # FLIM image
param.ltAxis = lt_axis # lifetime axis index
param.iThresh = int_thresh # intensity threshold value
param.xInc = time_base / time_bins # time increment between two consecutive data points

# fit curves
kernel = ops.op("create.kernelSum").input(1 + 2 * radius).apply()
phasor_results = ops.op("flim.fitPhasor").input(param).apply()

# view the fit output
output = phasor_results.paramMap
