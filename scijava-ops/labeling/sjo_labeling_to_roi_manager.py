#@ OpEnvironment ops
#@ ConvertService cs
#@ Img (label = "Input image:", autofill = false) img

from net.imglib2.roi.labeling import ImgLabeling, LabelRegions

from ij.gui import PolygonRoi
from ij.plugin.frame import RoiManager

def label_image_to_contours(image):
    """Get label image contours.

    Convert a label image into a list of contours.

    :param image:

        Input label image (typically 16-bit)

    :return:

        A list of object contours.
    """
    # convert label image to ImgLabeling
    contours = []
    labeling = cs.convert(image, ImgLabeling)
    regions = LabelRegions(labeling)
    for r in regions:
        contours.append(ops.op("geom.contour").input(r, True).apply())

    return contours

# get rois from label image as countours
rois = label_image_to_contours(img)

# add rois to the ROI Manager
rm = RoiManager.getRoiManager()
for r in rois:
    # convert ImgLib2 contour to ImageJ roi
    rm.addRoi(cs.convert(r, PolygonRoi))
