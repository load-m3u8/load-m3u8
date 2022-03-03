.. load-m3u8 documentation master file, created by
   sphinx-quickstart on Sat Dec 25 16:37:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to load-m3u8's documentation!
=====================================
[TOC]

m3u8文件
--------

M3U: Moving Picture Experts Group Audio Layer 3 Uniform Resource Locator

一个存储了多个音频的索引文件，记录了多个音频片段

M3U8:
使用UTF-8编码的M3U文件，可以存储视频流编码为H.264，音频流编码为AAC的音视频片段地址，视频格式为
ts

TS: Transport Stream 全称为
MPEG2-TS，特点就是要求从视频流的任一片段开始都是可以独立解码的。

HLS协议
-------

HTTP Live Streaming

由苹果公司提出的基于HTTP的流媒体网络传输协议，基于 m3u8
文件完成对视频的传输。

它的工作原理是把整个流分成一个个小的基于HTTP的文件来下载，每次只下载一些。当媒体流正在播放时，客户端可以选择从许多不同的备用源中以不同的速率下载同样的资源，允许流媒体会话适应不同的数据速率。

HLS 流可以用于直播，也可以用于点播。

点播：使用静态的播放列表文件，列表文件指向所有的播放文件

直播：使用动态的播放列表文件，需要实时更新播放索引文件

.. code:: mermaid

   flowchart LR
       服务端 --> 获取视频 --> 视频切割 --> publish(发布 m3u8 文件和 ts 视频片段)
       
       客户端 --> 下载m3u8文件 --> 下载AES密钥 --> 下载TS片段 --> 解密TS片段后播放

多分辨率视频

先有一个总的m3u8文件，记录不同分辨率的m3u8文件地址，当用户选择不同的分辨率时候会切换到对应的m3u8文件，然后下载对应的
ts 片段，解密 ts 片段后播放

HLS协议文档: https://datatracker.ietf.org/doc/html/rfc8216

python 版本的对 m3u8 文件解析工具：

https://github.com/globocom/m3u8

https://pypi.org/project/m3u8

ffmpeg
------

一个完整的跨平台解决方案，用于录制、转换和流式传输音频和视频。

官方文档： https://ffmpeg.org/documentation.html

可以将一个完整的视频文件切割成符合 m3u8 格式的多个 ts
视频片段，支持对视频片段进行 AES 加密。

m3u8 用途
---------

1. 加密视频，保护付费视频
2. 插播广告，可以在任意片段位置插播一个广告视频
3. 多码率的适配：因网络差异使用不同的分辨率保证视频流畅度

m3u8 加密视频
-------------

   描述解析 m3u8 文件的技术细节

.. code:: mermaid

   flowchart LR   
       客户端 --> 下载m3u8文件 --> 下载AES密钥 --> 下载TS片段 --> 解密TS片段后播放

.. code:: mermaid

   sequenceDiagram
       Client ->>+ Server: download m3u8
       Note over Server: 验证用户 token
       Server ->>- Client: 返回一个临时m3u8文本
       
       Client -->>+ Server: download AES key
       Note over Server: 验证密钥 token
       Server -->>- Client: 返回视频的密钥
       
       Client ->>+ Server: download ts video
       Note over Server: 验证 TS 视频 token
       Server ->>- Client: 返回加密的视频流
       Note over Client: 使用 AES 密钥解密视频

..

   默认生成的m3u8文件存储的 ts 地址和密钥地址都是固定的，客户端获取 m3u8
   文件时服务器需要读取到对应的文件，将地址替换成做了 token
   拦截的地址，当客户端请求密钥和视频的时候，验证相应的 token
   后再转发到固定的地址。

   密钥token 和 ts token 都设置一个有效期，只在短时间内可用。

FAQ

为什么要用 TS 而不是 MP4?

   这是因为两个 TS 片段可以无缝拼接，播放器能连续播放，而 MP4
   文件由于编码方式的原因，两段 MP4 不能无缝拼接，播放器连续播放两个 MP4
   文件会出现破音和画面间断，影响用户体验

