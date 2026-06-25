#!/usr/bin/env python3
"""YouTube Downloader GUI - Download videos/audio from YouTube.
Price: $25"""
import tkinter as tk, subprocess, threading
def download():
    url = url_entry.get()
    def d():
        subprocess.run(["yt-dlp", "-f", "best", "-o", "%(title)s.%(ext)s", url])
        status_label.config(text="Done!")
    threading.Thread(target=d).start()
    status_label.config(text="Downloading...")
root = tk.Tk(); root.title("YouTube Downloader"); root.geometry("400x150")
tk.Label(root, text="URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50); url_entry.pack()
tk.Button(root, text="Download", command=download).pack(pady=10)
status_label = tk.Label(root, text=""); status_label.pack()
root.mainloop()
