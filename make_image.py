import PIL
import Image, ImageDraw
import ImageFont
from matplotlib.pyplot import imshow
from IPython.core.display import display_jpeg
from PIL import ImageQt

from util.memo import json_memoized

imagesize = (350, 900)


BU = u'\u6b66'
SHI = u'\u58eb'
DO = u'\u9053'

def show(im):
    jpeg_str = im.tostring('jpeg', im.mode)
    display_jpeg(jpeg_str, raw=True)

def main():
    chars = [BU, SHI, DO]
    font_size = 294
    sizes = dict((c, char_sizes(c)[font_size]) for c in chars)


    offsets, bounds = zip(*[sizes[c] for c in chars])
    sum_height = sum(h for _, h in bounds)
    max_width = max(w for w, _ in bounds)

    im_size = im_width, im_height = (300, 850)
    
    extra_height = im_height - sum_height

    assert max_width < im_width
    assert extra_height > 0
    
    im = Image.new('RGBA', im_size)
    
    # don't work:
    # font = ImageFont.truetype("simsunb.ttf", font_size, encoding='unic')
    # font = ImageFont.truetype("simpbdo.ttf", font_size, encoding='unic')
    # font = ImageFont.truetype("simpfxo.ttf", font_size, encoding='unic')
    # font = ImageFont.truetype("simpo.ttf", font_size, encoding='unic')

    # serif:
    font = ImageFont.truetype("simsun.ttc", font_size, encoding='unic')
    # artistic/curvy:
    # font = ImageFont.truetype("simkai.ttf", font_size, encoding='unic')
    # kinda gangly:
    # font = ImageFont.truetype("simfang.ttf", font_size, encoding='unic')
    # big & blocky:
    # font = ImageFont.truetype("simhei.ttf", font_size, encoding='unic')


    draw = ImageDraw.Draw(im)
    
    center_x = float(im_width) / 2
    stride = float(im_height) / len(chars)

    for i, c in enumerate(chars):
        center_y = (i + .5) * stride

        b_w, b_h = bounds[i]

        ul_x = center_x - b_w/2.
        ul_y = center_y - b_h/2.

        off_x, off_y = offsets[i]

        ul_x -= off_x
        ul_y -= off_y

        draw.text((ul_x, ul_y), c, font=font, fill=(255,255,255,255))

    show(im)

def box_around(x, y, w, h=None):
    if h is None:
        h = w
    
    return (x - w/2., y - h/2., x + w/2., y + h/2.)

#should use im.getbbox and font.getmask for char sizes... TODO
@json_memoized('charsizes.json')
def char_sizes(ch):
    res = {}
    for sz in xrange(0, 300, 6):
        res[sz] = char_size(ch, sz)
    return res

def char_size(ch, size):
    # here, I tried both arial.ttf and times.ttf and there wasn't
    # the characters that I needed, got the name of this font from wordpad
    # when I tried to paste the characters
    font = ImageFont.truetype("simsun.ttc", size, encoding='unic')
    charsize = font.getsize(ch)

    img_mode = 'L'
    im = Image.new(img_mode, charsize)
    draw = ImageDraw.Draw(im)

    draw.text((0, 0), ch, font=font, fill=255)

    min_i, min_j = im.size
    max_i, max_j = (0, 0)

    for i in xrange(im.size[0]):
        for j in xrange(im.size[1]):
            pix = im.getpixel((i, j))
            if pix != 0:
                min_i = min(min_i, i)
                min_j = min(min_j, j)
                max_i = max(max_i, i)
                max_j = max(max_j, j)
    
    offset = (min_i, min_j)
    width = (max_i - min_i, max_j - min_j)
    print offset, width

    # jpeg_str = im.tostring('jpeg', img_mode)
    # display_jpeg(jpeg_str, raw=True)

    return offset, width

# for i, c in enumerate(chars):
#     img_w, img_h    = imagesize
#     img_center_w    = float(img_w)/2
#     ch_w, ch_h      = charsize
#     ch_center_h     = (i+.5)*float(img_h)/len(chars)
#     ch_ul_x = img_center_w - float(ch_w)/2
#     ch_ul_y = ch_center_h - float(ch_h)/2
#     print ch_ul_x, ch_ul_y, imagesize, charsize
#     draw.text((ch_ul_x, ch_ul_y), c, font=font)
#     def _box(where, color):
#         box = box_around(where[0], where[1], 20)
#         print box
#         draw.rectangle(box, color)
#     _box((img_center_w, ch_center_h), 'red')
#     _box((ch_ul_x, ch_ul_y), 'yellow')



if __name__ == '__main__':
    im = main()
