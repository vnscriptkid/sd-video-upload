import ffmpeg
import os
import http.server
import socketserver

def create_hls_streams(input_file, output_dir):
    # Define the resolutions and bitrates
    variants = [
        {'resolution': '640x360', 'v_bitrate': '800k', 'a_bitrate': '128k', 'maxrate': '856k', 'bufsize': '1200k', 'output_dir': '360p'},
        {'resolution': '1280x720', 'v_bitrate': '2500k', 'a_bitrate': '128k', 'maxrate': '2678k', 'bufsize': '3750k', 'output_dir': '720p'},
        {'resolution': '1920x1080', 'v_bitrate': '5000k', 'a_bitrate': '128k', 'maxrate': '5350k', 'bufsize': '7500k', 'output_dir': '1080p'}
    ]

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create HLS streams for each variant
    for variant in variants:
        variant_output_dir = os.path.join(output_dir, variant['output_dir'])
        if not os.path.exists(variant_output_dir):
            os.makedirs(variant_output_dir)

        output_file = os.path.join(variant_output_dir, 'stream.m3u8')

        (
            ffmpeg
            .input(input_file)
            .output(output_file,
                    vf=f"scale={variant['resolution']}",
                    vcodec='libx264',
                    acodec='aac',
                    **{'b:v': variant['v_bitrate'], 'b:a': variant['a_bitrate']},
                    maxrate=variant['maxrate'],
                    bufsize=variant['bufsize'],
                    hls_time=2, # Segment duration in seconds
                    hls_playlist_type='vod',
                    hls_segment_filename=os.path.join(variant_output_dir, 'segment%d.ts'),
                    f='hls')
            .run()
        )
        print(f"Created HLS stream for {variant['resolution']} at {variant_output_dir}")

    # Create the master playlist
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as master_playlist:
        master_playlist.write('#EXTM3U\n')
        for variant in variants:
            master_playlist.write(f"#EXT-X-STREAM-INF:BANDWIDTH={int(variant['v_bitrate'][:-1]) * 1000},RESOLUTION={variant['resolution']}\n")
            master_playlist.write(f"{variant['output_dir']}/stream.m3u8\n")
    print(f"Created master playlist at {master_playlist_path}")

def start_http_server(directory, port=8000):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    input_video = 'input_video.mov'  # Replace with your input video file path
    output_directory = 'output'

    # Step 1: Generate HLS streams
    create_hls_streams(input_video, output_directory)

    # Step 2: Start the HTTP server
    start_http_server(output_directory)
