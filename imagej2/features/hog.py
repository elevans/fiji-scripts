#@ OpService ops
#@ ImgPlus img
#@ Integer num_orientations(label="Number of Orientations:", value=0)
#@ Integer span_of_neighborhood(label="Span of Neighborhood:", value=0)
#@output output

output = ops.run("hog.hog", img, num_orientations, span_of_neighborhood)