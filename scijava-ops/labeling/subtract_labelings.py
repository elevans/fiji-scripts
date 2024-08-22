#@ OpEnvironment ops
#@ ConvertService cs
#@ Img (label="Input label image A", autofill=false) img_a
#@ Img (label="Input label iamge B", autofill=false) img_b
#@output Img output

from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import ImgLabeling, LabelRegions

def set_to_zero(sample):
    """Set the given sample region pixel values to 0.

    :param: A sample region.
    """
    c = sample.cursor()
    while c.hasNext():
        c.fwd()
        c.get().set(0)


def subtract_label_images(a, b):
    """Subtract Label images from each other.

    Details

    :param a:

        Input label image A.

    :param b:

        Input label Image B.
    """
    # convert to uint16
    a = ops.op("convert.uint16").input(a).apply()
    b = ops.op("convert.uint16").input(b).apply()

    # extract regions and set to zero
    labeling_a = cs.convert(a, ImgLabeling)
    regions_a = LabelRegions(labeling_a)
    for r in regions_a:
        sample = Regions.sample(r, b)
        set_to_zero(sample)

    return cs.convert(b, ImgLabeling)

output = subtract_label_images(img_a, img_b).getIndexImg()
