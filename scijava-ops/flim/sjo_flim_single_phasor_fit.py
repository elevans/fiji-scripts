#@ OpEnvironment ops
#@ PlotService ps
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ String (visibility = MESSAGE, value ="<b>[ Phasor settings ]</b>", required = false) phs_msg
#@ Integer (label = "Lifetime axis:", value = 2) lt_axis
#@ Float (label = "Time base (ns)", min = 0, value = 12.5) time_base
#@ Integer (label = "Time bins", min = 0, value = 256) time_bins
#@ Integer (label = "Median filter Kernel size:", min = 0, value = 0) kernel_size
#@ String (visibility = MESSAGE, value ="<b>[ Output settings ]</b>", required = false) out_msg
#@ Boolean (label = "Show phasor map:", value = false) show_map
#@ Boolean (label = "Show phasor plot:", value = false) show_plot
#@ Boolean (label = "Draw universal half circle:", value = false) draw_uc
#@ String (visibility = MESSAGE, value ="<b>[ Phasor coordinates CSV export settings ]</b>", required = false) exp_msg
#@ Boolean (label = "Export coordinates:", value = false) export_coords
#@ File (label = "Output directory:", style = "directory", required = false) out_dir
#@ String (label = "Filename:", required = false) filename

import os
import math
import csv
from math import cos, sin, pi
from net.imglib2.algorithm.neighborhood import RectangleShape
from net.imglib2.view import Views
from org.scijava.ops.flim import FitParams
from org.scijava.plot import LineStyle, MarkerStyle
from org.scijava.util import ColorRGB

def coords_to_csv(u, v, path, name):
    """Export the u and v coordinates to a .csv file.

    :param u:
        The 'u' coordinate (i.e. 'x' or 'g').

    :param v:
        The 'v' coordinate (i.e. 'y' or 'g').

    :param path:
        The path to save the file.

    :param name:
        The name of the file, without the .csv suffix.
    """
    f = os.path.join(path, name)
    print(f)
    with open(f, "w") as stream:
        # write header
        stream.write("G,S\n")
        for g, s in zip(u, v):
            # write data row by row
            stream.write("{},{}\n".format(g, s))

def extract_phasor_coordinates(img_u, img_v):
    """Extract the 'x' and 'y' phasor coordinates from Imgs.

    Use a cursor and random access to extract each pixel's value
    (i.e. 'u' or 'v'). The random access is set to the cursor's
    position, ensuring 'u' and 'v' are properly linked.

    :param img_u:
        The image containing 'u' values.

    :param img_v:
        The image containing 'v' values.

    :return:
        A tuple of lists containing paired 'u' and 'v' values.
    """
    # get a cursor and random access on the input data
    c = img_u.cursor()
    ra = img_v.randomAccess()
    u = []
    v = []
    while c.hasNext():
        c.fwd()
        u.append(c.get().getRealDouble())
        ra.setPosition(c)
        v.append(ra.get().getRealDouble())

    return (u, v)


def get_universal_circle(points=100):
    """Compute the points for a universal circle.

    :param points:
        The number of points to compute.

    :param style:
        Full or half circle.

    :return:
        A tuple of lists containing pair 'x' and 'y' coordinates
        for the universal circle.
    """
    # universal circle parameters
    radius = 0.5
    center = (0.5, 0.0)

    # calculate points along the circle
    x = []
    y = []
    for p in range(points + 1):
        # angle from 0 to 2*pi
        theta = pi * p / points
        x.append(center[0] + radius * cos(theta))
        y.append(center[1] + radius * sin(theta))

    return (x, y)


def label_universal_circle(plot):
    """Add decay labels to the universal circle.
    """
    # add fixed 0 ns and inf ns decay labels
    plot.addText("0 ns", 1.0, 0.0)
    plot.addText("inf ns", 0.0, 0.0)

    # TODO: compute taus along the universal circle

# apply median kernel filter to input image
if kernel_size > 0:
    shape = RectangleShape(kernel_size, False)
    stack = []
    for i in range(img.dimensionsAsLongArray()[2]):
        view = ops.op("transform.hyperSliceView").input(img, 2, i).apply()
        m_img = ops.op("create.img").input(view).apply()
        ops.op("filter.median").input(view, shape).output(m_img).compute()
        # add a channel dimension to median_imga
        stack.append(ops.op("transform.addDimensionView").input(m_img, 1, 1).apply())
    trans_map = Views.concatenate(2, stack)
else:
    trans_map = img

# set FLIM parameter config
param = FitParams()
param.transMap = trans_map # FLIM image
param.ltAxis = lt_axis # lifetime axis index
param.xInc = time_base / time_bins # time increment between two consecutive data points

# run phasor analysis with FLIMLib
phasor_results = ops.op("flim.fitPhasor").input(param).apply()

# get phasor results as a 3D (X, Y, C) Img
# each channel represents an output of the phasor analysis
# [z, u, v, tauPhi, tauMod, tau]
# z = the precomputed background, to be subtracted from input (default is 0)
# u = the 'horizontal' or real axis (i.e. 'x' or 'g')
# v = the 'vertical' or imaginary axis (i.e. 'y' or 's')
# tauPhi = the lifetime calculated from the phase change
# tauMod = the lifetime calculated from the amplitude change (i.e. demodulation)
# tau = the mean tau of the other taus
phasor_img = phasor_results.paramMap
img_u = ops.op("transform.hyperSliceView").input(phasor_img, 2, 1).apply()
img_v = ops.op("transform.hyperSliceView").input(phasor_img, 2, 2).apply()
phasor_coords = extract_phasor_coordinates(img_u, img_v)

# outputs
if show_map:
    ui.show("Phasor output map", phasor_img)
if show_plot:
    # initialize a plot
    plot = ps.newXYPlot()
    plot.setTitle("FLIMLib Phasor plot")
    plot.xAxis().setLabel("g")
    plot.yAxis().setLabel("s")

    # optionally add the universal circle
    if draw_uc:
        uc_coords = get_universal_circle()
        uc_series = plot.addXYSeries()
        uc_series.setLabel("universal circle")
        uc_series.setValues(uc_coords[0], uc_coords[1])
        uc_style = ps.newSeriesStyle(
                ColorRGB("black"),
                LineStyle.DASH,
                MarkerStyle.CIRCLE
                )
        uc_series.setStyle(uc_style)

    # add data points
    data_series = plot.addXYSeries()
    data_series.setLabel("phasor data")
    data_series.setValues(phasor_coords[0], phasor_coords[1])
    data_style = ps.newSeriesStyle(
            ColorRGB("blue"),
            LineStyle.NONE,
            MarkerStyle.PLUS
            )
    data_series.setStyle(data_style)

    # show the plot
    ui.show(plot)

if export_coords:
    # export g and s coords
    coords_to_csv(
            phasor_coords[0],
            phasor_coords[1],
            out_dir.getAbsolutePath(),
            filename + ".csv"
            )
