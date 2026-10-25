import subprocess
import sys
import platform
import time
import threading
from screen_cap.audio_record import record_audio

def screen_record(duration, output_filename="desktop_record.mp4"):
    os_name = platform.system()
    
    # Base FFmpeg command setup
    # -y overwrites output file if it exists
    cmd = ["ffmpeg", "-y"]
    
    # Configure OS-specific capture inputs
    if os_name == "Windows":
        cmd.extend([
            "-f", "gdigrab",
            "-framerate", "30",
            "-i", "desktop"
        ])
    elif os_name == "Darwin":  # macOS
        cmd.extend([
            "-f", "avfoundation",
            "-framerate", "30",
            "-i", "1:none"  # "1" targets main screen, "none" mutes audio
        ])
    elif os_name == "Linux":
        cmd.extend([
            "-f", "x11grab",
            "-framerate", "30",
            "-video_size", "1920x1080",  # Change to match your screen resolution
            "-i", ":0.0"
        ])
    else:
        print(f"Unsupported OS: {os_name}")
        return

    # Add output encoding settings (H.264 video codec)
    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_filename
    ])

    print(f"Starting recording on {os_name}...")
    
    # Start the FFmpeg process
    # stdin=subprocess.PIPE allows us to send 'q' to stop FFmpeg cleanly later
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(duration)

    # Cleanly stop FFmpeg by sending 'q' to its stdin
    print("Recording time reached. Saving video...")
    try:
        process.communicate(input=b'q', timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    print(f"Video saved to: {output_filename}")

if __name__ == "__main__":
    screen_record(10)
