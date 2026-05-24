import threading
import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x500")

        self.download_path = ""

        title = ctk.CTkLabel(
            root,
            text="YouTube Video Downloader",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.url_entry = ctk.CTkEntry(
            root,
            width=500,
            height=40,
            placeholder_text="لینک ویدیو یوتیوب را وارد کن"
        )
        self.url_entry.pack(pady=10)

        self.quality_option = ctk.CTkOptionMenu(
            root,
            values=["best", "720p", "480p", "audio"]
        )
        self.quality_option.pack(pady=10)

        self.path_button = ctk.CTkButton(
            root,
            text="انتخاب پوشه دانلود",
            command=self.choose_folder
        )
        self.path_button.pack(pady=10)

        self.path_label = ctk.CTkLabel(root, text="پوشه انتخاب نشده")
        self.path_label.pack()

        self.progress = ctk.CTkProgressBar(root, width=500)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.status_label = ctk.CTkLabel(root, text="آماده دانلود")
        self.status_label.pack(pady=10)

        self.download_button = ctk.CTkButton(
            root,
            text="شروع دانلود",
            height=45,
            command=self.start_download
        )
        self.download_button.pack(pady=20)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_label.configure(text=folder)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            percent = percent_str.replace('%', '').strip()

            try:
                percent_float = float(percent)
                self.progress.set(percent_float / 100)
            except:
                pass

            speed = d.get('_speed_str', '---')
            eta = d.get('_eta_str', '---')

            self.status_label.configure(
                text=f"در حال دانلود: {percent_str} | سرعت: {speed} | زمان باقی‌مانده: {eta}"
            )

        elif d['status'] == 'finished':
            self.progress.set(1)
            self.status_label.configure(text="دانلود کامل شد ✅")

    def download_video(self):
        url = self.url_entry.get()
        quality = self.quality_option.get()

        if quality == "best":
            format_type = "best"
        elif quality == "720p":
            format_type = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "480p":
            format_type = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:
            format_type = "bestaudio"

        ydl_opts = {
            'format': format_type,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'merge_output_format': 'mp4',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            self.status_label.configure(text=f"خطا: {e}")

    def start_download(self):
        threading.Thread(target=self.download_video).start()


root = ctk.CTk()
app = YouTubeDownloaderApp(root)
root.mainloop()