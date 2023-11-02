#@ ImgPlus img
#@ OpService ops
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

import ij.IJ
import net.imglib2.FinalDimensions
import net.imglib2.type.numeric.real.FloatType

// convert interger parameters to float
wavelength = wavelength.toFloat()

// convert input image to 32-bit
img_f = ops.convert().float32(img)

// get imglib2 dimensions from the input image
psf_dims = []
for (dim in img.dimensionsAsLongArray()) {
    psf_dims.add(dim)
}
psf_size = new FinalDimensions(psf_dims as long[])

// convert the input parameters to meteres (m)
wv = wavelength * 1E-9
lateral_res = lateral_res * 1E-6
axial_res = axial_res * 1E-6
pZ = pZ * 1E-6

// create the synthetic PSF
psf = ops.create().kernelDiffraction(
    psf_size,
    numericalAperture,
    wv,
    riSample,
    riImmersion,
    lateral_res,
    axial_res,
    pZ,
    new FloatType()
    )

// deconvolve image
result = ops.deconvolve().richardsonLucyTV(img_f, psf, iterations, regularizationFactor)