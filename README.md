# load-m3u8

[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

## Import

```python
if __name__ == '__main__':
    from load_m3u8.generate.resolve import CreateM3U8
    
    # Make sure the D:/test/test.ts video file exists
    CreateM3U8('D:/test/test.ts', hls_enc_key='5dd0a99887d8c801').run()

    from load_m3u8.load.resolve import LoadM3U8

    LoadM3U8("D:/test//test.ts.m3u8", video_path="D:/test/load/test_load.ts").run()

    # Download from the Server
    LoadM3U8("http://127.0.0.1/m3u8/test.m3u8").run()
```

## Usage

### install load-m3u8

```shell
pip --no-cache-dir install load-m3u8
```

### Decrypt and Encrypt

```shell
# Make sure the D:/test/test.ts video file exists
gen-m3u8 D:/test/test.ts -key 5dd0a99887d8c801

# Download the video and decrypt it
load-m3u8 "D:/test//test.ts.m3u8" -o "D:/test/load"
```

### Specifying a aes key server

```shell
# Make sure the http://127.0.0.1/enc has access
gen-m3u8 D:/test/test.ts -key 5dd0a99887d8c801 -iv 5dd0a99887d8c801 -t 120 -base "D:/test/segment" -m3u8 "D:/test/m3u8/test.m3u8" -seg "test_stream" -url "http://127.0.0.1/enc" -method POST -d

# Download the video and decrypt it
load-m3u8 "D:/test/m3u8/test.m3u8" -o "D:/test/load" -d -tw 2

OR

load-m3u8 "D:/test/m3u8/test.m3u8" -o "D:/test/load" -d -pw 2
```