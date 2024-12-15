import os
import asyncio
import threading

import customtkinter
from yt_dlp import YoutubeDL
import customtkinter as ctk
from tkinter import messagebox, font, filedialog
from PIL import Image
import requests
from io import BytesIO
from customtkinter import*



class App:
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

class BaixarVideo:

    def run_in_thread(self, target, *args):
        threading.Thread(target=target, args=args, daemon=True).start()

    def __init__(self, root):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = root
        self.root.title("Shimmer")
        self.root.geometry("1200x300")
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'icon.ico')
        self.root.iconbitmap(icon_path)
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")

        # Configuração do grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Frame esquerdo principal
        self.left_frame = ctk.CTkFrame(root, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.left_frame.grid_rowconfigure((0, 1, 2), weight=1)  # Linhas distribuem o espaço vertical

        # Linha 1: Label, entrada do link e botão Info
        self.link_label = ctk.CTkLabel(self.left_frame, text="Link do vídeo:", font=my_font)
        self.link_label.grid(row=0, column=0, padx=10, sticky="e")

        self.link_entry = ctk.CTkEntry(self.left_frame, corner_radius=30, width=300, height=40, border_color="#581a76")
        self.link_entry.grid(row=0, column=1, columnspan=2, padx=10, sticky="ew")

        self.info_button = ctk.CTkButton(self.left_frame, text="Info", width=110, height=40, corner_radius=50,
                                         fg_color="#581a76", command=self.show_info, font=my_font)
        self.info_button.grid(row=0, column=3, padx=10, sticky="w")

        # Linha 2: Botões Baixar MP3 e MP4 com espaçamento equilibrado
        self.download_mp3_button = ctk.CTkButton(self.left_frame, text="Baixar MP3", width=150, height=40,
                                                 corner_radius=50, fg_color="#581a76", command=self.download_mp3,
                                                 font=my_font)
        self.download_mp3_button.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=5, sticky="e")

        self.download_mp4_button = ctk.CTkButton(self.left_frame, text="Baixar MP4", width=150, height=40,
                                                 corner_radius=50, fg_color="#581a76", command=self.download_mp4,
                                                 font=my_font)
        self.download_mp4_button.grid(row=1, column=2, columnspan=2, padx=(5, 10), pady=5, sticky="w")

        # Linha 3: Botão Selecionar Pasta e label centralizados
        self.dest_button = ctk.CTkButton(self.left_frame, text="Selecionar Pasta", width=150, height=40,
                                         corner_radius=32,
                                         fg_color="#581a76", command=self.select_destination, font=my_font)
        self.dest_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="e")

        self.dest_path = ctk.CTkLabel(self.left_frame, text="Diretório Indefinido", text_color="white")
        self.dest_path.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="w")

        # Frame direito para informações do vídeo
        self.info_frame = ctk.CTkFrame(root, corner_radius=10)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.thumbnail_label = ctk.CTkLabel(self.info_frame, text="Informações do Vídeo", wraplength=200, font=my_font)
        self.thumbnail_label.pack(pady=10)

        # Usando CTkImage para a imagem padrão
        self.default_image = ctk.CTkImage(
            light_image=Image.open(BytesIO(requests.get("https://i.ibb.co/5Tv5k3k/Cabe-alho.png").content)),
            size=(320, 180)
        )

        self.thumbnail_image = ctk.CTkLabel(self.info_frame, image=self.default_image, text="")
        self.thumbnail_image.pack()

        self.destination = '.'

    def select_destination(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination = folder_selected
            self.dest_path.configure(text=self.destination)

    def download_mp4(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        downloader = App(link, self.destination)
        self.run_in_thread(downloader.download_mp4)

    def download_mp3(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        downloader = App(link, self.destination)
        self.run_in_thread(downloader.download_mp3)

    def show_info(self):
        def _downloadinfo():
            link = self.link_entry.get().strip()
            if not link:
                messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
                return

            downloader = App(link)
            info = downloader.get_info()
            if info:
                self.thumbnail_label.configure(text=info['title'])

                if info['thumbnail']:
                    try:
                        response = requests.get(info['thumbnail'], stream=True)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            thumbnail = ctk.CTkImage(light_image=img, size=(320, 180))

                            self.thumbnail_image.configure(image=thumbnail)
                            self.thumbnail_image.image = thumbnail
                        else:
                            self.thumbnail_image.configure(image=self.default_image)
                    except Exception:
                        self.thumbnail_image.configure(image=self.default_image)
        self.run_in_thread(_downloadinfo)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BaixarVideo(root)
    root.mainloop()
