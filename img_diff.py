import img_diff_func
import screen_capture
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.ini')
SECTION_NAME = 'PATH'
TMP_IMG_PATH = config.get(SECTION_NAME, 'tmp_img_path')
TMP_IMG_NAME = config.get(SECTION_NAME, 'tmp_img_name')
RESULT_IMG_NAME = config.get(SECTION_NAME, 'result_img_name')
NEED_TO_SAVE_RESULT_IMG = config.getboolean(SECTION_NAME, 'need_to_save_result_img')

WAIT_TIME = config.getint('SCREEN_CAPTURE', 'wait_time')
if __name__ == '__main__':
    import time
    import os

    time.sleep(WAIT_TIME)
    screen_capture.screen_capture('{}.png'.format(TMP_IMG_NAME))
    img_copy = img_diff_func.get_diff_img('{}.png'.format(TMP_IMG_NAME))
    if NEED_TO_SAVE_RESULT_IMG:
        img_copy.save(os.path.join(TMP_IMG_PATH, '{}.jpg'.format(RESULT_IMG_NAME)))
