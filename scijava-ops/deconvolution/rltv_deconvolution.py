#@ OpEnvironment ops
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ Integer (label = "Iterations", value = 15) iterations
#@ Float (label = "Numerical Aperture", style = "format:0.00", min = 0.00, value = 1.45) numericalAperture
#@ Integer (label = "Emission Wavelength (nm)", value = 457) wavelength
#@ Float (label = "Refractive Index (immersion)", style = "format:0.00", min = 0.00, value = 1.5) riImmersion
#@ Float (label = "Refractive Index (sample)", style = "format:0.00", min = 0.00, value = 1.4) riSample
#@ Float (label = "XY spacing (um/pixel)", style = "format:0.0000", min = 0.0000, value = 0.065) lateral_res
#@ Float (label = "Z spacing (um/pixel)", style = "format:0.0000", min = 0.0000, value = 0.1) axial_res
#@ Float (label="Particle/sample Position (um)", style = "format:0.0000", min = 0.0000, value = 0) pZ
#@ Float (label = "Regularization factor", style = "format:0.00000", min = 0.00000, value = 0.002) regularizationFactor
#@ Boolean (label = "Show PSF", value = false) show_psf
#@output Img result

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.real import FloatType
from net.imglib2.type.numeric.complex import ComplexFloatType
from java.lang import Float

# convert input image to float
img_float = ops.op("create.img").input(img, FloatType()).apply()
ops.op("convert.float32").input(img).output(img_float).compute()

# use image dimensions for PSF size
psf_size = FinalDimensions(img.dimensionsAsLongArray())

# convert the input parameters to meters (m)
wavelength = float(wavelength) * 1E-9
lateral_res = lateral_res * 1E-6
axial_res = axial_res * 1E-6
pZ = pZ * 1E-6

# create the synthetic PSF
psf = ops.op("create.kernelDiffraction").input(psf_size,
                                                        numericalAperture,
                                                        wavelength,
                                                        riSample,
                                                        riImmersion,
                                                        lateral_res,
                                                        axial_res,
                                                        pZ,
                                                        FloatType()).apply()

# deconvolve image
result = ops.op("deconvolve.richardsonLucyTV").input(img_float, psf, FloatType(), ComplexFloatType(), iterations, False, False, Float(regularizationFactor)).apply()

# optionally show PSF
if show_psf:
    ui.show("PSF", psf)
