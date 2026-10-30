import threading
import transformers
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor, pipeline
from UI.UI import App
from screen_cap.main_screen_record import screen_audio_record
from video_detect import video_detect
from audio_detect import audio_detect
from image_detect import image_detect
from UI.pop_up import CustomPopup
from pathlib import Path

popup = None

def live(self):
    global popup

    if ( popup == None or not popup.exists() )and self._live_running == False:
        popup = CustomPopup("live loading")

    if self._live_running == False:

        #load models
        audio_model_name = "garystafford/wav2vec2-deepfake-voice-detector"
        audio_model = AutoModelForAudioClassification.from_pretrained(audio_model_name)
        feature_extractor = AutoFeatureExtractor.from_pretrained(audio_model_name)

        video_model = pipeline(
            "video-classification",
            model="KoreaPeter/ms-eff-gcvit-deepfake-b0-ff-plus-plus", 
            device = "cuda" if torch.cuda.is_available() else "cpu",
            trust_remote_code=True,
        )

        def worker(stop_event):
            while not stop_event.is_set():

                screen_audio_record()

                if stop_event.is_set() or ( popup == None or not popup.exists() ):
                    self._live_running = False
                    self.live_btn.configure(text="●  Start Live Monitoring",
                                            fg_color="#F87171", hover_color="#DC2626")
                    break

                video_result = video_detect(video_model)
                audio_result = audio_detect(audio_model,feature_extractor)

                result = max(video_result,audio_result)

                if stop_event.is_set() or ( popup == None or not popup.exists() ):
                    self._live_running = False
                    self.live_btn.configure(text="●  Start Live Monitoring",
                                            fg_color="#F87171", hover_color="#DC2626")
                    break

                popup.update_message("Fake probability :")
                popup.update_chart(result)

                explain_message = ""
                if video_result == -1:
                    explain_message += "No face detected but audio checked \n"
                elif video_result > 0.5:
                    explain_message += f"Fake live video detected ({video_result* 100:.0f}%) \n"

                if audio_result > 0.5:
                    explain_message += f"Fake live audio detected ({audio_result* 100:.0f}%) \n"

                if result <= 0.4:
                    explain_message += "The current live should be real"
                elif result <= 0.6 :
                    explain_message += "The current live is uncertain"
                else:
                    explain_message += "The current live is probably fake"

                popup.update_explain_message(explain_message)
                    

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
            result = video_detect(file=self.file_path)
        elif self.kind == "Audio":
            result = audio_detect(file=self.file_path)
        elif self.kind == "Image":
            result = image_detect(file=Path(self.file_path).as_posix())
        else:
            result = 0

    if result == -1.0:
        popup.update_message("No face detected")
    else:
        popup.update_message("Fake probability :")
        popup.update_chart(result)
        if result <=0.5 :
            popup.update_explain_message(f"This {self.kind} should be real")
        else:
            popup.update_explain_message(f"This {self.kind} is probably fake")

app = App(_on_file_detection_click=lambda: file_detect(app), _on_live_button_click=lambda: live(app))
app.mainloop()