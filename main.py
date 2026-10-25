import threading
from UI.UI import App
from screen_cap.main_screen_record import screen_audio_record
from video_detect import video_detect
from audio_detect import audio_detect
from image_detect import image_detect
from UI.pop_up import CustomPopup

popup = None

def live(self):
    global popup

    if popup == None or not popup.exists():
        popup = CustomPopup("live loading")

    if self._live_running == False:

        def worker(stop_event):
            while not stop_event.is_set():

                screen_audio_record()

                if stop_event.is_set():
                    break

                result = video_detect()
                audio_detect() #TO-DO

                if stop_event.is_set():
                    break

                if result == -1.0:
                    popup.update_message("No face detected")
                else:
                    popup.update_message("The chance of this face\nbeing real is")
                    popup.update_chart(result)

            if stop_event.is_set():
                popup.destroy()

        self.stop_live_signal = threading.Event()
        self.live_loop = threading.Thread(target=worker, args=(self.stop_live_signal,),daemon=True)
    
        self.live_loop.start()
        self._live_running = True
        self.live_btn.configure(text="■  Stop Monitoring", fg_color="#6B7280",
                                        hover_color="#4B5563")
    else:
        self.stop_live_signal.set()
        self._live_running = False
        self.live_btn.configure(text="●  Start Live Monitoring",
                                        fg_color="#F87171", hover_color="#DC2626")

def file_detect(self):
    global popup

    if self.file_path == None:
        return
    else:
        if popup == None or not popup.exists():
                popup = CustomPopup("Loading")

        if self.kind == "Video":
            result = video_detect(self.file_path)
        elif self.kind == "Audio":
            result = audio_detect(self.file_path)
        elif self.kind == "Image":
            result = image_detect(self.file_path)
        else:
            result = 0

    if result == -1.0:
        popup.update_message("No face detected")
    else:
        popup.update_message("The chance of this face\nbeing real is")
        popup.update_chart(result)

app = App(_on_file_detection_click=lambda: file_detect(app), _on_live_button_click=lambda: live(app))
app.mainloop()