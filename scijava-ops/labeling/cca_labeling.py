#@ OpEnvironment ops
#@ UIService ui
#@ Img (label="Input image:", autofill=false) img
#@ String (label="Structuring Element type:", choices={"FOUR", "EIGHT"}, style="listBox") strel_type
#@output Img output

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement

# get the structuring element
if strel_type == "FOUR":
    strel = StructuringElement.FOUR_CONNECTED
else:
    strel = StructuringElement.EIGHT_CONNECTED

output = ops.op("labeling.cca").input(img, strel).apply()
