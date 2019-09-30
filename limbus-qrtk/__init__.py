from pylibdmtx.pylibdmtx import decode
from PIL import Image
import numpy as np


image = Image.open("/home/keo7/Downloads/IMG_20181122_144935.jpg").convert('L')


results = decode(np.array(image))


def determine_grid(results: list) -> dict:

    def _gridify(coords, spacing):
        return np.round(coords / spacing) * spacing

    left_all = [abs(result.rect.left) for result in results]
    top_all = [abs(result.rect.top) for result in results]

    av_width = np.mean([abs(result.rect.width) for result in results])

    g_l = _gridify(left_all, av_width*1.1)

    g_l_d = {v : k for (k,v) in enumerate(set(g_l))}

    g_t = _gridify(top_all, av_width*1.1)
    g_t_d = {v : k for (k,v) in enumerate(set(g_t))}


    for index, result in enumerate(results):
        column = g_l_d[g_l[index]]
        row = g_t_d[g_t[index]]


        print("%s on row %i, column %i" % (result.data, row+1, column+1))

    #print(g_l, g_t)


determine_grid(results)


