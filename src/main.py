import threading
import customtkinter
import requests
import os
import sys

from yt_dlp import YoutubeDL
import customtkinter as ctk
from tkinter import messagebox, font, filedialog
from PIL import Image
from io import BytesIO
from customtkinter import*

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App:

    def __init__(self, link, destination='.', formatar_nomes=False):
        self.link = link
        self.destination = destination
        self.formatar_nomes = formatar_nomes
        self.ffmpeg_path = "C:\\ffmpeg\\bin"  # Verifique se este caminho é válido
        self.my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")

    def download_mp4(self, progress_bar=None, progress_label=None, progress_window=None):
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")
        try:
            def progress_hook(d):
                if d['status'] == 'downloading' and progress_bar:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', None)
                    progress = downloaded / total if total else 0
                    progress_bar.set(progress)
                    progress_label.configure(text=f"Baixando... {int(progress * 100)}%")
                elif d['status'] == 'finished':
                    progress_label.configure(text="Download concluído, iniciando conversão...")

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [progress_hook]
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.link, download=True)

                if isinstance(info_dict, dict) and 'entries' in info_dict:
                    total_videos = len(info_dict['entries'])
                    downloaded_count = 0
                    for entry in info_dict['entries']:
                        try:
                            if entry is None or 'title' not in entry:
                                raise ValueError("Vídeo indisponível na playlist.")

                            downloaded_file = ydl.prepare_filename(entry)
                            if downloaded_file.endswith(".webm"):
                                self.convert_to_mp4(downloaded_file, progress_bar, progress_label)
                                os.remove(downloaded_file)

                            final_file = downloaded_file.replace(".webm", ".mp4") if downloaded_file.endswith(".webm") else downloaded_file

                            if self.formatar_nomes:
                                novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(final_file))[0], ".mp4")
                                novo_caminho = os.path.join(self.destination, novo_nome)
                                os.rename(final_file, novo_caminho)
                                final_file = novo_caminho

                            downloaded_count += 1
                            progress_label.configure(text=f"Baixando... [{downloaded_count}/{total_videos}]")
                        except ValueError as ve:
                            print(f"Erro: {ve} - Ignorando entrada.")
                        except Exception as e:
                            print(f"Erro ao processar o vídeo da playlist: {e}")
                else:
                    try:
                        if info_dict is None or 'title' not in info_dict or info_dict.get('is_private') or info_dict.get('was_live') or info_dict.get('uploader') is None:
                            raise ValueError("Vídeo indisponível ou não encontrado.")

                        downloaded_file = ydl.prepare_filename(info_dict)
                        if downloaded_file.endswith(".webm"):
                            self.convert_to_mp4(downloaded_file, progress_bar, progress_label)
                            os.remove(downloaded_file)

                        final_file = downloaded_file.replace(".webm", ".mp4") if downloaded_file.endswith(".webm") else downloaded_file

                        if self.formatar_nomes:
                            novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(final_file))[0], ".mp4")
                            novo_caminho = os.path.join(self.destination, novo_nome)
                            os.rename(final_file, novo_caminho)
                            final_file = novo_caminho
                    except ValueError as ve:
                        messagebox.showerror("Erro", f"{ve}")
                        return
                    except Exception as e:
                        print(f"Erro ao processar o vídeo: {e}")

            if not os.path.exists(final_file):
                raise FileNotFoundError(f"O arquivo final {final_file} não foi gerado.")

            if progress_window:
                for widget in progress_window.winfo_children():
                    widget.destroy()
                absolute_path = os.path.abspath(final_file)
                local_path = os.path.dirname(absolute_path)
                progress_label = customtkinter.CTkLabel(
                    progress_window,
                    text=f"Download concluído!\n\nArquivo: {os.path.basename(final_file)}\nLocal: {local_path}",
                    font=my_font,
                    justify="center"
                )
                progress_label.pack(pady=20)

                close_button = customtkinter.CTkButton(
                    progress_window,
                    text="Fechar",
                    command=progress_window.destroy,
                    width=110,
                    height=40,
                    corner_radius=50,
                    fg_color="#c74066",
                    font=my_font,
                    hover_color="#b03558",
                    border_color="#000000",
                    border_width=1
                )
                close_button.pack(pady=10)

        except Exception as e:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar ou converter o vídeo: {e}")

    def download_mp3(self, progress_bar=None, progress_label=None, progress_window=None):
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")
        try:
            def progress_hook(d):
                # Atualiza o progresso do download
                if d['status'] == 'downloading' and progress_bar:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', None)

                    if total and total > 0:  # Verifica se 'total_bytes' é válido
                        progress = downloaded / total
                    else:
                        progress = 0  # Define progresso como 0 se não for possível calcular

                    progress_bar.set(progress)
                    progress_label.configure(text=f"Baixando... {int(progress * 100)}%", font=my_font)

                # Indica que o download foi finalizado
                elif d['status'] == 'finished':
                    progress_label.configure(text="Download concluído!", font=my_font)

            ydl_opts = {
                'format': 'bestaudio/best',  # Obtém o melhor áudio disponível
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [progress_hook]
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.link, download=True)

                # Processa os nomes dos arquivos baixados
                if isinstance(info_dict, dict) and 'entries' in info_dict:
                    # É uma playlist
                    total_videos = len(info_dict['entries'])
                    downloaded_count = 0
                    for entry in info_dict['entries']:
                        try:
                            if entry is None or 'title' not in entry:
                                raise ValueError("Vídeo indisponível na playlist.")

                            downloaded_file = ydl.prepare_filename(entry).replace(".webm", ".mp3")
                            final_file = downloaded_file
                            if self.formatar_nomes:
                                novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(downloaded_file))[0],
                                                               ".mp3")
                                novo_caminho = os.path.join(self.destination, novo_nome)
                                os.rename(downloaded_file, novo_caminho)
                                final_file = novo_caminho

                            downloaded_count += 1
                            progress_label.configure(text=f"Baixando... [{downloaded_count}/{total_videos}]", font=my_font)
                        except ValueError as ve:
                            print(f"Erro: {ve} - Ignorando entrada.")
                        except Exception as e:
                            print(f"Erro ao processar o vídeo da playlist: {e}")
                else:
                    try:
                        if info_dict is None or 'title' not in info_dict or info_dict.get('is_private') or info_dict.get('was_live') or info_dict.get('uploader') is None:
                            raise ValueError("Vídeo indisponível ou não encontrado.")

                        downloaded_file = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")
                        final_file = downloaded_file
                        if self.formatar_nomes:
                            novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(downloaded_file))[0], ".mp3")
                            novo_caminho = os.path.join(self.destination, novo_nome)
                            os.rename(downloaded_file, novo_caminho)
                            final_file = novo_caminho
                    except ValueError as ve:
                        messagebox.showerror("Erro", f"{ve}")
                        return
                    except Exception as e:
                        print(f"Erro ao processar o vídeo: {e}")

            if progress_window:
                for widget in progress_window.winfo_children():
                    widget.destroy()
                absolute_path = os.path.abspath(final_file)
                local_path = os.path.dirname(absolute_path)
                progress_label = customtkinter.CTkLabel(
                    progress_window,
                    text=f"Download concluído!\n\nArquivo: {os.path.basename(final_file)}\nLocal: {local_path}",
                    font=my_font,
                    justify="center"
                )
                progress_label.pack(pady=20)

                close_button = customtkinter.CTkButton(
                    progress_window,
                    text="Fechar",
                    command=progress_window.destroy,
                    width=110,
                    height=40,
                    corner_radius=50,
                    fg_color="#c74066",
                    font=my_font,
                    hover_color="#b03558",
                    border_color="#000000",
                    border_width=1
                )
                close_button.pack(pady=10)

        except Exception as e:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o áudio: {e}")


    def convert_to_mp4(self, input_file, progress_bar=None, progress_label=None):
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")
        import subprocess
        import re

        output_file = input_file.replace(".webm", ".mp4")
        progress_bar.set(0)  # Reinicia o progresso para a conversão
        progress_label.configure(text="Convertendo vídeo...")

        command = [
            os.path.join(self.ffmpeg_path, "ffmpeg"), "-y", "-i", input_file,
            "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", output_file
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        progress_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

        for line in process.stderr:
            match = progress_pattern.search(line)
            if match:
                hours, minutes, seconds = map(float, match.groups())
                total_seconds = hours * 3600 + minutes * 60 + seconds
                progress = min(1, total_seconds / 300)  # Ajuste para estimativa de tempo total
                progress_bar.set(progress)
                progress_label.configure(text=f"Convertendo... {int(progress * 100)}%", font= my_font)

        process.wait()

        if process.returncode == 0:
            progress_label.configure(text="Conversão concluída!", font= my_font)
        else:
            progress_label.configure(text="Erro na conversão.", font= my_font)
            messagebox.showerror("Erro", "Houve um problema durante a conversão do vídeo.")

    def formatar_nome(self, nome_original, extensao=".mp3"):
        """Formata o nome mantendo espaços entre palavras, mas adicionando um traço direto entre o número e o nome."""
        import re

        # Remove caracteres especiais, mas mantém espaços e hifens
        nome_formatado = ''.join(c for c in nome_original if c.isalnum() or c in (' ', '-')).strip()

        # Listar todos os arquivos no diretório de destino
        arquivos_existentes = os.listdir(self.destination)

        # Identificar a maior numeração existente independentemente da extensão
        maior_numero = 0
        padrao = re.compile(r"^(\d{2})-")  # Padrão para encontrar números no início do nome

        for arquivo in arquivos_existentes:
            match = padrao.match(arquivo)
            if match:
                numero = int(match.group(1))
                maior_numero = max(maior_numero, numero)

        # Incrementar a maior numeração encontrada
        novo_numero = maior_numero + 1

        while True:
            nome_completo = f"{novo_numero:02d}-{nome_formatado}{extensao}"
            if not os.path.exists(os.path.join(self.destination, nome_completo)):
                return nome_completo
            novo_numero += 1

    def download_mp3(self, progress_bar=None, progress_label=None, progress_window=None):
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")
        try:
            def progress_hook(d):
                # Atualiza o progresso do download
                if d['status'] == 'downloading' and progress_bar:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', None)

                    if total and total > 0:  # Verifica se 'total_bytes' é válido
                        progress = downloaded / total
                    else:
                        progress = 0  # Define progresso como 0 se não for possível calcular

                    progress_bar.set(progress)
                    progress_label.configure(text=f"Baixando... {int(progress * 100)}%", font=my_font)

                # Indica que o download foi finalizado
                elif d['status'] == 'finished':
                    progress_label.configure(text="Download concluído!", font=my_font)

            ydl_opts = {
                'format': 'bestaudio/best',  # Obtém o melhor áudio disponível
                'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [progress_hook]
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.link, download=True)

                # Processa os nomes dos arquivos baixados
                if isinstance(info_dict, dict) and 'entries' in info_dict:
                    # É uma playlist
                    total_videos = len(info_dict['entries'])
                    downloaded_count = 0
                    for entry in info_dict['entries']:
                        try:
                            if entry is None or 'title' not in entry:
                                raise ValueError("Vídeo indisponível na playlist.")

                            downloaded_file = ydl.prepare_filename(entry).replace(".webm", ".mp3")
                            final_file = downloaded_file
                            if self.formatar_nomes:
                                novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(downloaded_file))[0],
                                                               ".mp3")
                                novo_caminho = os.path.join(self.destination, novo_nome)
                                os.rename(downloaded_file, novo_caminho)
                                final_file = novo_caminho

                            downloaded_count += 1
                            progress_label.configure(text=f"Baixando... [{downloaded_count}/{total_videos}]", font=my_font)
                        except ValueError as ve:
                            print(f"Erro: {ve} - Ignorando entrada.")
                        except Exception as e:
                            print(f"Erro ao processar o vídeo da playlist: {e}")
                else:
                    try:
                        if info_dict is None or 'title' not in info_dict or info_dict.get('is_private') or info_dict.get('was_live') or info_dict.get('uploader') is None:
                            raise ValueError("Vídeo indisponível ou não encontrado.")

                        downloaded_file = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")
                        final_file = downloaded_file
                        if self.formatar_nomes:
                            novo_nome = self.formatar_nome(os.path.splitext(os.path.basename(downloaded_file))[0], ".mp3")
                            novo_caminho = os.path.join(self.destination, novo_nome)
                            os.rename(downloaded_file, novo_caminho)
                            final_file = novo_caminho
                    except ValueError as ve:
                        messagebox.showerror("Erro", f"{ve}")
                        return
                    except Exception as e:
                        print(f"Erro ao processar o vídeo: {e}")

            if progress_window:
                for widget in progress_window.winfo_children():
                    widget.destroy()
                absolute_path = os.path.abspath(final_file)
                local_path = os.path.dirname(absolute_path)
                progress_label = ctk.CTkLabel(
                    progress_window,
                    text=f"Download concluído!\n\nArquivo: {os.path.basename(final_file)}\nLocal: {local_path}",
                    font=my_font,
                    justify="center"
                )
                progress_label.pack(pady=20)

                close_button = ctk.CTkButton(
                    progress_window,
                    text="Fechar",
                    command=progress_window.destroy,
                    width=110,
                    height=40,
                    corner_radius=50,
                    fg_color="#c74066",
                    font=my_font,
                    hover_color="#b03558",
                    border_color="#000000",
                    border_width=1
                )
                close_button.pack(pady=10)

        except Exception as e:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o áudio: {e}")

    def get_info(self):
        try:
            with YoutubeDL({}) as ydl:
                info = ydl.extract_info(self.link, download=False)
            return {
                'title': info.get('title', 'Título não encontrado'),
                'thumbnail': info.get('thumbnail', ''),

                'duration': info.get('duration', 0),

                'channel': info.get('channel', 'Canal não encontrado'),

                'description': info.get('description', 'Descrição não encontrada')
            }
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível obter informações do vídeo: {e}")
            return None

