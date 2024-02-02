#@ OpService ops
#@ ImgPlus img
#@ Double (label="Sigma:", style="format:#.00", min=0.0, stepsize=0.5, value=0.00) sigma
#@output ImgPlus img_out

# convert input ImgPlus to float32
img = ops.convert().float32(img)

# apply gaussian blur
img_g = ops.filter().gauss(img, sigma)

# subtract input ImgPlus from gaussian blurred image
img_out  = ops.math().subtract(img, img_g)