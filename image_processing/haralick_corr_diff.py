#@ OpService ops
#@ ImgPlus img
#@ Integer grey_levels(label="Number of Grey levels:", value=0)
#@ Integer dist(label="Distance:", value=0)
#@ String (choices={"antidiagonal", "diagonal", "horizontal", "vertical"}, style="listBox") orientation

from net.imagej.ops.image.cooccurrenceMatrix import MatrixOrientation2D

matrix_orientation = {
    "antidiagonal": MatrixOrientation2D.ANTIDIAGONAL,
    "diagonal": MatrixOrientation2D.DIAGONAL,
    "horizontal": MatrixOrientation2D.HORIZONTAL,
    "vertical": MatrixOrientation2D.VERTICAL
}


def run_asm_corr_diff(img):
    # compute haralick correlation and difference (variance)
    corr = ops.haralick().correlation(img, grey_levels, dist, matrix_orientation.get(orientation))
    diff = ops.haralick().differenceVariance(img, grey_levels, dist, matrix_orientation.get(orientation))
    
    return [corr, diff]

print(run_asm_corr_diff(img))
