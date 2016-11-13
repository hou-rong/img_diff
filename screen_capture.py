import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.ini')

SECTION_NAME = 'PATH'
TMP_IMG_PATH = config.get(SECTION_NAME, 'tmp_img_path')


def get_wid_list():
    import Quartz
    wid_list = []
    wl = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
    wl = sorted(wl, key=lambda k: k.valueForKey_('kCGWindowOwnerPID'))

    for v in wl:
        if 'Pictures Mania Deluxe' == v.valueForKey_('kCGWindowName'):
            wid = v.valueForKey_('kCGWindowNumber')
            x = int(v.valueForKey_('kCGWindowBounds').valueForKey_('X'))
            y = int(v.valueForKey_('kCGWindowBounds').valueForKey_('Y'))
            width = int(v.valueForKey_('kCGWindowBounds').valueForKey_('Width'))
            height = int(v.valueForKey_('kCGWindowBounds').valueForKey_('Height'))

            wid_list.append(str(wid))
    return wid_list


def screen_capture(file_name):
    per_wid = get_wid_list()[0]
    print 'Wid', per_wid
    cmd_line = 'screencapture -l {0} {1}'.format(per_wid, os.path.join(TMP_IMG_PATH, file_name))
    return os.system(cmd_line)


if __name__ == '__main__':
    import time

    TMP_IMG_NAME = config.get(SECTION_NAME, 'tmp_img_name')
    WAIT_TIME = config.getint(SECTION_NAME, 'wait_time')
    time.sleep(WAIT_TIME)
    screen_capture('{}.png'.format(TMP_IMG_NAME))
