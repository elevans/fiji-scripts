#@ OpEnvironment ops
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ Double (label = "Sigma:", style = "format:0.00", min = 0.0, value = 0.0) sigma

from net.imglib2.type.numeric.real import FloatType

def gaussian_high_pass_filter(image, sigma):
    """Apply a Gaussian high pass filter to an input image.

    Apply a Guassian high pass filter by applyinmg a guassian
    blur to the input image and subtracting from the original.

    :param image:

        Input image.

    :param sigma:

        Input Sigma value for Gaussian blur.

    :return:

        High pass filtered image.
    """
    gauss_image = ops.op("filter.gauss").input(image, sigma).apply()
    high_pass_image = ops.op("create.img").input(image, FloatType()).apply()
    ops.op("math.sub").input(image, gauss_image).output(high_pass_image).compute()

    return high_pass_image

ui.show("high pass filter result - sigma: {}".format(sigma),
        gaussian_high_pass_filter(img, sigma))
