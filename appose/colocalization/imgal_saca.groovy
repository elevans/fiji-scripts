#@ Img (label = "Input image:", autofill = false) image

#@output Img z_score

import org.apposed.appose.Appose

saca_script = """
def share_as_ndarray(img):
    ""\"Copies a NumPy array into a same-sized newly allocated block of shared memory""\"
    from appose import NDArray
    shared = NDArray(str(img.dtype), img.shape)
    shared.ndarray()[:] = img
    return shared

import imgal.colocalization as coloc
import imgal.threshold as ths
import numpy as np
arr = image.ndarray()
ch_a = arr[0, :, :]
ch_b = arr[1, :, :]
z_score = coloc.saca_2d(ch_a, ch_b, ths.otsu_value(ch_a), ths.otsu_value(ch_b))
share_as_ndarray(z_score)
"""

println("== BUILDING ENVIRONMENT ==")
env = Appose.uv().include("pyimgal").name("pyimgal").logDebug().build()
println("Environment build complete: ${env.base()}")

// Conversion functions: ImgLib2 Img <-> Appose NDArray
imgToAppose = { img ->
	ndArray = net.imglib2.appose.ShmImg.copyOf(image).ndArray()
	println("Copied image into shared memory: ${ndArray.shape()} DType{${ndArray.dType()}}")
	return ndArray
}
apposeToImg = { ndarray ->
	net.imglib2.appose.NDArrays.asArrayImg(ndarray)
}
copyImg = { img ->
	// Note: We use PlanarImg because the original ImageJ likes them best.
	copy = new net.imglib2.img.planar.PlanarImgFactory(img.getType()).create(img.dimensionsAsLongArray())
	net.imglib2.util.ImgUtil.copy(img, copy)
	return copy
}

// Run the script as an Appose task
println("== STARTING PYTHON SERVICE ==")
try (python = env.python()) {
	inputs = [
		"image": imgToAppose(image),
	]
	task = python.task(saca_script, inputs)
		.listen { if (it.message) println("[IMGAL] ${it.message}") }
		.waitFor()

	println("TASK FINISHED: ${task.status}")
	if (task.error) println(task.error)
	z_score = copyImg(apposeToImg(task.result()))
	// Without the copyImg, imglib2-ij fails to wrap such ArrayImgs to ImagePlus,
	// due to ImageProcessorUtils expecting a backing Java primitive array type.
	//
	// pixels = labels.update( null ).getCurrentStorageArray()
	// ^ Pixels is a DirectShortBufferU here -- makes sense; it's shared memory
	//
	// But then... how the heck does the unseg_fiji plugin work?!
	// So for the moment, we just copy it into a non-shm Img. :'-(	
}
finally {
	println("== TERMINATING PYTHON SERVICE ==")
}
