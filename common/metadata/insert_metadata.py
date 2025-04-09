#@ ImagePlus (label = "Input image:", autofill = false) imp
#@ String (label = "Metadata section name:", value = "Custom metadata") name
#@ Integer (label = "Number of key/value pairs to add:", value = 1) entries

from ij.gui import GenericDialog

from java.util import Properties

def insert_metadata(image, metadata_name, num_entries):
    """Insert the user defined metadata.

    This method creates a dialog box (defined by config)
    to collect the user defined metadata. Once collected
    the metadata is set on the input image.

    :param image:

        An ImagePlus.

    :param metadata_name:

        Name of the metadata section.

    :param num_entries:

        Number of metadata entries to insert.
    """
    # extract metadata
    imp_props = image.getProperties()
    # create metadata if none is found
    if imp_props is None:
        imp_props = Properties()
        imp_props.setProperty("Info", "")
    metadata = imp_props.getProperty("Info")
    # create insert metadata dialog
    gd_ins = GenericDialog("Insert Metadata")
    # add key/value fields
    gd_ins.addMessage("Enter metadata key/value pairs:")
    for i in range(num_entries):
        gd_ins.addStringField("Key:", "")
        gd_ins.addToSameRow()
        gd_ins.addStringField(" Value:", "")
    gd_ins.showDialog()
    # stop if canceled
    if gd_ins.wasCanceled():
        return
    # fetch user input
    insert = ""
    header = "--- {} ---\n".format(metadata_name)
    insert += header
    for i in range(num_entries):
        k = gd_ins.getNextString()
        v = gd_ins.getNextString()
        s = "{} = {}\n".format(k, v)
        insert += s
    # set image metadata
    image.setProperty("Info", insert + metadata)
    # mark image as changed
    image.changes = True

insert_metadata(imp, name, entries)
