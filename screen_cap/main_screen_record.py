import subprocess
import threading
from screen_cap.audio_record import record_audio
from screen_cap.screen_record import screen_record

def merge_audio_video(video_input="desktop_10s.mp4", audio_input="recorded_audio.wav", output_file="merged_output.mp4"):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_input,       # Stream 0: The video source
        "-i", audio_input,       # Stream 1: The separate WAV audio source
        
        # Mapping instructions:
        "-map", "0:v:0",         # Take the first video stream from the 1st input
        "-map", "1:a:0",         # Take the first audio stream from the 2nd input (.wav)
        
        # Encoding choices:
        "-c:v", "copy",          # Direct stream copy for video (Instant, no re-encoding!)
        "-c:a", "aac",           # Encode the raw .wav into compressed AAC format for MP4
        "-b:a", "192k",          # Give the audio a high quality bitrate
        
        # Ensure the video ends cleanly if lengths differ slightly
        "-shortest",             
        output_file
    ]
    
    print(f"Merging {audio_input} into {video_input}...")
    
    # Run the FFmpeg process
    process = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    
    if process.returncode == 0:
        print(f"✓ Success! Final file saved to: {output_file}")
    else:
        print("✗ Merging failed. FFmpeg Error:")
        print(process.stderr)

def screen_audio_record():
    vid = threading.Thread(target=screen_record,args=(5,"outputs/video.mp4",))
    aud = threading.Thread(target=record_audio,args=(5,"outputs/audio.wav"))
    vid.start()
    aud.start()
    vid.join()
    aud.join()
    merge_audio_video(
        video_input="outputs/video.mp4", 
        audio_input="outputs/audio.wav", 
        output_file="outputs/video_w_audio.mp4"
    )

if __name__ == "__main__":
    screen_audio_record()