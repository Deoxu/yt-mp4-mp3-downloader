import os
from yt_dlp import YoutubeDL

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

            print("Vídeo baixado com sucesso com áudio.")
        except Exception as e:
            print(f"Ocorreu um erro ao baixar o vídeo: {e}")

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

            print("Áudio baixado com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao baixar o áudio como MP3: {e}")

while True:
    print("\nDigite o link do vídeo que deseja baixar ou '0' para sair:")
    link = input(">> ").strip()

    if link == '0':
        print("Saindo do programa. Até mais!")
        break

    print("Escolha o formato de download:")
    print("1. MP4 (vídeo)")
    print("2. MP3 (áudio)")
    option = input("Digite '1' para vídeo ou '2' para áudio: \n>> ").strip()

    destination = input("Digite o destino para salvar o arquivo (deixe em branco para o diretório atual): \n>> ") or '.'

    downloader = BaixarVideo(link, destination)

    if option == '1':
        downloader.download_mp4()
    elif option == '2':
        downloader.download_mp3()
    else:
        print("Opção inválida. Tente novamente.")
