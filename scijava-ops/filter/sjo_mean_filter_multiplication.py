#@ OpEnvironment ops
#@ Img (label = "Input image:", autofill = false) img
#@ Integer (label = "Radius:", min = 1, value = 1) radius
#@ String (label = "Neighborhood shape:", choices = {"Diamond", "Diamond tips", "Hyper sphere"}, style = "listBox", value = "Hyper sphere") shape_type
#@output Img output

from net.imglib2.algorithm.neighborhood import (
        DiamondShape,
        DiamondTipsShape,
        HyperSphereShape
        )
from net.imglib2.type.numeric.real import FloatType

if shape_type == "Diamond":
    shape = DiamondShape(radius)
if shape_type == "Diamond tips":
    shape = DiamondTipsShape(radius)
if shape_type == "Hyper sphere":
    shape = HyperSphereShape(radius)

mean_img = ops.op("create.img").input(img, FloatType()).apply()
output = ops.op("create.img").input(img, FloatType()).apply()
ops.op("filter.mean").input(img, shape).output(mean_img).compute()
ops.op("math.multiply").input(img, mean_img).output(output).compute()
