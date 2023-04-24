#@ UIService ui
#@ OpService ops
#@ ImgPlus(label="Input image", required=True) input_img
#@ Double sigma(label="sigma:", value=1.0)
#@output ImgPlus output_img

from net.imglib2.algorithm.math import ImgMath

input_img = ops.convert().float32(input_img)
img_g = ops.filter().gauss(input_img, sigma)
output_img = ImgMath.computeInto(ImgMath.sub(input_img, img_g), input_img.copy())