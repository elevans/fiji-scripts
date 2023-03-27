#@ String(label="Threshold Method", required=True, choices={'otsu', 'huang'}) method
#@ ImgPlus(label="Input Dataset", required=True) data
#@ DatasetService ds
#@ OpService ops
#@ UIService ui
#@OUTPUT Dataset output

import ij.IJ as IJ
import ij.plugin.frame.RoiManager as RoiManager
from ij.measure import ResultsTable
from collections import defaultdict
from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import LabelRegions

def get_roi_manager():
    rm = RoiManager.getRoiManager()
    rm.runCommand("Reset")
    return rm


def get_region_labels(regions):
    return list(regions.getExistingLabels())


def apply_threshold(method, img):
    h = ops.run("image.histogram", img)
    t_val = ops.run("threshold.{}".format(method), h)
    t_out = ops.run("threshold.apply", img, t_val)
    return t_out


def run_cca(img, add_to_roi_manager=True):
    return ops.run("cca", img, StructuringElement.EIGHT_CONNECTED)


def compute_stats(labeling, img):
    regions = LabelRegions(labeling)
    for r in regions:
        stats = defaultdict(list)
        samples = Regions.sample(r, img)
        stats["area"].append(ops.run("stats.size", samples).getRealDouble())
        stats["mean"].append(ops.run("stats.mean", samples).getRealDouble())
        min_max = ops.run("stats.minMax", samples)
        stats["min"].append(min_max.getA().getRealDouble())
        stats["max"].append(min_max.getB().getRealDouble())

    # create an empty table
    table = ResultsTable()

    # add columns to the table
    for key in stats.keys():
        table.setHeading(key)
    
    # add rows to the table
    num_rows = max([len](x) for x in stats.values())
    for i in range(num_rows):
        row = []
        for key in stats.keys():
            if i < len(stats[key]):
                row.append(stats[key][i])
            else:
                row.append('')
        table.addRow(row)
    
    return table

get_roi_manager()
mask = apply_threshold(method, data)
ui.show("mask", mask)
labeling = run_cca(mask)
results_table = compute_stats(labeling, data)
results_table.show('Results')
print("Done!")