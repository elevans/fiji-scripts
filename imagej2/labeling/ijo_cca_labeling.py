#@ OpService ops
#@ Img (label = "Input binary image:", autofill = false) img
#@ String (label = "Structuring Element type:", choices = {"FOUR", "EIGHT"}, style = "listBox") strel_type
#@output Img label_image

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement

# get the structuring element
if strel_type == "FOUR":
    strel = StructuringElement.FOUR_CONNECTED
else:
    strel = StructuringElement.EIGHT_CONNECTED

labeling = ops.labeling().cca(img, strel)
label_image = labeling.getIndexImg()
