#@ OpEnvironment ops
#@ ImgPlus img
#@ Integer iterations(label="Iterations", value=30)
#@ Float numericalAperture(label="Numerical Aperture", style="format:0.00", min=0.00, value=1.45)
#@ Integer wavelength(label="Emission Wavelength (nm)", value=550)
#@ Float riImmersion(label="Refractive Index (immersion)", style="format:0.00", min=0.00, value=1.5)
#@ Float riSample(label="Refractive Index (sample)", style="format:0.00", min=0.00, value=1.4)
#@ Float lateral_res(label="Lateral resolution (μm/pixel)", style="format:0.0000", min=0.0000, value=0.065)
#@ Float axial_res(label="Axial resolution (μm/pixel)", style="format:0.0000", min=0.0000, value=0.1)
#@ Float pZ(label="Particle/sample Position (μm)", style="format:0.0000", min=0.0000, value=0)
#@ Float regularizationFactor(label="Regularization factor", style="format:0.00000", min=0.00000, value=0.002)
#@output ImgPlus psf
#@output ImgPlus result

from java.lang import System

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.real import FloatType
from net.imglib2.type.numeric.complex import ComplexFloatType

# convert input image to float
img_float = ops.op("create.img").arity2().input(img, FloatType()).apply()
ops.op("convert.float32").arity1().input(img).output(img_float).compute()

# use image dimensions for PSF size
psf_size = FinalDimensions(img.dimensionsAsLongArray())

# convert the input parameters to meters (m)
wavelength = float(wavelength) * 1E-9
lateral_res = lateral_res * 1E-6
axial_res = axial_res * 1E-6
pZ = pZ * 1E-6

# create the synthetic PSF
psf = ops.op("create.kernelDiffraction").arity9().input(psf_size,
                                                        numericalAperture,
                                                        wavelength,
                                                        riSample,
                                                        riImmersion,
                                                        lateral_res,
                                                        axial_res,
                                                        pZ,
                                                        FloatType()).apply()

# deconvole image
i1 = System.currentTimeMillis()
result = ops.op("deconvolve.richardsonLucyTV").arity8().input(img_float, psf, FloatType(), ComplexFloatType(), iterations, False, False, regularizationFactor).apply()
i2 = System.currentTimeMillis()
print("processing time: {}".format(i2 - i1))