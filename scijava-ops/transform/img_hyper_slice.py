#@ OpEnvironment ops
#@ Img (label="Input image:", autofill=false) img
#@ Integer (label="Dimension:", min=1, value=1) dim
#@ Integer (label="Position:", min=1, value=1) pos
#@output Img output

output = ops.op("transform.hyperSliceView").input(img, dim - 1, pos -  1).apply()
