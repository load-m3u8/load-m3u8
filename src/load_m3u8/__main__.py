# _*_coding:utf-8_*_

import argparse
import logging
import os
import sys

from version import __version__
from load_m3u8.resolve import LoadM3U8

_options = [
    'help',
    'version',
    'm3u8_url',
    'video_path',
    'process_workers',
    'thread_workers',
]


def main(**kwargs):
    """
    Main entry point.
    [-h] [-v] -mu M3U8_URL [-vp VIDEO_PATH] [-pw PROCESS_WORKERS] [-tw THREAD_WORKERS]
    """
    usage = 'load-m3u8 [OPTION]... url...'
    description = '\n\t\tDownload m3u8 video, support AES decryption'
    parser = argparse.ArgumentParser(usage=usage, description=description, add_help=True)

    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-d', '--debug', action='store_true', help='show traceback and other debug info')
    parser.add_argument('URL', nargs='*', type=str, help=argparse.SUPPRESS)

    download_group = parser.add_argument_group('Download options')
    download_group.add_argument('-o', '--output-dir', default='.', help='Set output directory')
    download_group.add_argument('-i', '--input-file', metavar='FILE', type=argparse.FileType('r'),
                                help='Read non-playlist URLs from FILE')

    workers_group = parser.add_argument_group('Workers options')
    workers_group = workers_group.add_mutually_exclusive_group()
    workers_group.add_argument('-pw', '--process_workers', type=int, nargs=1, help='number of process used')
    workers_group.add_argument('-tw', '--thread_workers', type=int, nargs=1, help='number of threads used')

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        stream=sys.stdout)

    m3u8_urls = []
    if args.input_file:
        logging.debug('you are trying to load urls from %s', args.input_file)
        m3u8_urls.extend(args.input_file.read().splitlines())
        args.input_file.close()
    m3u8_urls.extend(args.URL)

    if not m3u8_urls:
        parser.print_help()
        sys.exit()
    video_dir = args.output_dir
    abspath = os.path.abspath(video_dir)
    index = 0
    for m3u8_url in m3u8_urls:
        video_path = os.path.join(abspath, str(index) + '.ts')
        index = index + 1
        load_obj = LoadM3U8(m3u8_url, video_path, args.process_workers, args.thread_workers)
        load_obj.run()
        logging.info('Video download is complete, video address: %s', load_obj.video_path)


if __name__ == '__main__':
    main()
