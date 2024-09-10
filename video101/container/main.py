import ffmpeg
import os

def extract_streams(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract video stream
    video_output = os.path.join(output_dir, 'video.h264')
    ffmpeg.input(input_file).output(video_output, vcodec='copy', an=None).run()
    print(f"Extracted video stream to {video_output}")

    # Extract audio stream
    audio_output = os.path.join(output_dir, 'audio.aac')
    ffmpeg.input(input_file).output(audio_output, acodec='copy', vn=None).run()
    print(f"Extracted audio stream to {audio_output}")

    # Extract subtitle stream (if available)
    subtitle_output = os.path.join(output_dir, 'subtitles.srt')
    try:
        ffmpeg.input(input_file).output(subtitle_output, scodec='copy', vn=None, an=None).run()
        print(f"Extracted subtitle stream to {subtitle_output}")
    except ffmpeg.Error:
        print("No subtitle stream found or failed to extract subtitles.")

        # Generate a fake subtitle file with sample lines
        subtitle_output = os.path.join(output_dir, 'subtitles.srt')
        with open(subtitle_output, 'w') as subtitle_file:
            subtitle_file.write("1\n00:00:01,000 --> 00:00:05,000\nHello, this is a sample subtitle.\n\n")
            subtitle_file.write("2\n00:00:06,000 --> 00:00:10,000\nThis is another line of subtitles.\n")

        print(f"Generated fake subtitle file at {subtitle_output}")

    return video_output, audio_output, subtitle_output

def reassemble_container(input_dir, output_file):
    # Read files from the output directory
    video_file = os.path.join(input_dir, 'video.h264')
    audio_file = os.path.join(input_dir, 'audio.aac')
    subtitle_file = os.path.join(input_dir, 'subtitles.srt')

    # Reassemble the video, audio, and subtitle streams into a new container
    video_stream = ffmpeg.input(video_file)
    audio_stream = ffmpeg.input(audio_file)

    ffmpeg.output(
        video_stream,
        audio_stream,
        output_file,
        vf='subtitles={}'.format(subtitle_file),
        acodec='aac'  # Set audio codec, no vcodec since we want to re-encode video
    ).run()
    print(f"Reassembled into {output_file}")

if __name__ == "__main__":
    input_video = 'input_video.mp4'  # Replace with your input video file path
    output_directory = 'output_streams'
    output_video = 'output_video.mp4'  # Output file after reassembling

    # Step 1: Extract streams
    video_path, audio_path, subtitle_path = extract_streams(input_video, output_directory)

    # Step 2: Reassemble into a new video container
    reassemble_container(output_directory, output_video)
