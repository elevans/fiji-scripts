#@ String(label="Threshold Method", required=true, choices={'otsu', 'huang'}) method
#@ OpService ops
#@ Dataset data
#@ DatasetService ds
#@ UIService ui
#@OUTPUT Dataset output

import ij.IJ
import ij.gui.PointRoi
import ij.plugin.frame.RoiManager
import net.imglib2.algorithm.labeling.ConnectedComponents.StructuringElement
import net.imglib2.roi.labeling.LabelRegions

// get the histogram
h = ops.run("image.histogram", data)

// apply the selected threshold
t_val = ops.run("threshold.${method}", h)
t_out = ops.run("threshold.apply", data, t_val)
mask = ds.create(t_out)

// get ROIManager instance
rm = RoiManager.getRoiManager()
rm.runCommand("Reset")

// indentify rois
img = mask.getImgPlus()
img_l = ops.run("cca", img, StructuringElement.EIGHT_CONNECTED)
regions = LabelRegions(img_l)
regions_l = regions.getExistingLabels()

// display CCA result
ui.show("labeling", img_l.getIndexImg())