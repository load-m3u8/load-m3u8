# _*_coding:utf-8_*_

import argparse
import logging
import sys

from version import __version__
from generate_m3u8.resolve import CreateM3U8

_options = [
    'help',
    'version',
    'm3u8_path',
    'video_path',
    'hls_time',
    'hls_enc_key',
    'hls_enc_iv',
    'hls_enc_key_url',
    'hls_base_url',
    'hls_segment_filename',
]


def main(**kwargs):
    """
    Main entry point.
    """
    usage = 'gen-m3u8 [OPTION]... url...'
    description = '\n\t\tEncrypt video by AES'
    parser = argparse.ArgumentParser(usage=usage, description=description, add_help=True)

    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-d', '--debug', action='store_true', help='show traceback and other debug info')

    parser.add_argument('video_path', type=str, help='Set video path')
    parser.add_argument('-m3u8', '--m3u8_path', type=str, default=None, help='Set m3u8 output path')

    encrypt_options = parser.add_argument_group('Encrypt options')
    encrypt_options.add_argument('-t', '--hls_time', default=60, help='Set segment time')
    encrypt_options.add_argument('-iv', '--hls_enc_iv', default=None, help='Set AES IV')
    encrypt_options.add_argument('-key', '--hls_enc_key', default=None, help='Set AES key')
    encrypt_options.add_argument('-url', '--hls_enc_key_url', default=None, help='Set key url')
    encrypt_options.add_argument('-method', '--hls_enc_key_url_method', default=None, help='Set key url method')
    encrypt_options.add_argument('-base', '--hls_base_url', default=None, help='Set base url')
    encrypt_options.add_argument('-seg', '--hls_segment_filename', default=None, help='Set segment name')

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        stream=sys.stdout)

    if not args.video_path:
        parser.print_help()
        sys.exit()

    create_obj = CreateM3U8(args.video_path, m3u8_path=args.m3u8_path, hls_time=args.hls_time,
                            hls_enc_key=args.hls_enc_key, hls_enc_iv=args.hls_enc_iv,
                            hls_enc_key_url=args.hls_enc_key_url, hls_enc_key_url_method=args.hls_enc_key_url_method,
                            hls_base_url=args.hls_base_url, hls_segment_filename=args.hls_segment_filename)
    create_obj.run()


if __name__ == '__main__':
    main()
