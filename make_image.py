import PIL
import Image, ImageDraw
import ImageFont
from matplotlib.pyplot import imshow
from IPython.core.display import display
from PIL import ImageQt

from util.memo import json_memoized

imagesize = (350, 900)


BU = u'\u6b66'
SHI = u'\u58eb'
DO = u'\u9053'

# display_pil.py
# source: http://mail.scipy.org/pipermail/ipython-user/2012-March/009706.html
# by 'MinRK'
import Image
from IPython.core import display
from io import BytesIO

def display_pil_image(im):
    """displayhook function for PIL Images, rendered as PNG"""
    b = BytesIO()
    im.save(b, format='png')
    data = b.getvalue()

    ip_img = display.Image(data=data, format='png', embed=True)
    return ip_img._repr_png_()

# register display func with PNG formatter:
png_formatter = get_ipython().display_formatter.formatters['image/png']
png_formatter.for_type(Image.Image, display_pil_image)

BIG_KANJI_SIZE = 294

def _font(name):
    return ImageFont.truetype(name, BIG_KANJI_SIZE, encoding='unic')

# don't work:
# font = ImageFont.truetype("simsunb.ttf", font_size, encoding='unic')
# font = ImageFont.truetype("simpbdo.ttf", font_size, encoding='unic')
# font = ImageFont.truetype("simpfxo.ttf", font_size, encoding='unic')
# font = ImageFont.truetype("simpo.ttf", font_size, encoding='unic')
BIG_KANJI_FONTS = dict(
    (shortname, _font(fontfname)) for shortname, fontfname in [
        ('serif', 'simsun.ttc'),
        ('curvy', "simkai.ttf"),
        ('gangly', "simfang.ttf"),
        ('blocky', "simhei.ttf")
    ]
)

def mk_big_char_im():
    chars = [BU, SHI, DO]

    sizes = dict((c, char_sizes(c)[BIG_KANJI_SIZE]) for c in chars)

    offsets, bounds = zip(*[sizes[c] for c in chars])
    sum_height = sum(h for _, h in bounds)
    max_width = max(w for w, _ in bounds)

    im_size = im_width, im_height = (300, 850)
    
    extra_height = im_height - sum_height

    assert max_width < im_width
    assert extra_height > 0
    
    im = Image.new('L', im_size)
    
    draw = ImageDraw.Draw(im)
    
    center_x = float(im_width) / 2
    stride = float(im_height) / len(chars)

    font = BIG_KANJI_FONTS['serif']

    for i, c in enumerate(chars):
        center_y = (i + .5) * stride

        b_w, b_h = bounds[i]

        ul_x = center_x - b_w/2.
        ul_y = center_y - b_h/2.

        off_x, off_y = offsets[i]

        ul_x -= off_x
        ul_y -= off_y

        draw.text((ul_x, ul_y), c, font=font, fill=255)

    return im

def mk_rand_bin_img_from_mask(mask_im):
    bin_font = ImageFont.truetype('consola.ttf', 9)
    bin_color = (0xc8, 0xff, 0xc8, 0xff)

    im = Image.new('RGBA', mask_im.size)
    draw = ImageDraw.Draw(im)

    width, height = im.size

    one = bin_font.getsize('1')
    zero = bin_font.getsize('0')
    
    start_x = 0
    start_y = 0

    import random

    for start_y in xrange(start_y, height, zero[1]):
        randstr = ''.join(random.choice(['1', '0']) for _ in xrange(100))
        draw.text((start_x, start_y), randstr, font=bin_font, fill=bin_color)

    display.display(im)

    import ImageMath

    bands = im.split()

    bands = [
        ImageMath.eval(
            'convert(min(mask, band), "L")',
            mask = mask_im,
            band = band
        )
        for band in bands
    ]

    new_im = Image.merge('RGBA', bands)

    with file('foo.jpg', 'wb') as f:
        new_im.save(f, format='jpeg')

    display.display(new_im)


def main():
    im = mk_big_char_im()
    
    display.display(im)

    mk_rand_bin_img_from_mask(im)

    return im

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
