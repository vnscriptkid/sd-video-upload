# Setup
- pip install ffmpeg-python

# Concepts
- codec: compresses and decompresses video, e.g. h.264, h.265
- bitrates
- container: mp4, mov, avi, mkv
- resolutions: 360, 720, 1080
- streaming protocols: HLS, DASH
- HLS: HTTP Live Streaming
    - .m3u8: manifest file (playlist), first file to be downloaded
    - .ts: video segments (MPEG-2 transport stream)
- manifest files (m3u8 - HLS, mpd - DASH)
    - primary: contains all the video segments
    - variant: contains the video segments for a specific resolution