#@ String(label="Threshold Method", required=True, choices={'Default', 'Huang', 'Intermodes', 'IsoData', 'Li', 'MaxEntropy', 'Mean', 'MinError', 'Minimum', 'Moments', 'Otsu', 'Percentile', 'RenyiEntropy', 'Shanbhag', 'Triangle', 'Yen'}) method
#@ ImagePlus(label="Input image", required=True) imp
#@ UIService ui
#@OUTPUT ImagePlus imp

import ij.IJ as IJ
import ij.plugin.frame.RoiManager as RoiManager


def get_roi_manager():
    rm = RoiManager.getRoiManager()
    rm.runCommand("Reset")

    return rm

rm = get_roi_manager()
mask = imp.duplicate()
IJ.setAutoThreshold(mask, "{} dark no-reset".format(method))
IJ.run(mask, "Convert to Mask", "")
IJ.run(mask, "Analyze Particles...", "  show=Nothing clear add")
rm.runCommand(imp, "Show All without labels")
rm.runCommand(imp, "Measure")