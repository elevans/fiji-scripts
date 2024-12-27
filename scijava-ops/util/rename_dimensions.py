#@ OpEnvironment ops
#@ UIService ui
#@ Dataset (label = "Input image:", autofill = false) ds
#@ String (label = "Dimension order:", value = "x,y,c,t,z") dim_order

from net.imagej.axis import Axes, DefaultLinearAxis

from java.lang import Double

def convert_dim_name(key):
    """Convert the dimension name into ImgLib2 format.
    """
    dims = {
            "col": "X",
            "x": "X",
            "row": "Y",
            "y": "Y",
            "ch": "Channel",
            "c": "Channel",
            "pln": "Z",
            "z": "Z",
            "t": "Time",
            }
    if key in dims:
        return dims[key]
    else:
        return key


def rename_dataset_dims(dataset, dim_order):
    """Rename the dimensions of a Dataset.

    Rename the dimensions of a net.imagej.DefaultDataset. This only
    renames the dimensions of a Dataset, preserving the array shape
    and axis coordinates.

    :param dataset:

        An input net.imagej.Dataset

    :param dim_order:

        A list/tuple of strings with the new dimension order.

    :return:

        The dataset with renamed dimensions.
    """
    # get the old dataset axes
    ndim = dataset.numDimensions()
    old_axes = tuple(dataset.axis(d) for d in range(ndim))
    new_axes = []
    for i in range(ndim):
        # get old axis scale and origin
        old_scale = old_axes[i].scale()
        old_origin = old_axes[i].origin()
        # create a new axis with old scale and origin
        axis_type = Axes.get(convert_dim_name(dim_order[i])) 
        new_axis = DefaultLinearAxis(
                axis_type,
                Double(old_scale),
                Double(old_origin)
                )
        new_axes.append(new_axis)
    dataset.setAxes(new_axes)

    return dataset

ui.show("result", rename_dataset_dims(ds, dim_order.split(",")))
