# _*_coding:utf-8_*_

import base64
import binascii
import os.path
import random
import socket
import string
import unittest
from multiprocessing import Process

import ffmpy


def create_encrypt(client_socket):
    """
    Generate AES key
    """
    request_data = client_socket.recv(10240)
    print('request data: \n', request_data.decode(), '\n\n')

    resposne = 'HTTP/1.1 200 OK\r\n'
    resposne += 'Server: Encrypt Server\r\n'
    resposne += 'Content-Type: application/text\r\n'
    resposne += '\r\n'

    # return AES key body
    resposne += '5dd0a99887d8c801'
    # resposne += '0x35646430613939383837643863383031'
    client_socket.send(resposne.encode())
    client_socket.close()


class TestEncrypt(unittest.TestCase):

    def test_hex(self):
        print(binascii.b2a_hex('5dd0a99887d8c801'.encode()))
        print(binascii.a2b_hex('35646430613939383837643863383031'))

    def test_rand_hex(self):
        random_choice = self.random_string(8)
        print(random_choice, ' -> ', binascii.b2a_hex(random_choice.encode()).decode())

    def test_rand_base64(self):
        random_choice = self.random_string(8)
        print(random_choice, ' -> ', base64.encodebytes(random_choice.encode()).decode())

    def random_string(self, counts=1):
        population = string.ascii_letters + string.digits + '!@#$%^&*()_+=-'
        random_choice = random.sample(population, counts)
        return ''.join(random_choice)

    def test_encrypt_web(self):
        """
        Start web service
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", 80))
        server_socket.listen(100)

        while True:
            client_socket, client_address = server_socket.accept()
            client_process = Process(target=create_encrypt, args=(client_socket,))
            client_process.start()
            client_socket.close()

    def test_encrypt(self):
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

        # Set the length of the segment (unit: seconds)
        outputs = ' -hls_time 60'

        # Set AES key
        outputs += ' -hls_enc true -hls_enc_key 5dd0a99887d8c801 -hls_enc_iv 5dd0a99887d8c801'
        # The AES key will be pushed to the interface through the PUT method, and the interface needs to support GET method to query the key
        outputs += ' -method PUT -hls_enc_key_url http://127.0.0.1/enc.key'
        outputs += ' -hls_segment_type mpegts'
        outputs += ' -hls_flags append_list'

        # sequence
        # Set video download address
        encrypt_directory = 'C:/tmp/hls/'
        if not os.path.exists(encrypt_directory):
            os.mkdir(encrypt_directory)
        outputs += ' -hls_base_url ' + encrypt_directory

        # Set m3u8 video type
        outputs += ' -hls_playlist_type vod'

        # Set output path
        outputs += ' -hls_segment_filename ' + encrypt_directory + 'stream_%d.ts'
        ff = ffmpy.FFmpeg(
            global_options=['-y'],
            inputs={'C:/tmp/test.ts': None},
            outputs={'C:/tmp/test.m3u8': outputs}
        )
        print('run ffmpeg:\n', ff.cmd)
        ff.run()
