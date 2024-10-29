#@ OpEnvironment ops
#@ ImgPlus (label = "Input image:", autofill = false) img
#@ Float (label = "Isolevel", style = "format:0.00", min = 1.0, value = 1.0) isolevel

from net.imglib2.type.logic import BitType

from org.scijava.vecmath import Point3f

from customnode import CustomTriangleMesh
from ij3d import Image3DUniverse

def apply_isolevel(image, isolevel):
    """Apply the desired isolevel on the input image.

    Apply a desired isolevel (i.e. isosurface) value on the input image,
    returning a BitType image that can be used with the marching cubes Op.

    :param image:

        Input ImgPlus.

    :param isolevel:

        Input isolevel value (float).

    :return:

        Output ImgPlus of BitType at desired isolevel.
    """
    if isolevel > 1.0:
        isolevel -= 1
    val = image.firstElement().copy()
    val.setReal(isolevel)
    out = ops.op("create.img").input(image, BitType()).apply()
    ops.op("threshold.apply").input(image, val).output(out).compute()
    
    return out


def view_mesh(image):
    """Create an ImgLib2 mesh and view in the 3D viewer.

    Convert the input ImgPlus BitType image into an ImgLib2 mesh
    and display it with the 3D viewer.

    :param image:

        Input ImgPlus of BitType.
    """
    mesh = ops.op("geom.marchingCubes").input(image).apply()
    points = []
    for t in mesh.triangles():
        points.append(Point3f(t.v0xf(), t.v0yf(), t.v0zf()))
        points.append(Point3f(t.v1xf(), t.v1yf(), t.v1zf()))
        points.append(Point3f(t.v2xf(), t.v2yf(), t.v2zf()))

    ctm = CustomTriangleMesh(points)
    univ = Image3DUniverse()
    univ.addCustomMesh(ctm, "mesh")
    univ.show()

view_mesh(apply_isolevel(img, isolevel))
