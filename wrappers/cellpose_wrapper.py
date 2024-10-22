#@ IOService io
#@ Img (label = "Input image:", autofill = false) img
#@ String (label="Cellpose Python path:") cp_py_path 
#@ String (label="Pretrained model:", choices={"cyto", "cyto2", "cyto2_cp3", "cyto3", "nuclei", "livecell_cp3", "deepbacs_cp3", "tissuenet_cp3", "bact_fluor_cp3", "bact_phase_cp3", "neurips_cellpose_default", "neurips_cellpose_transformer", "neurips_grayscale_cyto2", "transformer_cp3", "yeast_BF_cp3", "yeast_PhC_cp3"}, style="listBox") model
#@ Float (label="Diameter (2D only):", style="format:0.00", value=0.00, stepSize=0.01) diameter
#@ Float (label="Flow threshold:", style="format:0.0", value=0.4, stepSize=0.1) flow_thres
#@ Float (label="Cellprob threshold:", style="format:0.0", value=0.0, stepSize=0.1) cellprob_thres
#@ Boolean (label="Enable 3D segmentation:", value=False) use_3d
#@output result

from java.nio.file import Files

import os
import subprocess
import shutil

def run_cellpose(image):
    # create a temp directory
    tmp_dir = Files.createTempDirectory("fiji_tmp")

    # save input image
    tmp_save_path = tmp_dir.toString() + "/cellpose_input.tif"
    io.save(image, tmp_save_path)

    # build cellpose command
    if use_3d:
        cp_cmd = "cellpose --dir {} --pretrained_model {} --flow_threshold {} --cellprob_threshold {} --save_tif --do_3D --no_npy".format(tmp_dir, model, flow_thres, cellprob_thres)
    else:
        cp_cmd = "cellpose --dir {} --pretrained_model {} --flow_threshold {} --cellprob_threshold {} --diameter {} --save_tif --no_npy".format(tmp_dir, model, flow_thres, cellprob_thres, diameter)

    # run cellpose
    full_cmd = "{} -m {}".format(cp_py_path, cp_cmd)
    process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()

    # harvest cellpose results
    cp_masks_path = os.path.join(tmp_dir.toString(), "cellpose_input_cp_masks.tif")
    cp_masks = io.open(cp_masks_path)

    # remove temp directory
    shutil.rmtree(tmp_dir.toString())

    return cp_masks

result = run_cellpose(img)
