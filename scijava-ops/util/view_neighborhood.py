#@ OpEnvironment ops
#@ UIService ui
#@ String (visibility = MESSAGE, value = "<b>General settings</b>", required = false) general_msg
#@ Integer (label = "Dimensionality", min = 2, max = 3, value = 2) ndim
#@ String (visibility = MESSAGE, value = "<b>Radius based neighborhood shapes</b>", required = false) radius_msg
#@ Integer (label = "Radius", value = 0) radius
#@ Boolean (label = "Show diamond", value = false) show_diamond
#@ Boolean (label = "Show diamond tips", value = false) show_diamond_tips
#@ Boolean (label = "Show sphere", value = false) show_sphere
#@ String (visibility = MESSAGE, value = "<b>Span based neighborhood shapes</b>", required = false ) span_msg
#@ Integer (label = "Span", value = 0) span
#@ String (label = "Center", choices = {"keep", "skip"}, style = "listBox") center
#@ Boolean (label = "Show rectangle", value = false) show_rectangle

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.integer import UnsignedByteType
from net.imglib2.algorithm.neighborhood import (
        DiamondShape,
        DiamondTipsShape,
        RectangleShape,
        HyperSphereShape
        )

def create_img(axis_value, ndim):
    """Create an isometric 8-bit Img of variable dimension length.

    :params axis_value:

        The value to use for each dimension of the Img. All dimensions use
        the same value to create an isometric Img.

    :param ndim:
    
        The number of dimesions to create (e.g. 2 or 3 for 2D and 3D
        Img's respectively).

    :return:

        An 8-bit Img with the given dimension length.
    """
    dims = [4 * axis_value + 1] * ndim
    
    return ops.op("create.img").input(
            FinalDimensions(dims),
            UnsignedByteType()
            ).apply()


def fill_img(image, val, shape, ndim):
    """Fill the image with the given shape.

    :param image:

        Input Img.

    :param val:

        Value for axis bias (i.e. radius or span value).

    :param shape:

        Neighborhood shape.

    :param ndim:

        The number of dimensions (2 or 3).
    """
    ra = shape.neighborhoodsRandomAccessible(image).randomAccess()
    # set position to the center of the image
    for i in range(ndim):
        ra.setPosition(2 * val, i)
   
    # get cursor and fill the image
    c = ra.get().cursor()
    while c.hasNext():
        c.fwd()
        c.get().set(255)


def show_neighborhood_img(val, ndim, shape, title):
    """Show neighborhood images.

    :param val:

        Value for axis bias (i.e. radius or span value).

    :param ndim:

        The number of dimensions (2 or 3).

    :param shape:

        Beighborhood shape.

    :param title:

        Title for the image.
    """
    img = create_img(val, ndim)
    fill_img(img, val, shape, ndim)
    ui.show(title, img)

# radius shapes
diamond_shape = DiamondShape(radius)
diamond_tips_shape = DiamondTipsShape(radius)
sphere_shape = HyperSphereShape(radius)

# span shapes
skip_center = True if center == "skip" else False
rectangle_shape = RectangleShape(span, skip_center)

if show_diamond:
    show_neighborhood_img(
            radius,
            ndim, diamond_shape,
            "Diamond radius {}".format(radius)
            )
if show_diamond_tips:
    show_neighborhood_img(
            radius,
            ndim,
            diamond_tips_shape,
            "Diamond tips radius {}".format(radius)
            )
if show_sphere:
    show_neighborhood_img(
            radius,
            ndim,
            sphere_shape,
            "Sphere radius {}".format(radius)
            )
if show_rectangle:
    show_neighborhood_img(
            span,
            ndim,
            rectangle_shape,
            "Rectangle span {}".format(span)
            )
