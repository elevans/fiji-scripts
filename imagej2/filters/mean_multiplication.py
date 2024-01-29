#@ OpService ops
#@ ImgPlus img
#@ Long (label="Radius:", style="format:#", min=0, stepsize=1, value=0) radius
#@ String (choices={"Diamond", "Hyper Sphere"}, style="listBox") shape
#@output ImgPlus img_out

from net.imglib2.algorithm.math import ImgMath
from net.imglib2.algorithm.neighborhood import (DiamondShape,
                                                HyperSphereShape)

# create a map for the shapes
shape_map = {
    "Diamond": DiamondShape,
    "Hyper Sphere": HyperSphereShape,
}

# convert input image type to 32-bit
img = ops.convert().float32(img)

# apply mean filter
img_m = ops.create().img(img)
ops.filter().mean(img_m, img, shape_map.get(shape)(radius))

# multiply mean image with input image
img_out = ops.create().img(img)
ImgMath.computeInto(ImgMath.mul(img, img_m), img_out)