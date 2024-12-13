# Sobre

Estou desenvolvendo essa aplicação para aprender mais sobre Python e ajudar pessoas que necessitam de um aplicativo para baixar músicas ou vídeos, sem a inconveniência de múltiplos pop-ups.

## Instruções de Utilização

1. Certifique-se de que o [FFmpeg](https://www.ffmpeg.org/download.html) está baixado e localizado na raiz do seu HD (ex.: `C:\`). Clique [aqui](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) para fazer o download.

2. Para rodar o código da aplicação em sua IDE favorita, instale as seguintes bibliotecas:

   - **yt_dlp**  
     ```bash
     pip install yt_dlp
     ```

   - **requests**  
     ```bash
     pip install requests
     ```

   - **pillow**  
     ```bash
     pip install pillow
     ```

3. Após instalar todas as dependências necessárias, inicialize a aplicação.

4. **Utilização da aplicação**:
   - Insira o link do vídeo que deseja baixar.
   - Escolha entre as opções disponíveis:
     - **MP4**: Baixar o vídeo completo.
     - **MP3**: Extrair o áudio do vídeo.
   - Você será solicitado a selecionar um diretório para salvar o arquivo. Caso não escolha, o arquivo será salvo no diretório atual.
