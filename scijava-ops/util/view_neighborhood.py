#@ OpEnvironment ops
#@ Integer (label = "Radius", value = 0) radius
#@ String (label = "Neighborhood shape", choices = {"Diamond", "Hypersphere"}, style = "listBox") shape_type
#@ Integer (label = "Dimensionality", min = 2, max = 3, value = 2) dims_length
#@output Img output

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.integer import UnsignedByteType
from net.imglib2.algorithm.neighborhood import (
        DiamondShape,
        GeneralRectangleShape,
        HyperSphereShape
        )

def create_img(dims_length):
    """Create an isometric 8-bit Img of variable dimension length.

    :param dims_length:
    
        The number of dimesions to create (e.g. 2 or 3 for 2D and 3D
        Img's respectively).

    :return:

        An 8-bit Img with the given dimension length.
    """
    dims = [4 * radius + 1] * dims_length
    
    return ops.op("create.img").input(
            FinalDimensions(dims),
            UnsignedByteType()
            ).apply()


def fill_img(image, shape, dims_length):
    """
    """
    ra = shape.neighborhoodsRandomAccessible(image).randomAccess()
    # set position to the center of the image
    for i in range(dims_length):
        ra.setPosition(2 * radius, i)
   
    # get cursor and fill the image
    c = ra.get().cursor()
    while c.hasNext():
        c.fwd()
        c.get().set(255)

# get neighborhood shape
if shape_type == "Diamond":
    shape = DiamondShape(radius)
else:
    shape = HyperSphereShape(radius)

output = create_img(dims_length)
output = fill_img(output, shape, dims_length)
