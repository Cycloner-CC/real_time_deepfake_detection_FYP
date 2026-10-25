import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path


BG       = "#070B14"
CARD     = "#0F1623"
CARD2    = "#141C2B"
CARD3    = "#1A2438"
BORDER   = "#1E2A3A"
ACCENT   = "#3B82F6"
ACCENT_H = "#2563EB"
CYAN     = "#22D3EE"
GREEN    = "#34D399"
AMBER    = "#FBBF24"
RED      = "#F87171"
TEXT     = "#F1F5F9"
MUTED    = "#94A3B8"
DIM      = "#64748B"
SOFT     = "#475569"

AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


class App(ctk.CTk):
    def __init__(self,_on_file_detection_click,_on_live_button_click) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Deepfake Detection  ·  FYP Demo")
        self.geometry("420x620")
        self.minsize(360, 520)
        self.configure(fg_color=BG)

        self.stop_live_signal = threading.Event()
        self._on_file_detection_click = _on_file_detection_click
        self._on_live_button_click = _on_live_button_click
        self.file_path = None
        self._history: list[str] = []
        self._live_running = False
        self._mode = "file"
        self._train_running = False
        self._train_thread = None

        self._build()
        # self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _card(self, parent, **kw):
        return ctk.CTkFrame(
            parent, fg_color=CARD, corner_radius=14,
            border_width=1, border_color=BORDER, **kw
        )

    def _section(self, parent, text: str):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=11, weight="bold"), text_color=CYAN
        )

    def _build(self) -> None:
        self._build_topbar()
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(10, 16))

        left = self._card(body, width=340)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.pack_propagate(False)
        self._build_left(left)

        right = ctk.CTkFrame(body, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

    def _build_topbar(self) -> None:
        top = ctk.CTkFrame(self, fg_color="#0A101C", corner_radius=0, height=58)
        top.pack(fill="x")
        top.pack_propagate(False)

        brand = ctk.CTkFrame(top, fg_color="transparent")
        brand.pack(side="left", padx=22, pady=12)
        ctk.CTkLabel(
            brand, text="  Deepfake Detection",
            font=ctk.CTkFont(size=16), text_color=CYAN
        ).pack(side="left")


    def _build_left(self, left) -> None:
        self._section(left, "MODE").pack(anchor="w", padx=18, pady=(16, 6))
        mode_row = ctk.CTkFrame(left, fg_color="transparent")
        mode_row.pack(fill="x", padx=16, pady=(0, 10))

        self.btn_file = ctk.CTkButton(
            mode_row, text="📁  File", height=34, corner_radius=9,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._set_mode("file"),
        )
        self.btn_file.pack(side="left", expand=True, fill="x", padx=(0, 4))

        self.btn_live = ctk.CTkButton(
            mode_row, text="🔴  Live", height=34, corner_radius=9,
            fg_color=CARD3, hover_color="#243044",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._set_mode("live"),
        )
        self.btn_live.pack(side="left", expand=True, fill="x", padx=(4, 0))

        # File panel
        self.file_panel = ctk.CTkFrame(left, fg_color="transparent")
        self.file_panel.pack(fill="x")

        self._section(self.file_panel, "INPUT MEDIA").pack(anchor="w", padx=18, pady=(6, 2))
        ctk.CTkLabel(
            self.file_panel, text="Upload audio / video / image",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(0, 8))

        drop = ctk.CTkFrame(
            self.file_panel, fg_color=CARD2, corner_radius=11,
            border_width=1, border_color="#2A3A4F", height=90
        )
        drop.pack(fill="x", padx=14, pady=2)
        drop.pack_propagate(False)

        self.path_var = ctk.StringVar(value="No file selected")
        ctk.CTkLabel(
            drop, textvariable=self.path_var,
            font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT
        ).pack(anchor="w", padx=12, pady=(16, 2))
        self.meta_var = ctk.StringVar(value="Supported: wav · mp3 · mp4 · jpg …")
        ctk.CTkLabel(
            drop, textvariable=self.meta_var,
            font=ctk.CTkFont(size=11), text_color=DIM
        ).pack(anchor="w", padx=12)

        ctk.CTkButton(
            self.file_panel, text="Browse file…", height=36, corner_radius=9,
            fg_color=CARD3, hover_color="#243044",
            border_width=1, border_color="#334155",
            command=self._browse,
        ).pack(fill="x", padx=14, pady=(10, 4))

        self.run_btn = ctk.CTkButton(
            self.file_panel, text="▶   Run Detection", height=42, corner_radius=9,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_file_detection_click,
        )
        self.run_btn.pack(fill="x", padx=14, pady=(4, 6))

        # Live panel
        self.live_panel = ctk.CTkFrame(left, fg_color="transparent")

        self._section(self.live_panel, "LIVE CAPTURE").pack(anchor="w", padx=18, pady=(6, 2))
        ctk.CTkLabel(
            self.live_panel, text="Monitor (Zoom / Teams)",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(0, 8))

        # ctk.CTkLabel(
        #     self.live_panel, text="Source",
        #     font=ctk.CTkFont(size=11), text_color=DIM
        # ).pack(anchor="w", padx=18)
        # self.live_source = ctk.CTkSegmentedButton(
        #     self.live_panel,
        #     values=["Webcam", "Screen"],
        #     font=ctk.CTkFont(size=12),
        #     selected_color=ACCENT, selected_hover_color=ACCENT_H,
        #     unselected_color=CARD3, unselected_hover_color="#243044",
        #     command=self._on_live_source_change,
        # )
        # self.live_source.set("Screen")
        # self.live_source.pack(fill="x", padx=14, pady=(2, 8))

        # ctk.CTkLabel(
        #     self.live_panel, text="Device / Monitor",
        #     font=ctk.CTkFont(size=11), text_color=DIM
        # ).pack(anchor="w", padx=18)
        # self.device_var = ctk.StringVar(value="1 (Primary)")
        # self.device_menu = ctk.CTkOptionMenu(
        #     self.live_panel, variable=self.device_var,
        #     values=["1 (Primary)"],
        #     fg_color=CARD3, button_color=CARD3, button_hover_color="#243044",
        #     font=ctk.CTkFont(size=12),
        # )
        # self.device_menu.pack(fill="x", padx=14, pady=(2, 8))

        self.live_btn = ctk.CTkButton(
            self.live_panel, text="●  Start Live Monitoring", height=42,
            corner_radius=9, fg_color=RED, hover_color="#DC2626",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_live_button_click,
        )
        self.live_btn.pack(fill="x", padx=14, pady=(6, 4))

        ctk.CTkLabel(
            self.live_panel,
            text="Tip: Open Zoom/Teams → choose Screen → select the\n"
                 "monitor showing the meeting. Frames are sampled & scored.",
            font=ctk.CTkFont(size=10), text_color=SOFT, justify="left",
        ).pack(anchor="w", padx=16, pady=(6, 4))

        # Shared progress / status
        self.progress = ctk.CTkProgressBar(
            left, height=5, corner_radius=3, progress_color=CYAN
        )
        self.progress.set(0)
        self.progress.pack(fill="x", padx=14, pady=(10, 4))

        self.status_var = ctk.StringVar(value="Ready — choose File or Live mode")
        ctk.CTkLabel(
            left, textvariable=self.status_var,
            font=ctk.CTkFont(size=11), text_color=DIM
        ).pack(anchor="w", padx=18, pady=(2, 6))

    def _set_mode(self, mode: str) -> None:
            if mode == self._mode:
                return
            if self._live_running:
                self.stop_live_signal.set()
                self._live_running = False
                self.live_btn.configure(text="●  Start Live Monitoring",
                                        fg_color="#F87171", hover_color="#DC2626")
            self._mode = mode
            if mode == "file":
                self.btn_file.configure(fg_color=ACCENT, hover_color=ACCENT_H)
                self.btn_live.configure(fg_color=CARD3, hover_color="#243044")
                self.live_panel.pack_forget()
                self.file_panel.pack(fill="x")
                self.status_var.set("File mode — select a media file")
            else:
                self.btn_live.configure(fg_color=ACCENT, hover_color=ACCENT_H)
                self.btn_file.configure(fg_color=CARD3, hover_color="#243044")
                self.file_panel.pack_forget()
                self.live_panel.pack(fill="x")
                # self._refresh_devices()
                self.status_var.set("Live mode — choose source & start monitoring")

    def _browse(self) -> None:
            path = filedialog.askopenfilename(
                title="Select media file",
                filetypes=[
                    ("Media",
                        "*.mp4 *.avi *.mov *.mkv *.webm *.wav *.mp3 *.flac *.ogg *.m4a "
                        "*.jpg *.jpeg *.png *.bmp *.webp"),
                    ("All", "*.*"),
                ],
            )
            if not path:
                return
            self.file_path = Path(path)
            self.path_var.set(self.file_path.name)
            size_mb = self.file_path.stat().st_size / (1024 * 1024)
            ext = self.file_path.suffix.lower()
            self.kind = ("Audio" if ext in AUDIO_EXTS else
                         "Video" if ext in VIDEO_EXTS else
                         "Image" if ext in IMAGE_EXTS else "File")
            self.meta_var.set(f"{self.kind}  ·  {size_mb:.2f} MB  ·  {ext}")
            self.status_var.set("File loaded — press Run Detection")


