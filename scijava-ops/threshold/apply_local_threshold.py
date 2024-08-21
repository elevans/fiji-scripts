#@ OpEnvironment ops
#@ UIService ui
#@ Img (label="Input image:", autofill=false) img
#@ String (label="Local threshold method:", choices={"huang", "ij1", "intermodes", "isoData", "li", "maxEntropy", "maxLikelihood", "mean", "minError", "minimum", "moments", "otsu", "percentile", "renyiEntropy", "rosin", "shanbhag", "triangle", "yen"}, style="listBox") method
#@ String (label="Neighborhood shape:", choices={"Diamond", "Diamond tips", "Rectangle", "Sphere"}, style="listBox") shape_type
#@ Integer (label="Shape radius/Span (pixels):", min=1, value=1) rds_spn
#@ String (label="Rectangle center:", choices={"keep", "skip"}, style="listBox") center

from net.imglib2.algorithm.neighborhood import (
        DiamondShape,
        DiamondTipsShape,
        HyperSphereShape,
        RectangleShape
        )
from net.imglib2.type.logic import BitType

# create requested neighborhood shape
if shape_type == "Diamond":
    shape = DiamondShape(rds_spn)
if shape_type == "Diamond tips":
    shape = DiamondTipsShape(rds_spn)
if shape_type == "Sphere":
    shape = HyperSphereShape(rds_spn)
if shape_type == "Rectangle":
    skip_center = True if center == "skip" else False
    shape = RectangleShape(rds_spn, skip_center)

# apply local threshold with neighborhood shape
out = ops.op("create.img").input(img, BitType()).apply()
ops.op("threshold.{}".format(method)).input(img, shape).output(out).compute()
ui.show("{} threshold output".format(method), out)
