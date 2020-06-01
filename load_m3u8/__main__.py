# _*_coding:utf-8_*_

import argparse

from load_m3u8._version import __version__
from load_m3u8.resolve import Load_M3U8

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
    usage = '\n\t\tload_m3u8 [-h] [-v] -mu M3U8_URL [-vp VIDEO_PATH] [-pw PROCESS_WORKERS] [-tw THREAD_WORKERS]'
    description = '\n\t\tDownload m3u8 video, support AES decryption'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-mu', '--m3u8_url', dest='m3u8_url', required=True, type=str, nargs=1, help='m3u8 url')

    parser.add_argument('-vp', '--video_path', dest='video_path', required=False, type=str, nargs=1,
                        default='/tmp/m3u8.ts', help='Video storage path (default: /tmp/m3u8.ts)')

    parser.add_argument('-pw', '--process_workers', dest='process_workers', required=False, type=int, nargs=1,
                        help='Number of process used')

    parser.add_argument('-tw', '--thread_workers', '--thread_workers', dest='thread_workers', required=False, type=int,
                        nargs=1, help='Number of threads used')

    args = parser.parse_args()

    print(args.m3u8_url, args.video_path)

    load_obj = Load_M3U8(args.m3u8_url, video_path=args.video_path, process_workers=args.process_workers,
                         thread_workers=args.thread_workers)
    load_obj.run()
    print('Video download is complete, video address: \n', load_obj.video_path)


if __name__ == '__main__':
    main()
