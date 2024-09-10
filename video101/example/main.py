import ffmpeg

def encode_video(input_file, output_file, resolution, codec='libx264', bitrate='1000k'):
    try:
        # Using ffmpeg to encode the video
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec=codec, video_bitrate=bitrate, s=resolution, format='mp4')
            .run(overwrite_output=True)
        )
        print(f"Video encoded successfully at {resolution} and saved as {output_file}")
    except ffmpeg.Error as e:
        print("An error occurred during encoding:", e)

# Example usage:
input_video = 'input_video.mov'  # Replace with your input video file path

# Encode the video into different resolutions
encode_video(input_video, 'output_360p.mp4', '640x360', bitrate='700k')   # 360p
encode_video(input_video, 'output_720p.mp4', '1280x720', bitrate='2500k') # 720p
encode_video(input_video, 'output_1080p.mp4', '1920x1080', bitrate='5000k') # 1080p
