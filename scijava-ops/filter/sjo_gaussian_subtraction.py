#@ OpEnvironment ops
#@ Img (label = "Input image:", autofill = false) img
#@ Double (label = "Sigma:", style = "format:0.00", min = 0.0, value = 0.0) sigma
#@output Img output

from net.imglib2.type.numeric.real import FloatType

gauss_img = ops.op("filter.gauss").input(img, sigma).apply()
output = ops.op("create.img").input(img, FloatType()).apply()
ops.op("math.sub").input(img, gauss_img).output(output).compute()
