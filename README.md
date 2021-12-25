# load-m3u8
[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

## Import

```python
from load_m3u8.resolve import LoadM3U8

LoadM3U8("http://www.youtube.com/test.m3u8").run()
```

## Usage
```shell
pip --no-cache-dir install load-m3u8

gen-m3u8 C:/tmp/test.ts -key 5dd0a99887d8c801

load-m3u8 "C:/tmp//test.ts.m3u8" -o "c:/tmp/load"


gen-m3u8 C:/tmp/test.ts -key 5dd0a99887d8c801 -iv 5dd0a99887d8c801 -t 120 -base "C:/tmp/segment" -m3u8 "C:/tmp/m3u8/abc.m3u8" -seg "test_stream" -url "http://127.0.0.1" -method POST -d

load-m3u8 "C:/tmp/m3u8/abc.m3u8" -o "c:/tmp/load" -d -tw 2

load-m3u8 "C:/tmp/m3u8/abc.m3u8" -o "c:/tmp/load" -d -pw 2

```