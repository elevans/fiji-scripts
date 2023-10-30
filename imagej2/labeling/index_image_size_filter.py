#@ OpService ops
#@ ConvertService cs
#@ ImgPlus img
#@ String (visibility=MESSAGE, value="<html>Enter size range (labels within this range are retained):", required=false) msg
#@ Integer min_size(label="Minimum size (pixels):", min=0, value=0)
#@ Integer max_size(label="Maximum size (pixels):", value=0)

from net.imglib2.roi.labeling import ImgLabeling, LabelRegions
from net.imglib2.roi import Regions

def remove_label(sample):
    """
    Set the given sample region pixel values to 0.

    :param: A sample region.
    """
    # get the sample region's cursor
    c = sample.cursor()
    # set all pixels within the sample region to 0
    while c.hasNext():
        c.fwd()
        c.get().set(0)

def filter_labeling(index_img, labeling, min_size, max_size):
    """
    Filter an index image's labels by minimum/maximum pixel size exclusion.

    :param index_img: An index image.
    :param labeling: A labeling created from the index image.
    :param min_size: Minimum label size.
    :param max_size: Maximum label size.
    """
    # get the label regions from the labeling
    regs = LabelRegions(labeling)
    for r in regs:
        # get a sample region and compute the size
        sample = Regions.sample(r, index_img)
        size = float(str(ops.stats().size(sample)))
        # if region size is outside of min/max range set to zero
        if size <= float(min_size) or size >= float(max_size):
            remove_label(sample)

# convert index image to labeling
labeling = cs.convert(img, ImgLabeling)
filter_labeling(img, labeling, min_size ,max_size)