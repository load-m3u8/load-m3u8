# _*_coding:utf-8_*_
import binascii
import logging
import os.path
import random
import string

import ffmpy


def random_string(counts=1):
    population = string.ascii_letters + string.digits + '!@#$%^&*()_+=-'
    random_choice = random.sample(population, counts)
    return ''.join(random_choice)


def rand_hex(counts=8):
    random_choice = random_string(counts)
    random_hex = binascii.b2a_hex(random_choice.encode()).decode()
    logging.debug(random_choice, ' -> ', random_hex)
    return random_hex


class CreateM3U8(object):
    """
       Cut a video into multiple ts segments,
       and use AES-128 encryption for each segment during the cutting process,
       and finally generate a m3u8 video index file

       1. Generate AES KEY
           Run test_rand_hex()

       2. Generate IV
           Run test_rand_hex()

       3. Prepare video
           C:/tmp/test.ts

       4. Start web service, ffmpeg check key address
           Run test_encrypt_web()

       Full command reference:
           ffmpeg -y -i C:/tmp/test.ts
               -hls_time 60
               -hls_enc true -hls_enc_key 5dd0a99887d8c801 -hls_enc_iv 5dd0a99887d8c801 -hls_enc_key_url http://127.0.0.1/enc.key
               -hls_base_url C:/tmp/test/
               -hls_playlist_type vod
               -hls_segment_filename C:/tmp/test/segment_%d.ts C:/tmp/test.m3u8

       HTTP Live Streaming parameter description:
           hls_time:             The length of each segment of the divided video, in seconds
           hls_enc:              Enable AES encryption
           hls_enc_key:          AES key, 16 bits
           hls_enc_iv:           IV vector used for AES encryption, 16 bits
           hls_enc_key_url:      The address to obtain the key when decrypting the video
           hls_base_url:         The root address of the video URL when downloading the video
           hls_segment_filename: Video file name after cutting
           hls_playlist_type:    Set m3u8 video type, optional values EVENT, VOD. can be overlooked. Because the generated m3u8 file contains #EXT-X-ENDLIST
       """

    video_path: str
    m3u8_path: str
    hls_time: int
    hls_enc_key: str
    hls_enc_iv: str
    hls_enc_key_url: str
    hls_base_url: str
    hls_segment_filename: str
    outputs: str

    def __init__(self, video_path, m3u8_path=None, hls_time=60, hls_enc_key=None, hls_enc_iv=None,
                 hls_enc_key_url=None, hls_enc_key_url_method=None, hls_base_url=None, hls_segment_filename=None):
        self.video_path = video_path
        self.m3u8_path = video_path + '.m3u8' if m3u8_path is None else m3u8_path
        self.hls_time = hls_time
        self.hls_enc_key = hls_enc_key
        self.hls_enc_iv = hls_enc_iv
        self.hls_enc_key_url = hls_enc_key_url
        self.method = 'PUT' if hls_enc_key_url_method is None else hls_enc_key_url_method
        self.hls_base_url = os.path.dirname(video_path) if hls_base_url is None else hls_base_url
        self.hls_segment_filename = os.path.basename(
            video_path) + '_%d.ts' if hls_segment_filename is None else hls_segment_filename + '_%d.ts'

        self.hls_base_url = self.hls_base_url.replace('\\', '/')
        if not self.hls_base_url.endswith('/'):
            self.hls_base_url = self.hls_base_url + '/'
        self.hls_segment_filename = os.path.join(self.hls_base_url, self.hls_segment_filename)

        outputs = ''
        if hls_enc_key is not None:
            outputs += ' -hls_enc true'
            outputs += ' -hls_enc_key ' + self.hls_enc_key
            if hls_enc_iv is not None:
                outputs += ' -hls_enc_iv ' + self.hls_enc_iv

        if hls_enc_key_url is not None:
            outputs += ' -method ' + self.method
            outputs += ' -hls_enc_key_url ' + self.hls_enc_key_url

        outputs += ' -hls_flags append_list'
        outputs += ' -hls_segment_type mpegts'
        outputs += ' -hls_playlist_type vod'
        outputs += ' -hls_base_url ' + self.hls_base_url
        outputs += ' -hls_segment_filename ' + self.hls_segment_filename
        outputs += ' -hls_time ' + str(hls_time)
        self.outputs = outputs
        logging.debug('outputs: %s', self.outputs)

    def run(self):
        try:
            if not os.path.exists(os.path.dirname(self.m3u8_path)):
                os.makedirs(os.path.dirname(self.m3u8_path))
            if not self.hls_base_url.startswith(('https://', 'http://', 's3://')) and not os.path.exists(
                    self.hls_base_url):
                os.makedirs(self.hls_base_url)
            ff = ffmpy.FFmpeg(global_options=['-y'],
                              inputs={self.video_path: None},
                              outputs={self.m3u8_path: self.outputs})
            logging.debug('run ffmpeg: %s', ff.cmd)
            ff.run()
        except Exception as e:
            logging.exception('encryption failed')
