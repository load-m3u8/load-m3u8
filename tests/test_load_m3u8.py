# _*_coding:utf-8_*_
import logging
import sys
import unittest

from src.load_m3u8 import resolve

debug = True
log_level = logging.DEBUG if debug else logging.INFO
logging.basicConfig(level=log_level,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)


class TestLoadM3U8(unittest.TestCase):

    def test_download(self):
        m3u8_url = "http://127.0.0.1/test.m3u8"
        m3u8_url = "C:/tmp/test.m3u8"
        load_obj = resolve.LoadM3U8(m3u8_url, video_path='C:/tmp/test_m3u8.ts', process_workers=1, thread_workers=1)
        load_obj.run()
