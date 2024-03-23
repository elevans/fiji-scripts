#@ OpService ops
#@ String (label="Transformation:", choices={"Translation", "Affine"}, style="listBox") transformation
#@ Integer (label="Maximum pyramid levels:", style="listBox", min=0, max=4, stepSize=1) pyramid_levels
#@ Integer (label="Iterations", min=0, value=200) iterations
#@ Float (label="Template update coefficient:", style="format:0.00", value=0.90) update_coeff
#@ Float (label="Error tolerance:", style="format:0.0000000", value=0.0000001) error_tol
#@ Boolean (label="Log transform coefficients", value=False) log_transform

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


def run():
    """
    Run multi-channel image stabilization.

    :param image: Input multi-channel ImagePlus
    :param return: Image stabilized multi-channel ImagePlus
    """
    # initial images
    init_image_ids = WindowManager.getIDList()
    stablized_image_ids = []

    for id in init_image_ids:
        # get an open image
        tmp_init_imp = WindowManager.getImage(id)

        # split channels and show the images
        chs = ChannelSplitter.split(tmp_init_imp)
        for ch in chs:
            ch.show()

        # find the new split channel image IDs
        tmp_working_ids = []
        tmp_open_image_ids = WindowManager.getIDList()
        for v in tmp_open_image_ids:
            if v not in init_image_ids and v not in stablized_image_ids:
                tmp_working_ids.append(v)

        chs_stab = []
        for i in range(len(tmp_working_ids)):
            tmp_imp = WindowManager.getImage(tmp_working_ids[i])
            image_stabilization(tmp_imp)
            chs_stab.append(tmp_imp)

        # stack images together (do not keep source images)
        imp_stab = RGBStackMerge.mergeChannels(chs_stab, False)
        imp_stab.show()

        # hide split channels
        for v in tmp_working_ids:
            WindowManager.getImage(v).hide()

        # store new stabalized image id
        tmp_open_image_ids = WindowManager.getIDList()
        for v in tmp_open_image_ids:
            if v not in init_image_ids and v not in stablized_image_ids:
                stablized_image_ids.append(v)

    # hide input images
    for v in init_image_ids:
        WindowManager.getImage(v).hide()

# run the multi-channel image stabilization
run()