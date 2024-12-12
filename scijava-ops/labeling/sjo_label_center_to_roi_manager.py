#@ OpEnvironment ops
#@ Img (label = "Input image:", autofill = false) img
#@ String (label = "Structuring Element type:", choices = {"FOUR", "EIGHT"}, style = "listBox") se_type
#@output Img output

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi.labeling import LabelRegions

from ij.gui import PointRoi 
from ij.plugin.frame import RoiManager

def cca(image, se):
    """Run connected component analysis.

    Run connected component analysis (CCA) on the given binary image and
    structuring element.

    :param image:

        Input image.

    :param se:

        Structuring element type: FOUR or EIGHT connected.

    :return:

        An ImgLabeling of the input image.
    """
    # get the structuring element
    if se == "FOUR":
        strel = StructuringElement.FOUR_CONNECTED
    else:
        strel = StructuringElement.EIGHT_CONNECTED

    return ops.op("labeling.cca").input(img, strel).apply()


def center_to_roi_manager(labeling):
    """Add the center of mass of a label to the ROI Manager.

    Add the center of mass for a given region from an ImgLabeling
    to the ROI Manager as a Point ROI.

    :param labeling:

        Input ImgLabeling
    """
    regs = LabelRegions(labeling)
    rm = RoiManager.getRoiManager()
    for r in regs:
        pos = r.getCenterOfMass().positionAsDoubleArray()
        rm.addRoi(PointRoi(pos[0], pos[1]))

labeling = cca(img, se_type)
center_to_roi_manager(labeling)
