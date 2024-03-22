#@ OpService ops
#@ String (label="Transformation:", choices={"Translation", "Affine"}, style="listBox") transformation
#@ Integer (label="Maximum pyramid levels:", style="listBox", min=0, max=4, stepSize=1) pyramid_levels
#@ Integer (label="Iterations", min=0, value=200) iterations
#@ Float (label="Template update coefficient:", style="format:0.00", value=0.90) update_coeff
#@ Float (label="Error tolerance:", style="format:0.0000000", value=0.0000001) error_tol
#@ Boolean (label="Log transform coefficients", value=False) log_transform
#@ ImagePlus imp
#@output ImagePlus result

from ij import IJ, ImagePlus, WindowManager
from ij.plugin import ChannelSplitter, RGBStackMerge


def image_stabilization(image):
    """
    Run the Image Stabilization plugin on the input image.

    :param image: Input ImagePlus
    :return: Stabilized ImagePlus image
    """
    cmd_str = "transformation={} maximum_pyramid_levels={} template_update_coefficient={} maximum_iterations={} error_tolerance={}".format(str(transformation),
                                                                                                                                           str(pyramid_levels),
                                                                                                                                           str(update_coeff),
                                                                                                                                           str(iterations),
                                                                                                                                           str(error_tol))
    if log_transform:
        cmd_str = cmd_str + " log_transformation_coefficients"
    IJ.run(image, "Image Stabilizer", cmd_str)

    return image


def run(image):
    """
    Run multi-channel image stabilization.

    :param image: Input multi-channel ImagePlus
    :param return: Image stabilized multi-channel ImagePlus
    """
    # split channels and show the images
    chs = ChannelSplitter.split(image)
    for ch in chs:
        ch.show()

    # close the input image
    input_image_id = WindowManager.getIDList()[0]
    WindowManager.getImage(input_image_id).close()

    # apply image stabilization to open images (skip input image)
    open_chs = WindowManager.getIDList()
    chs_stab = []
    for i in range(len(open_chs)):
        tmp_imp = WindowManager.getImage(open_chs[i])
        image_stabilization(tmp_imp)
        chs_stab.append(tmp_imp)

    # stack images together (do not keep source images)
    imp_stab = RGBStackMerge.mergeChannels(chs_stab, False)

    # close all images
    IJ.run("Close All", "")

    return imp_stab

# run the multi-channel image stabilization
result = run(imp)