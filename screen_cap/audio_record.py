import pyaudiowpatch as pyaudio
import wave

def record_audio(duration, output_file="internal_output.wav"):
    p = pyaudio.PyAudio()

    try:
        # Get default WASAPI output device info
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    except IOError:
        print("WASAPI is not available on this system.")
        p.terminate()
        exit()

    # Find the loopback device corresponding to your default speakers
    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

    if not default_speakers["isLoopbackDevice"]:
        for loopback in p.get_loopback_device_info_generator():
            if default_speakers["name"] in loopback["name"]:
                default_speakers = loopback
                break
        else:
            print("No matching loopback device found.")
            p.terminate()
            exit()

    print(f"Recording from: {default_speakers['name']}")

    wave_file = wave.open(output_file, 'wb')
    wave_file.setnchannels(default_speakers["maxInputChannels"])
    wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(int(default_speakers["defaultSampleRate"]))

    def callback(in_data, frame_count, time_info, status):
        wave_file.writeframes(in_data)
        return (in_data, pyaudio.paContinue)

    # Open the stream using the loopback device
    stream = p.open(format=pyaudio.paInt16,
                    channels=default_speakers["maxInputChannels"],
                    rate=int(default_speakers["defaultSampleRate"]),
                    input=True,
                    input_device_index=default_speakers["index"],
                    stream_callback=callback)

    stream.start_stream()

    import time
    time.sleep(duration)

    stream.stop_stream()
    stream.close()
    wave_file.close()
    p.terminate()

    print(f"Recording saved to {output_file}")


if __name__ == "__main__":
    record_audio(10)