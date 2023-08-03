#@ ImgPlus img
#@ OpService ops
#@ UIService ui
#@ Integer radius(label="Radius:", value=0)
#@ Boolean show(label="Show FFT arrays", value=False)
#@output ImgPlus recon

from net.imglib2.img.display.imagej import ImageJFunctions
from net.imglib2.util import Util

# run FFT on the input image
fft_img = ops.filter().fft(img)

if show:
    # display the FFT array in a power spectrum
    ImageJFunctions.show(fft_img).setTitle("FFT power spectrum")

# get a cursor on the FFT array
fft_cursor = fft_img.cursor()

# note dimension order is X, Y or col, row
cursor_pos = [None, None]
origin_a = [0, 0]
origin_b = [0, fft_img.dimension(1)]
origin_c = [fft_img.dimension(0), 0]
origin_d = [fft_img.dimension(0), fft_img.dimension(1)]

# loop through the FFT array
while fft_cursor.hasNext():

    # advance cursor and localize
    fft_cursor.fwd()
    cursor_pos[0] = fft_cursor.getLongPosition(0)
    cursor_pos[1] = fft_cursor.getLongPosition(1)

    # calculate distance from origins
    dist_a = Util.distance(origin_a, cursor_pos)
    dist_b = Util.distance(origin_b, cursor_pos)
    dist_c = Util.distance(origin_c, cursor_pos)
    dist_d = Util.distance(origin_d, cursor_pos)
    
    # Remove high frequences
    if (dist_a > radius) and \
        (dist_b > radius) and \
        (dist_c > radius) and \
        (dist_d > radius):
        fft_cursor.get().setZero()

if show:
    # display the FFT array after remove low frequences
    ImageJFunctions.show(fft_img).setTitle("FFT post filter")

# reconstruct filtered image from FFT array and show
recon = ops.create().img([img.dimension(0), img.dimension(1)])
ops.filter().ifft(recon, fft_img)