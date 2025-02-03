#@ OpEnvironment ops
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ String (visibility = MESSAGE, value ="<b>[ Phasor settings ]</b>", required = false) phs_msg
#@ Integer (label = "Lifetime axis:", value = 2) lt_axis
#@ Float (label = "Time base (ns)", min = 0, value = 12.5) time_base
#@ Integer (label = "Time bins", min = 0, value = 256) time_bins
#@ String (visibility = MESSAGE, value ="<b>[ Output settings ]</b>", required = false) out_msg
#@ Boolean (label = "Show phasor map:", value = false) show_map
#@ Boolean (label = "Show phasor plot:", value = false) show_plot
#@ String (label = "Universal circle:", choices={"None", "Full", "Half"}, style="listBox", value = "None") uc_style
#@ String (visibility = MESSAGE, value ="<b>[ Phasor coordinates CSV export settings ]</b>", required = false) exp_msg
#@ Boolean (label = "Export coordinates:", value = false) export_coords
#@ File (label = "Output directory:", style = "directory", required = false) out_dir
#@ String (label = "Filename:") filename

import os
import math
import csv
from ij.gui import Plot
from org.scijava.ops.flim import FitParams
from java.awt import Color

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


def get_universal_circle(points=100, style="Full"):
    """Compute the points for a universal circle.

    :param points:
        The number of points to compute.

    :param style:
        Full or half circle.

    :return:
        A tuple of lists containing pair 'x' and 'y' coordinates
        for the universal circle.
    """
    # calculate angle increment
    if style == "Full":
        ai = 2 * math.pi / points
    if style == "Half":
        ai = math.pi / points

    # calculate points along the circle
    x = []
    y = []
    for p in range(points):
        theta = p * ai
        x.append(math.cos(theta))
        y.append(math.sin(theta))

    # complete the circle by adding the first position to the end
    if style == "Full":
        x.append(x[0])
        y.append(y[1])

    return (x, y)

# set FLIM parameter config
param = FitParams()
param.transMap = img # FLIM image
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
    # initialize the scatter plot
    p = Plot("phasor plot", "g", "s")
    # add data points
    p.setColor(Color.BLUE)
    p.addPoints(phasor_coords[0], phasor_coords[1], Plot.DOT)
    # optinally add universal circle
    if uc_style != "None":
        uc = get_universal_circle(style=uc_style)
        p.setColor(Color.BLACK)
        p.addPoints(uc[0], uc[1], Plot.CONNECTED_CIRCLES)
    p.draw()
    p.show()
if export_coords:
    # export g and s coords
    coords_to_csv(
            phasor_coords[0],
            phasor_coords[1],
            out_dir.getAbsolutePath(),
            filename + ".csv"
            )
