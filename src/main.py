import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO

class BaixarVideo:
    def __init__(self, link, destination='.'):
        self.link = link
        self.destination = destination
        self.ffmpeg_path = "C:/ffmpeg/bin"  # Verifique se este caminho é válido

    def download_mp4(self):
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio',
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }
                ],
                'ffmpeg_location': self.ffmpeg_path
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link])

            messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso com áudio.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o vídeo: {e}")

    def download_mp3(self):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
                'ffmpeg_location': self.ffmpeg_path
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link])

            messagebox.showinfo("Sucesso", "Áudio baixado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o áudio como MP3: {e}")

    def get_info(self):
        try:
            with YoutubeDL({}) as ydl:
                info = ydl.extract_info(self.link, download=False)
            return {
                'title': info.get('title', 'Título não encontrado'),
                'thumbnail': info.get('thumbnail', '')
            }
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível obter informações do vídeo: {e}")
            return None

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.configure(bg="#f4f4f4")

        # Estilos globais
        label_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10, "bold")

        self.link_label = tk.Label(root, text="Link do vídeo:", font=label_font, bg="#f4f4f4")
        self.link_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.link_entry = tk.Entry(root, width=50)
        self.link_entry.grid(row=0, column=1, padx=5, pady=5)

        self.info_button = tk.Button(root, text="Info", font=button_font, command=self.show_info, bg="#009933", fg="white")
        self.info_button.grid(row=0, column=2, padx=5, pady=5)

        self.dest_label = tk.Label(root, text="Destino:", font=label_font, bg="#f4f4f4")
        self.dest_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.dest_button = tk.Button(root, text="Selecionar Pasta", font=button_font, command=self.select_destination, bg="#2196f3", fg="white")
        self.dest_button.grid(row=1, column=1, padx=5, pady=5)

        self.dest_path = tk.Label(root, text="Diretório atual", fg="#0d47a1", bg="#f4f4f4", font=("Helvetica", 9, "italic"))
        self.dest_path.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.download_mp4_button = tk.Button(root, text="Baixar Vídeo (MP4)", font=button_font, command=self.download_mp4, bg="#ff5722", fg="white")
        self.download_mp4_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.download_mp3_button = tk.Button(root, text="Baixar Áudio (MP3)", font=button_font, command=self.download_mp3, bg="#ff9800", fg="white")
        self.download_mp3_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Frame para exibir informações do vídeo
        self.info_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, bg="#ffffff")
        self.info_frame.grid(row=0, column=3, rowspan=5, padx=10, pady=5, sticky="n")

        self.thumbnail_label = tk.Label(self.info_frame, text="Insira o link do vídeo e clique em info para exibir informações", wraplength=200, font=label_font, bg="#ffffff")
        self.thumbnail_label.pack(pady=5)

        self.default_image = Image.open(BytesIO(requests.get(
            "https://i.ibb.co/5Tv5k3k/Cabe-alho.png"
        ).content)).resize((320, 180), Image.Resampling.LANCZOS)
        self.default_photo = ImageTk.PhotoImage(self.default_image)

        self.thumbnail_image = tk.Label(self.info_frame, image=self.default_photo, bg="#ffffff")
        self.thumbnail_image.image = self.default_photo
        self.thumbnail_image.pack()

        self.destination = '.'

    def select_destination(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination = folder_selected
            self.dest_path.config(text=self.destination)

    def download_mp4(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        downloader = BaixarVideo(link, self.destination)
        downloader.download_mp4()

    def download_mp3(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        downloader = BaixarVideo(link, self.destination)
        downloader.download_mp3()

    def show_info(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        downloader = BaixarVideo(link)
        info = downloader.get_info()
        if info:
            self.thumbnail_label.config(text=info['title'])

            if info['thumbnail']:
                try:
                    response = requests.get(info['thumbnail'], stream=True)
                    if response.status_code == 200:
                        img_data = BytesIO(response.content)
                        img = Image.open(img_data)
                        img = img.resize((320, 180), Image.Resampling.LANCZOS)
                        thumbnail = ImageTk.PhotoImage(img)

                        self.thumbnail_image.config(image=thumbnail)
                        self.thumbnail_image.image = thumbnail
                    else:
                        self.thumbnail_image.config(image=self.default_photo)
                except Exception as e:
                    self.thumbnail_image.config(image=self.default_photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
