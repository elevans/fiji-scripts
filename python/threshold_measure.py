#@ String(label="Threshold Method", required=True, choices={'otsu', 'huang'}) method
#@ ImgPlus(label="Input Dataset", required=True) data
#@ DatasetService ds
#@ OpService ops
#@ UIService ui
#@OUTPUT Dataset output

import ij.IJ as IJ
import ij.plugin.frame.RoiManager as RoiManager
from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi.labeling import LabelRegions

def get_roi_manager():
    rm = RoiManager.getRoiManager()
    rm.runCommand("Reset")
    return rm


def get_region_labels(regions):
    return list(regions.getExistingLabels())


def apply_threshold(method):
    h = ops.run("image.histogram", data)
    t_val = ops.run("threshold.{}".format(method), h)
    t_out = ops.run("threshold.apply", data, t_val)
    return t_out


def run_cca(img, add_to_roi_manager=True):
    img_l = ops.run("cca", img, StructuringElement.EIGHT_CONNECTED)
    return LabelRegions(img_l)


def compute_stats(regions, img, stats):
    return

get_roi_manager()
mask = apply_threshold(method)
ui.show("mask", mask)
regions = run_cca(mask)
labels = get_region_labels(regions)
print("Done!")