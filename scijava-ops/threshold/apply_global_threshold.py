#@ OpEnvironment ops
#@ UIService ui
#@ Img (label="Input image:", autofill=false) img
#@ String (label="Global threshold method:", choices={"huang", "ij1", "intermodes", "isoData", "li", "maxEntropy", "maxLikelihood", "mean", "minError", "minimum", "moments", "otsu", "percentile", "renyiEntropy", "rosin", "shanbhag", "triangle", "yen"}, style="listBox") method

from net.imglib2.type.logic import BitType

out = ops.op("create.img").input(img, BitType()).apply()
ops.op("threshold.{}".format(method)).input(img).output(out).compute()
ui.show("{} threshold output".format(method), out)
