# _*_coding:utf-8_*_
import unittest

from load_m3u8 import resolve


class TestUtil(unittest.TestCase):
    def test_download(self):
        m3u8_url = "http://www.youtube.com/test.m3u8"
        load_obj = resolve.Load_M3U8(m3u8_url)
        load_obj.run()