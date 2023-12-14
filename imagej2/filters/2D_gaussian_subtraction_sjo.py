#@ ImgPlus img
#@ Double (label="Sigma:", style="format:#.00", min=0.0, stepsize=0.5, value=0.00) sigma
#@output ImgPlus result

from org.scijava.ops.api import OpEnvironment
from net.imglib2.algorithm.math import ImgMath
from net.imglib2.type.numeric.real import FloatType

# get ops environment
ops = OpEnvironment.getEnvironment()

# convert input ImgPlus to float32
img_float = ops.op("create.img").arity2().input(img, FloatType()).apply()
ops.op("convert.float32").arity1().input(img).output(img_float).compute()

# apply gaussian blur
img_gauss = ops.op("filter.gauss").arity2().input(img_float, sigma).apply()

# subtract input ImgPlus from gaussian blurred image
result = ImgMath.computeInto(ImgMath.sub(img_float, img_gauss), img_float.copy())