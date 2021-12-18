# _*_coding:utf-8_*_
import unittest

from load_m3u8 import resolve


class TestUtil(unittest.TestCase):

    def test_download(self):
        m3u8_url = "http://127.0.0.1/test.m3u8"
        m3u8_url = "C:/tmp/test.m3u8"
        load_obj = resolve.Load_M3U8(m3u8_url, video_path='C:/tmp/test_m3u8.ts', process_workers=1, thread_workers=1)
        load_obj.run()
