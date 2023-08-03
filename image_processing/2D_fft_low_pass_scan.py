#@ OpService ops
#@ UIService ui
#@ ImgPlus img
#@ Integer start_radius(label="Start radius:", value=0)
#@ Integer end_radius(label="End radius:", value=0)
#@output ImgPlus recon

from net.imglib2.util import Util
from net.imglib2.view import Views

def fft_high_pass_filter(fft_array, radius):
    # get cursor
    fft_cursor = fft_array.cursor()

    # note dimension order is X, Y or col, row
    cursor_pos = [None, None]
    origin_a = [0, 0]
    origin_b = [0, fft_array.dimension(1)]
    origin_c = [fft_array.dimension(0), 0]
    origin_d = [fft_array.dimension(0), fft_array.dimension(1)]

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
        
        # remove high frequences
        if (dist_a > radius) and \
            (dist_b > radius) and \
            (dist_c > radius) and \
            (dist_d > radius):
            fft_cursor.get().setZero()


def fft_scan(img, start_radius, end_radius):
    results = []
    fft_array = ops.filter().fft(img)
    for radius in range(start_radius, end_radius):
        fft_array_dup = fft_array.copy()
        fft_high_pass_filter(fft_array_dup, radius)
        recon = ops.create().img([img.dimension(0), img.dimension(1)])
        ops.filter().ifft(recon, fft_array_dup)
        results.append(recon)

    return Views.stack(results)

# display result
ui.show(fft_scan(img, start_radius, end_radius))