import ffmpeg
import http.server
import socketserver
import os

# Function to chunk the video using ffmpeg-python
def chunk_video(input_file, output_dir, segment_time=2):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the ffmpeg command to chunk the video
    (
        ffmpeg
        .input(input_file)
        .output(os.path.join(output_dir, 'stream.m3u8'),
                codec='copy',
                hls_time=segment_time,
                hls_list_size=0,
                hls_segment_filename=os.path.join(output_dir, 'stream%d.ts'),
                format='hls')
        .run()
    )
    print(f"Video chunked successfully into {output_dir}.")

# Function to start the web server
def start_server(port=8000):
    Handler = http.server.SimpleHTTPRequestHandler

    # Serve files from the current directory
    os.chdir('output')
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

# Main execution
if __name__ == "__main__":
    input_video = 'input_video.mp4'  # Replace with your input video file path
    output_dir = 'output'  # Directory to store chunked video and HTML file

    # Step 1: Chunk the video
    chunk_video(input_video, output_dir)

    # Step 2: Start the web server to serve the files
    start_server()
