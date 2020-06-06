# _*_coding:utf-8_*_

import os
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from glob import iglob
from urllib.parse import urljoin

import m3u8
from natsort import natsorted

from load_m3u8 import load_ts

windows_invalid = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
'''Unresolvable characters in the Windows System'''


class Load_M3U8(object):
    '''
        Use M3U8 file to download ts format video.
        Support video decryption by AES.
        Dependent libraries: pip install m3u8 requests natsort
    '''

    m3u8_url: str
    video_path: str
    video_folder: str
    ts_folder: str

    def __init__(self, m3u8_url, video_path='/tmp/m3u8.ts', process_workers=None, thread_workers=None):
        use_process = thread_workers is None
        self.pool = ProcessPoolExecutor(max_workers=process_workers) if use_process else ThreadPoolExecutor(
            max_workers=thread_workers)
        self.m3u8_url = m3u8_url

        video_name = tmp = os.path.basename(video_path)
        for i in windows_invalid:
            if i in video_name:
                tmp = tmp.replace(i, '')
        video_name = tmp

        self.video_folder = os.path.dirname(video_path)
        self.video_path = os.path.join(self.video_folder, video_name)
        self.ts_folder = os.path.join(self.video_folder, video_name.split('.')[0])

        if not os.path.exists(self.video_folder):
            os.mkdir(self.video_folder)
        if not os.path.exists(self.ts_folder):
            os.mkdir(self.ts_folder)

    def __load_m3u8(self):
        urls = self.__resolve_url()
        for index, url in enumerate(urls):
            feature = self.pool.submit(load_ts, [url[0], url[1], f'{self.ts_folder}/{index}.ts'])
            # feature.add_done_callback(load_ts_done)
        self.pool.shutdown()

    def __resolve_url(self):
        m3u8_obj = m3u8.load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri
        if m3u8_obj.is_variant:
            '''Get HD video address'''
            bandwidth = 0
            for seq in m3u8_obj.playlists:
                if seq.stream_info.bandwidth > bandwidth:
                    bandwidth = seq.stream_info.bandwidth
                    self.m3u8_url = seq.absolute_uri
            print('redirect video address: ', self.m3u8_url)
            m3u8_obj = m3u8.load(self.m3u8_url)
            base_uri = m3u8_obj.base_uri
        segments = m3u8_obj.segments
        encryptKey = m3u8_obj.keys[0] if len(m3u8_obj.keys) > 0 else None
        for seg in segments:
            yield [urljoin(base_uri, seg.uri), encryptKey]

    def run(self):
        self.__load_m3u8()
        ts_path = self.ts_folder + '/*.ts'
        with open(self.video_path, 'wb') as fp:
            for ts in natsorted(iglob(ts_path)):
                with open(ts, 'rb') as ft:
                    fp.write(ft.read())
        for ts in iglob(ts_path):
            os.remove(ts)
        os.rmdir(self.ts_folder)