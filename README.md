# load_m3u8

## Import
```
from load_m3u8.resolve import Load_M3U8

m3u8_url = 'https://valipl.cp31.ott.cibntv.net/6572ADA8974387172E4EE355F/03000600005EA29CA08BB78000000090EA5C91-6344-4D54-A7DA-0A628B58F1DC.m3u8?ccode=0502&duration=1424&expire=18000&psid=68f923e911a2d51a4fb67ee0415ee72843102&ups_client_netip=1b733e92&ups_ts=1590998852&ups_userid=&utid=RzUvFpAZ8AcCARtzPpKg2gZP&vid=XMTY1ODYzMjQ1Ng&vkey=B83e330f14faead2b94cd3e33b8e90d81&sm=1&operate_type=1&dre=u37&si=73&eo=0&dst=1&iv=0&s=facfcb0cec2511e583e8&type=mp4hdv3&bc=2'
load_obj = Load_M3U8(m3u8_url)
load_obj.run()
```

## Usage
```
pip install load_m3u8
load_m3u8 -mu https://valipl.cp31.ott.cibntv.net/6572ADA8974387172E4EE355F/03000600005EA29CA08BB78000000090EA5C91-6344-4D54-A7DA-0A628B58F1DC.m3u8?ccode=0502&duration=1424&expire=18000&psid=68f923e911a2d51a4fb67ee0415ee72843102&ups_client_netip=1b733e92&ups_ts=1590998852&ups_userid=&utid=RzUvFpAZ8AcCARtzPpKg2gZP&vid=XMTY1ODYzMjQ1Ng&vkey=B83e330f14faead2b94cd3e33b8e90d81&sm=1&operate_type=1&dre=u37&si=73&eo=0&dst=1&iv=0&s=facfcb0cec2511e583e8&type=mp4hdv3&bc=2
```