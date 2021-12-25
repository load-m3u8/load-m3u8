import logging
import sys
import unittest

from src.generate_m3u8 import resolve

debug = True
log_level = logging.DEBUG if debug else logging.INFO
logging.basicConfig(level=log_level,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)


class TestCreateM3U8(unittest.TestCase):

    def test_generate(self):
        video_path = 'c:/tmp/test.ts'
        create_obj = resolve.CreateM3U8(video_path, m3u8_path=None, hls_time=60, hls_enc_key=None, hls_enc_iv=None,
                                        hls_enc_key_url=None, hls_base_url=None, hls_segment_filename=None)
        create_obj.run()
