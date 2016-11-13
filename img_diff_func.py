from PIL import Image, ImageDraw
import ConfigParser
import os.path

config = ConfigParser.RawConfigParser()
config.read('config.ini')

SECTION_NAME = 'IMG_DIFF'
DISSIMILAR_PERCENT = config.getfloat(SECTION_NAME, 'dissimilar_percent')
SQUARE_WIDTH = config.getint(SECTION_NAME, 'square_width')
SQUARE_HEIGHT = config.getint(SECTION_NAME, 'square_height')
SQUARE_SIMILAR_RATIO = config.getfloat(SECTION_NAME, 'square_similar_ratio')
SQUARE_SIMILAR_COUNT = int(SQUARE_SIMILAR_RATIO * (SQUARE_WIDTH * SQUARE_WIDTH))
OFFSET = config.getint(SECTION_NAME, 'offset')
START_X = config.getint(SECTION_NAME, 'start_x')
START_Y = config.getint(SECTION_NAME, 'start_y')
IMG_HEIGHT = config.getint(SECTION_NAME, 'img_height')
IMG_WIDTH = config.getint(SECTION_NAME, 'img_width')

TMP_IMG_PATH = config.get('PATH', 'tmp_img_path')


def similar(tuple_a, tuple_b):
    for i in range(3):
        if float(tuple_a[i] - tuple_b[i]) / 255.0 > DISSIMILAR_PERCENT:
            return False
    return True


def square_similar(left, top, img):
    similar_count = 0
    for x in range(left, left + SQUARE_WIDTH):
        for y in range(top, top + SQUARE_HEIGHT):
            pixel_a = img.getpixel((x, y))
            pixel_b = img.getpixel((x + OFFSET, y))

            if similar(pixel_a, pixel_b):
                similar_count += 1

    return similar_count >= SQUARE_SIMILAR_COUNT


def get_diff_img(file_name):
    img = Image.open(os.path.join(TMP_IMG_PATH, file_name))
    img_copy = img.copy()
    img_dr = ImageDraw.Draw(img_copy)

    count = 0
    for x in range(START_X, START_X + IMG_WIDTH + 1, SQUARE_WIDTH):
        for y in range(START_Y, START_Y + IMG_HEIGHT + 1, SQUARE_HEIGHT):
            count += 1
            print count
            if not square_similar(x, y, img):
                img_dr.rectangle(((x, y), (x + SQUARE_WIDTH, y + SQUARE_HEIGHT)), outline='blue')
                img_dr.rectangle(((x + OFFSET, y), (x + SQUARE_WIDTH + OFFSET, y + SQUARE_HEIGHT)), outline='red')

                img_dr.rectangle(((x + 1, y + 1), (x + SQUARE_WIDTH - 1, y + SQUARE_HEIGHT - 1)), outline='blue')
                img_dr.rectangle(((x + OFFSET + 1, y + 1), (x + SQUARE_WIDTH + OFFSET - 1, y + SQUARE_HEIGHT - 1)),
                                 outline='red')
                print 'Get'
    img_copy.show()
    return img_copy


if __name__ == '__main__':
    TMP_IMG_NAME = config.get('PATH', 'TMP_IMG_NAME')
    RESULT_IMG_NAME = config.get('PATH', 'RESULT_IMG_NAME')
    NEED_TO_SAVE_RESULT_IMG = config.getboolean('PATH', 'NEED_TO_SAVE_RESULT_IMG')
    img_copy = get_diff_img('{}.png'.format(TMP_IMG_NAME))
    if NEED_TO_SAVE_RESULT_IMG:
        img_copy.save(os.path.join(TMP_IMG_PATH, '{}.jpg'.format(RESULT_IMG_NAME)))
