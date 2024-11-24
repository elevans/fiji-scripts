#@ OpEnvironment ops
#@ Img (label = "FLIM Image:", autofill = false) img
#@ Integer (description = "Index of the lifetime axis in the data.", label = "Lifetime index axis:", min = 0, value = 2) lt_axis
#@ Float (description = "The time period the data was acquired at.", label = "Time period (ns):", style = "format:0.00", value = 12.5) t_period
#@ Integer (description = "The number of time bins", label = "Time bins:", min = 0, value = 256) t_bins
#@ File (description = "Enter the path to the IRF file.", label = "IRF file (optional):", style = "file", required = false) irf_path

from array import array

from org.scijava.ops.flim import FitParams

def read_irf(path):
    """Load an IRF file into an array.

    :param path:

        Path to the IRF text file.

    :return:

        IRF as a list of array.
    """
    with open(path.getAbsolutePath(), 'r') as f:
        arr = array('f', (float(l.strip()) for l in f))

    return arr

# set params
flim_params = FitParams()
flim_params.transMap = img
flim_params.ltAxis = lt_axis
flim_params.xInc = t_period / t_bins
if irf_path:
    flim_params.instr = read_irf(irf_path)
