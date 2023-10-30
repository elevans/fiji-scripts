#@ OpService ops
#@ ConvertService cs
#@ ImgPlus img
#@ Integer min_size(label="Minimum size (pixels):", value=0)
#@ Integer max_size(label="Maximum size (pixels):", value=0)

from net.imglib2.roi.labeling import ImgLabeling
from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import LabelRegions

def remove_label(sample):
    c = sample.cursor()
    while c.hasNext():
        c.fwd()
        c.get().set(0)

def filter_labeling(index_img, labeling, min_size, max_size):
    """
    :param index_img: An index image
    :param labeling:
    :param min_size:
    :param max_size:
    """
    regs = LabelRegions(labeling)
    for r in regs:
        sample = Regions.sample(r, index_img)
        size = float(str(ops.stats().size(sample)))
        # if region size is outside of min/max range set to zero
        if size <= float(min_size) or size >= float(max_size):
            remove_label(sample)

# convert index image to labeling
labeling = cs.convert(img, ImgLabeling)
filter_labeling(img, labeling, min_size ,max_size)