#@ ImgPlus img
#@ OpService ops
#@ UIService ui 
#@ Integer iterations(label="Iterations", value=30)
#@ Float numericalAperture(label="Numerical Aperture", value=1.4)
#@ Integer wavelength(label="Wavelength (nm)", value=550)
#@ Float riImmersion(label="Refractive Index (immersion)", value=1.5)
#@ Float riSample(label="Refractive Index (sample)", value=1.4)
#@ Float xySpacing(label="XY Spacing (nm)", value=62.9)
#@ Float zSpacing(label="Z Spacing (nm)", value=160)
#@ Integer depth(value=0)
#@output ImgPlus psf
#@output ImgPlus result

import ij.IJ
import net.imglib2.FinalDimensions
import net.imglib2.type.numeric.real.FloatType

//convert interger parameters to float
wavelength = wavelength.toFloat()

// convert input image to 32-bit
img_f = ops.convert().float32(img)

// generate synthetic psf based on input shape
psf_dims = []
for (dim in img.dimensionsAsLongArray()) {
    psf_dims.add(dim)
}
psf_size = new FinalDimensions(psf_dims as long[])
wv = wavelength * 1E-9
lateral_res = xySpacing * 1E-9
axial_res = zSpacing * 1E-9
psf = ops.create().kernelDiffraction(
    psf_size,
    numericalAperture,
    wv,
    riSample,
    riImmersion,
    lateral_res,
    axial_res,
    depth, 
    new FloatType()
    )

// deconvolve image
result = ops.deconvolve().richardsonLucyTV(img_f, psf, iterations, 0.002)