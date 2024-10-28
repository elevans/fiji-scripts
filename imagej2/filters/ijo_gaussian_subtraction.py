#@ OpService ops
#@ Img (label = "Input image:", autofill = false) img
#@ Float (label="Sigma:", style="format:0.00", min=0.0, value=0.00) sigma
#@output Img result

# convert input ImgPlus to float32
img = ops.convert().float32(img)

# apply gaussian blur
img_g = ops.filter().gauss(img, sigma)

# subtract input ImgPlus from gaussian blurred image
result  = ops.math().subtract(img, img_g)
