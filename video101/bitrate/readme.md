# Bitrate
```sh
# Get bitrate of input video
# -i: input file
ffmpeg -i input_video.mp4
# -> 5000 kb/s, h264

# Wont make video any better, just changes the container size
ffmpeg -i input_video.mp4 -b:v 20000k output_video_high.mp4

# Lower bitrate -> lower quality, smaller file size
ffmpeg -i input_video.mp4 -b:v 500k output_video_low.mp4

# Different codecs -> lower bitrate (500k), same quality, smaller file size (efficient codec)
# -c:v: codec
ffmpeg -i input_video.mp4 -c:v libx265 output_video_h265.mp4
```

# Common variations

| Resolution | Bitrate (Video) | Devices/Bandwidth |
| ---------- | -------------- | ---------------- |
| 2160p (4K) | 15,000 - 25,000 kbps | 4K TVs, high-speed connections (fiber) |
| 1440p (2K) | 9,000 - 15,000 kbps | High-end devices, fast connections |
| 1080p (Full HD) | 4,000 - 8,000 kbps | Desktops, large tablets, fast connections |
| 720p (HD) | 2,500 - 5,000 kbps | Laptops, tablets, moderate connections |
| 480p (SD) | 1,000 - 2,500 kbps | Mobile devices, slower connections |
| 360p (Low) | 500 - 1,000 kbps | Low-end phones, poor connections |
| 240p (Very Low) | 300 - 500 kbps | Extremely slow connections or older devices |

# ffmpeg key settings
- `-b:v`: video bitrate
- `-maxrate`: maximum bitrate
- `-bufsize`: buffer size
- `-vf scale`: resize video to fit the resolution
- `-c:a`: audio codec
- `-b:a`: audio bitrate
```sh
# 1080p Full HD
ffmpeg -i input.mp4 -c:v libx264 -b:v 5000k -maxrate 5350k -bufsize 7500k -vf scale=1920:1080 -c:a aac -b:a 192k output_1080p.mp4

# 720p HD
ffmpeg -i input.mp4 -c:v libx264 -b:v 3000k -maxrate 3200k -bufsize 5000k -vf scale=1280:720 -c:a aac -b:a 128k output_720p.mp4

# 480p SD
ffmpeg -i input.mp4 -c:v libx264 -b:v 1500k -maxrate 1600k -bufsize 3000k -vf scale=854:480 -c:a aac -b:a 128k output_480p.mp4

# 360p Low
ffmpeg -i input.mp4 -c:v libx264 -b:v 800k -maxrate 850k -bufsize 1200k -vf scale=640:360 -c:a aac -b:a 96k output_360p.mp4

# 240p Very Low
ffmpeg -i input.mp4 -c:v libx264 -b:v 400k -maxrate 450k -bufsize 800k -vf scale=426:240 -c:a aac -b:a 64k output_240p.mp4
```

# Package
```sh
ffmpeg -i input.mp4 -c:a aac -ar 48000 -b:a 128k -c:v libx264 -vf "scale=1280:720" \
    -hls_time 10 -hls_playlist_type vod -b:v 3000k -maxrate 3000k -bufsize 6000k \
    -hls_segment_filename "output_720p_%03d.ts" output_720p.m3u8
```