class BaixarVideo:


    def show_progress_window(self):
        my_font = customtkinter.CTkFont(family="Segoe UI", size=14, weight="bold")
        # Criação de uma nova janela para exibir a barra de progresso
        self.progress_window = ctk.CTkToplevel(self.root)
        self.progress_window.title("Progresso do Download")
        self.progress_window.geometry("650x200")
        self.progress_window.resizable(False, False)

        # Configurando a janela de progresso para ficar sempre no topo
        self.progress_window.attributes("-topmost", True)

        # Adicionando a barra de progresso
        self.progress_label = ctk.CTkLabel(self.progress_window, text="Iniciando download...", font= my_font)
        self.progress_label.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.progress_window, width=300, height=30, corner_radius=20, border_color = "#000000", border_width = 3,progress_color = "#c74066", fg_color= "#000000")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

    def run_in_thread(self, target, *args):
        threading.Thread(target=target, args=args, daemon=True).start()

    def __init__(self, root):
        ctk.set_appearance_mode("dark")
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("1100x440")
        self.destination = '.'
        self.formatar_nomes = customtkinter.BooleanVar(value=False)
        icon_path = resource_path(os.path.join('images', 'icon.ico'))
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
        self.left_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Linha 1: Label, entrada do link e botão Info
        self.link_label = ctk.CTkLabel(self.left_frame, text="Link do vídeo:", font=my_font)
        self.link_label.grid(row=0, column=0, padx=5, sticky="e")

        self.checkbox_tooltip_label = ctk.CTkLabel(self.left_frame, text="*", text_color="#c74066", cursor="hand2")
        self.checkbox_tooltip_label.grid(row=0, column=1, sticky="w", padx=0)
        self.checkbox_tooltip_label.bind("<Enter>", lambda e: self.show_tooltip(e,
                                                                                "Links suportados:\n- URL de um único vídeo.\n- URL de uma playlist completa.",
                                                                                x_offset=-120, y_offset=30))
        self.checkbox_tooltip_label.bind("<Leave>", self.hide_tooltip)


        self.link_entry = ctk.CTkEntry(self.left_frame, corner_radius=30, width=300, height=40, border_color="#c74066")
        self.link_entry.grid(row=0, column=1, columnspan=2, padx=10, sticky="ew")

        self.info_button = ctk.CTkButton(self.left_frame, text="Info", width=110, height=40, corner_radius=50,
                                         fg_color="#c74066", command=self.show_info, font=my_font,
                                         hover_color="#b03558",
                                         border_color="#000000", border_width=2)
        self.info_button.grid(row=0, column=3, padx=10, sticky="w")

        # Linha 2: Botões de download
        self.download_mp3_button = ctk.CTkButton(self.left_frame, text="Baixar MP3", width=150, height=40,
                                                 corner_radius=50, fg_color="#c74066", command=self.download_mp3,
                                                 font=my_font, hover_color="#b03558", border_color="#000000",
                                                 border_width=2)
        self.download_mp3_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        self.download_mp4_button = ctk.CTkButton(self.left_frame, text="Baixar MP4", width=150, height=40,
                                                 corner_radius=50, fg_color="#c74066", command=self.download_mp4,
                                                 font=my_font, hover_color="#b03558", border_color="#000000",
                                                 border_width=2)
        self.download_mp4_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Linha 3: Checkbox com o asterisco ao lado
        self.checkbox_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.checkbox_frame.grid(row=2, column=1, columnspan=2, pady=(5, 0), sticky="n")

        self.checkbox = customtkinter.CTkCheckBox(
            self.checkbox_frame,
            text="Formatar nomes automaticamente",
            variable=self.formatar_nomes,
            command=self.toggle_format_names,
            fg_color="#c75979",
            hover_color="#c74066",
            text_color="white",
            checkmark_color="white"
        )
        self.checkbox.grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.tooltip_label = ctk.CTkLabel(self.checkbox_frame, text="*", text_color="#c74066", cursor="hand2")
        self.tooltip_label.grid(row=0, column=1, sticky="w", padx=1)
        self.tooltip_label.bind("<Enter>", lambda e: self.show_tooltip(e,
                                                                       "Ativar esta opção irá:\n- Adicionar uma numeração ao nome do arquivo.\n- Remover caracteres especiais automaticamente.",
                                                                       x_offset=-180, y_offset=30))
        self.tooltip_label.bind("<Leave>", self.hide_tooltip)

        # Linha 4: Botão Selecionar Pasta
        self.dest_button = ctk.CTkButton(self.left_frame, text="Selecionar Pasta", width=150, height=40,
                                         corner_radius=32, fg_color="#c74066", command=self.select_destination,
                                         font=my_font, hover_color="#b03558", border_color="#000000", border_width=2)
        self.dest_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="e")

        self.dest_path = ctk.CTkLabel(self.left_frame,
                                      text="Diretório Indefinido",
                                      text_color="white")
        self.dest_path.grid(row=3, column=2, columnspan=2, padx=20, pady=5, sticky="w")
        #Tooltip
        self.tooltip_label = ctk.CTkLabel(self.left_frame, text="*", text_color="#c74066", cursor="hand2")
        self.tooltip_label.grid(row=3, column=2, columnspan =2, sticky="w", padx=10, pady=5)
        self.tooltip_label.bind("<Enter>", lambda e: self.show_tooltip(e,
                                                                           "Ao clicar no botão:\n- Altera o diretório em que o arquivo será baixado\n- Caso não selecione um, irá para o diretório padrão do programa.",
                                                                       x_offset=-180, y_offset=-70))
        self.tooltip_label.bind("<Leave>", self.hide_tooltip)

        # Frame direito para informações do vídeo
        self.info_frame = ctk.CTkFrame(root, corner_radius=10)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.thumbnail_label = ctk.CTkLabel(self.info_frame, text="Informações do Vídeo", wraplength=200, font=my_font)
        self.thumbnail_label.pack(pady=10)

        # Usando CTkImage para a imagem padrão
        image_path = resource_path(os.path.join('images', 'infoimg.png'))
        self.default_image = ctk.CTkImage(
            light_image=Image.open(image_path),
            size=(320, 180)
        )

        self.thumbnail_image = ctk.CTkLabel(self.info_frame, image=self.default_image, text="")
        self.info_details = ctk.CTkLabel(self.info_frame, text="", wraplength=350, justify="left",
                                         font=my_font)
        self.info_details.pack(pady=10)
        self.thumbnail_image.pack()
        self.tooltip = None
        self.destination = '.'

    def show_tooltip(self, event, text, x_offset=-120, y_offset=25):
        if self.tooltip is None:
            # Criar a tooltip como um label estilizado
            self.tooltip = ctk.CTkLabel(
                self.left_frame,
                text=text,
                text_color="white",
                fg_color="#c74066",
                corner_radius=30,
                justify="center",
                width=350,
                height=55,
            )

            self.tooltip.update_idletasks()
            self.tooltip.place(
                x=event.x_root - self.left_frame.winfo_rootx() - self.tooltip.winfo_width() + x_offset,
                y=event.y_root - self.left_frame.winfo_rooty() + y_offset
            )
            self.tooltip.lift()

    def hide_tooltip(self, event):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

    def toggle_format_names(self):
        if self.formatar_nomes.get():
            print("Formatação de nomes ativada. Os arquivos serão renomeados ao serem baixados.")
        else:
            print("Formatação de nomes desativada. Os arquivos manterão seus nomes originais.")

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

        self.show_progress_window()  # Mostra a janela de progresso
        downloader = App(link, self.destination, formatar_nomes=self.formatar_nomes.get())
        print(f"Formatar nomes: {downloader.formatar_nomes}")
        self.run_in_thread(downloader.download_mp4, self.progress_bar, self.progress_label, self.progress_window)

    def download_mp3(self):
        link = self.link_entry.get().strip()
        if not link:
            messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
            return

        self.show_progress_window()  # Mostra a janela de progresso
        downloader = App(link, self.destination, formatar_nomes=self.formatar_nomes.get())
        print(f"Formatar nomes: {downloader.formatar_nomes}")  # Confirme o estado aqui
        self.run_in_thread(downloader.download_mp3, self.progress_bar, self.progress_label, self.progress_window)

    def show_info(self):
        def _downloadinfo():
            link = self.link_entry.get().strip()
            if not link:
                messagebox.showwarning("Atenção", "Por favor, insira o link do vídeo.")
                return

            downloader = App(link)
            info = downloader.get_info()
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            if info:
                self.thumbnail_label.configure(text=info['title'])
                details = (f"Duração: {minutes}:{seconds:02}\n"

                           f"Canal: {info['channel']}\n"

                           f"Descrição:\n{info['description'][:70]}...")

                self.info_details.configure(text=details)
            if info['thumbnail']:
                    try:
                        response = requests.get(info['thumbnail'], stream=True)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            thumbnail = ctk.CTkImage(light_image=img,size=(320, 180))

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
