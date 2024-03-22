#@ OpService ops
#@ ConvertService cs
#@ UIService ui
#@ Dataset (label="label image") label_img
#@ Dataset (label="target image") target_img

from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import ImgLabeling, LabelRegions
from org.scijava.table import DefaultGenericTable

def split_dataset(image, axis=2):
    """
    Create views along the specified axis for the given
    Dataset.

    :param image: Input Dataset
    :param axis: Index of axis to slice (default=2)
    :return: A list of Views along the axis
    """
    views = []
    for i in range(image.dimensionsAsLongArray()[axis]):
        views.append(ops.transform().hyperSliceView(image, axis, i))
    
    return views


def run(label_img, target_img):
    """
    Measure the integrated density (IntDen) of a label
    across a Dataset's channel axis.

    :param label_img: Input label image (Dataset)
    :param target_img: Input target image (Dataset)
    """
    # split datasets
    target_img_chs = split_dataset(target_img, 2)
    label_img_time = split_dataset(label_img, 2)
    cal = target_img.averageScale(0) * target_img.averageScale(1) # pixel width and pixel height calibration
    num_chs = len(target_img_chs)
    t_count = len(label_img_time) # number of timepoints

    # set up table
    table = DefaultGenericTable(num_chs + 2, 0)
    table.setColumnHeader(0, "cell ID")
    table.setColumnHeader(1, "time")
    for col in range(num_chs):
        table.setColumnHeader(col + 2, "IntDen_ch_{}".format(col))

    img_time = {}
    for c in range(num_chs):
        img_time[c] = split_dataset(target_img_chs[c], 2)

    row = 0
    for t in range(t_count):
        tmp_labeling = cs.convert(label_img_time[t], ImgLabeling)
        tmp_regs = LabelRegions(tmp_labeling)
        for r in tmp_regs:
            table.appendRow()
            table.set("cell ID", row, r.getLabel())
            table.set("time", row, t)
            for c in range(num_chs):
                sample = Regions.sample(r, img_time.get(c)[t])
                mfi = ops.stats().mean(sample).getRealDouble()
                size = ops.stats().size(sample).getRealDouble()
                table.set("IntDen_ch_{}".format(c), row, mfi * (size * cal))
            row += 1

    ui.show(table)

# convert label image to labeling
run(label_img, target_img)