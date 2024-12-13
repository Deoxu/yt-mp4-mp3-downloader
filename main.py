import os
import subprocess
from yt_dlp import YoutubeDL

class BaixarVideo:
    def __init__(self, link, destination='.'):
        self.link = link
        self.destination = destination
        self.ffmpeg_path = "C:/ffmpeg/bin"

    def download_mp4(self):
        """Baixar o vídeo em formato MP4"""
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ffmpeg_location': self.ffmpeg_path
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link])

            print("Vídeo baixado com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro ao baixar o vídeo como MP4: {e}")

    def download_mp3(self):
        """Baixar apenas o áudio em formato MP3"""
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

            print("Áudio baixado com sucesso como MP3!")
        except Exception as e:
            print(f"Ocorreu um erro ao baixar o áudio como MP3: {e}")

# Entrada do usuário
link = input("Digite o link do vídeo que deseja baixar: \n>> ")
print("Escolha o formato de download:")
print("1. MP4 (vídeo)")
print("2. MP3 (áudio)")
option = input("Digite '1' para vídeo ou '2' para áudio: \n>> ").strip().lower()

destination = input("Digite o destino para salvar o arquivo (deixe em branco para o diretório atual): \n>> ") or '.'

# Instanciando a classe
downloader = BaixarVideo(link, destination)

if option == '1':
    downloader.download_mp4()
elif option == '2':
    downloader.download_mp3()
else:
    print("Opção inválida.")
