#@ OpEnvironment ops
#@ UIService ui
#@ ImgPlus img
#@ String (visibility = MESSAGE, value = "<b>Channel settings</b>", required = false) ch_msg
#@ String (label = "Channel A name", value = "a") ch_a_name
#@ String (label = "Channel B name", value = "b") ch_b_name
#@ Integer (label = "Channel A position", value = 1) ch_a
#@ Integer (label = "Channel B position", value = 2) ch_b
#@ String (visibility = MESSAGE, value = "<b>Mesh settings</b>", required = false) mesh_msg
#@output Object output

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.algorithm.neighborhood import HyperSphereShape
from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import LabelRegions
from net.imglib2.type.logic import BitType
from net.imglib2.type.numeric.real import FloatType

from org.scijava.table import DefaultGenericTable

from jarray import array

def extract_channel(image, ch):
    """Extract a channel from the input image.

    Extract the given channel from the input image.

    :param image:

        Input Img.

    :param ch:

        Channel number to extract.

    :return:

        A view of the extracted channel.
    """
    # find C and Z axis indicies
    c_idx = find_axis_index(image, "Channel")
    z_idx = find_axis_index(image, "Z")

    return ops.op("transform.hyperSliceView").input(image, c_idx, ch - 1).apply()


def extract_inside_mask(mask_a, mask_b):
    """Extract the mask "A" data from regions inside mask "B".

    Extract the mask "A" data from regions inside mask "B" using
    logical operations.
    """
    # create Img containers
    tmp = ops.op("create.img").input(mask_a, BitType()).apply()
    out = ops.op("create.img").input(mask_a, BitType()).apply()

    # perform logical operations on masks
    ops.op("logic.or").input(mask_a, mask_b).output(tmp).compute()
    ops.op("logic.xor").input(tmp, mask_b).output(out).compute()
    ops.op("copy.img").input(out).output(tmp).compute()
    ops.op("logic.xor").input(tmp, mask_a).output(out).compute()

    return out

def find_axis_index(image, axis_label):
    """Find the index of the given axis label.

    Find the axis index of the given axis label. If no
    label match is found, return None.

    :param image:

        Input Img.

    :param axis_label:

        Axis label to find.

    :return:

        The index of the given axis label in the image.
    """
    for i in range(len(image.dimensionsAsLongArray())):
        if axis_label == image.axis(i).type().toString():
            return i
        else:
            continue

    return None


def gaussian_subtraction(image, sigma):
    """Perform a Gaussian subtraction on an image.

    Apply a Gaussian blur and subtract from input image.

    :param image:

        Input Img.

    :param sigma:

        Sigma value.

    :return:

        Gaussian blur subtracted image.
    """
    blur = ops.op("filter.gauss").input(image, sigma).apply()
    out = ops.op("create.img").input(image, FloatType()).apply()
    ops.op("math.sub").input(image, blur).output(out).compute()

    return out

# extract channels
ch_a_img = extract_channel(img, ch_a)
ch_b_img = extract_channel(img, ch_b)

# customize the following sections below for your own data
# clean up channel "A" and create a mask
ch_a_img = gaussian_subtraction(ch_a_img, 8.0)
ch_a_ths = ops.op("create.img").input(ch_a_img, BitType()).apply()
ops.op("threshold.triangle").input(ch_a_img).output(ch_a_ths).compute()
ch_a_mask = ops.op("morphology.open").input(ch_a_ths, HyperSphereShape(1), 4).apply()

# clean up channel "B" and create a mask
ch_b_ths= ops.op("create.img").input(ch_b_img, BitType()).apply()
ops.op("threshold.otsu").input(ch_b_img).output(ch_b_ths).compute()
ch_b_mask = ops.op("morphology.open").input(ch_b_ths, HyperSphereShape(2), 4).apply()
ch_b_mask = ops.op("morphology.fillHoles").input(ch_b_mask, HyperSphereShape(2)).apply()

# process the data
output = extract_inside_mask(ch_a_mask, ch_b_mask)
labeling = ops.op("labeling.cca").input(output, StructuringElement.EIGHT_CONNECTED).apply()
meshes = create_meshes(mask, labeling)

# create a table and make measurement
table = DefaultGenericTable(3, 0)
table.setColumnHeader(0, "{} size (pixels)".format(ch_a_name))
table.setColumnHeader(1, "{} volume (um^3)".format(ch_a_name))
table.setColumnHeader(2, "{} sphericity".format(ch_a_name))

regs = LabelRegions(labeling)
i = 0
for r in regs:
    # create meshes per region
    crop = ops.op("transform.intervalView").input(
            output,
            r.minAsDoubleArray(),
            r.maxAsDoubleArray()
            ).apply()
    mesh = ops.op("geom.marchingCubes").input(crop).apply()
    table.appendRow()
    table.set("{} size (pixels)".format(ch_a_name), i, ops.op("stats.size").input(Regions.sample(r, output)).apply())
    # TODO add Img calibration
    table.set("{} volume (um^3)".format(ch_a_name), i, ops.op("geom.size").input(mesh).apply())
    table.set("{} sphericity".format(ch_a_name), i, ops.op("geom.sphericity").input(mesh).apply())
    i += 1

ur.show(table)
