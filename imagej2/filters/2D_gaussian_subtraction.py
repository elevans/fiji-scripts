#@ OpService ops
#@ ImgPlus img
#@ Double (label="Sigma:", style="format:#.00", min=0.0, stepsize=0.5, value=0.00) sigma
#@output ImgPlus img_out

from net.imglib2.algorithm.math import ImgMath

# convert input ImgPlus to float32
img = ops.convert().float32(img)

# apply gaussian blur
img_g = ops.filter().gauss(img, sigma)

# subtract input ImgPlus from gaussian blurred image
img_out = ImgMath.computeInto(ImgMath.sub(img, img_g), img.copy())