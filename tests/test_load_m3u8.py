# _*_coding:utf-8_*_

from load_m3u8 import resolve


def test_download():
    m3u8_url = ''
    load_obj = resolve.Load_M3U8(m3u8_url)
    load_obj.run()
