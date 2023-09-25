#@ OpService ops
#@ ImgPlus img
#@ Integer grey_levels(label="Number of Grey levels:", value=0)
#@ Integer distance(label="Distance:", value=0)
#@ String (choices={"antidiagonal", "diagonal", "horizontal", "vertical"}, style="listBox") orientation

from net.imagej.ops.image.cooccurrenceMatrix import MatrixOrientation2D

matrix_orientation = {
    "antidiagonal": MatrixOrientation2D.ANTIDIAGONAL,
    "diagonal": MatrixOrientation2D.DIAGONAL,
    "horizontal": MatrixOrientation2D.HORIZONTAL,
    "vertical": MatrixOrientation2D.VERTICAL
}

res = ops.haralick().asm(img, grey_levels, distance, matrix_orientation.get(orientation))
print(res)