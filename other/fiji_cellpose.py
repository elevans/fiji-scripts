#@ IOService io
#@ UIService ui
#@ Img img
#@ String (label="Cellpose Python path:") cp_py_path 
#@ String (label="Pretrained model:", choices={"cyto", "cyto2", "nuclei"}, style="listBox") model
#@ Float (label="Diameter (2D only):", style="format:0.00", value=0.00, stepSize=0.01) diameter
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
        cp_cmd = "cellpose --dir {} --pretrained_model {} --save_tif --do_3D".format(tmp_dir, model)
    else:
        cp_cmd = "cellpose --dir {} --pretrained_model {} --diameter {} --save_tif".format(tmp_dir, model, diameter)

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
