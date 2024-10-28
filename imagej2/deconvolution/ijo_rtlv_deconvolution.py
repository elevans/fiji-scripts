#@ OpService ops
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ Integer iterations(label="Iterations", value=15)
#@ Float numericalAperture(label="Numerical Aperture", style="format:0.00", min=0.00, value=1.45)
#@ Integer wavelength(label="Emission Wavelength (nm)", value=457)
#@ Float riImmersion(label="Refractive Index (immersion)", style="format:0.00", min=0.00, value=1.5)
#@ Float riSample(label="Refractive Index (sample)", style="format:0.00", min=0.00, value=1.4)
#@ Float lateral_res(label="Lateral resolution (μm/pixel)", style="format:0.0000", min=0.0000, value=0.065)
#@ Float axial_res(label="Axial resolution (μm/pixel)", style="format:0.0000", min=0.0000, value=0.1)
#@ Float pZ(label="Particle/sample Position (μm)", style="format:0.0000", min=0.0000, value=0)
#@ Float regularizationFactor(label="Regularization factor", style="format:0.00000", min=0.00000, value=0.002)
#@ Boolean (label = "Show PSF:", value = false) show_psf
#@output Img result

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.real import FloatType
from net.imglib2.type.numeric.complex import ComplexFloatType

# convert input image to float
img = ops.convert().float32(img)

# use image dimensions for PSF size
psf_size = FinalDimensions(img.dimensionsAsLongArray())

# convert the input parameters to meters (m)
wavelength = float(wavelength) * 1E-9
lateral_res = lateral_res * 1E-6
axial_res = axial_res * 1E-6
pZ = pZ * 1E-6

# create the synthetic PSF
psf = ops.create().kernelDiffraction(
    psf_size,
    numericalAperture,
    wavelength,
    riSample,
    riImmersion,
    lateral_res,
    axial_res,
    pZ,
    FloatType()
    )

# deconvolve image
result = ops.deconvolve().richardsonLucyTV(img, psf, iterations, regularizationFactor)

# optionally show the PSF
if show_psf:
    ui.show(psf)
