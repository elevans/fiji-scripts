#@ OpService ops
#@ UIService ui
#@ ImgPlus img
#@ Double(value = 1) isolevel

from java.util import ArrayList, List

from net.imagej.mesh import Mesh, Triangle
from net.imglib2 import RandomAccessibleInterval
from net.imglib2.type import BooleanType
from net.imglib2.util import Util
from org.scijava.vecmath import Point3f
from customnode import CustomTriangleMesh
from ij3d import Image3DUniverse

# convert mask to bit/boolean type
mask = ops.convert().bit(img)

# create the mesh
mesh = ops.geom().marchingCubes(mask, isolevel)

# calculate mesh volume
mesh_vol = ops.geom().size(mesh).getRealDouble()