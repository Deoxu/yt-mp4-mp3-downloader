# Sobre

Estou desenvolvendo essa aplicação para aprender mais sobre Python e ajudar pessoas que necessitam de um aplicativo para baixar músicas ou vídeos, sem a inconveniência de múltiplos pop-ups.

## Instruções de Utilização

1. Certifique-se de que o [FFmpeg](https://www.ffmpeg.org/download.html) está baixado e localizado na raiz do seu HD (ex.: `C:\`). Clique [aqui](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) para fazer o download.

2. Adicione o caminho onde o FFmpeg está instalado ao PATH do sistema:
   - No Windows:
     1. Abra o **Menu Iniciar** e procure por "Editar variáveis de ambiente do sistema".
     2. Na janela "Propriedades do Sistema", clique em **Variáveis de Ambiente**.
     3. Na seção **Variáveis do sistema**, encontre a variável `Path` e clique em **Editar**.
     4. Clique em **Novo** e insira o caminho completo do diretório onde o FFmpeg está localizado (ex.: `C:\ffmpeg\bin`).
     5. Clique em **OK** para salvar as alterações.
   - No macOS/Linux:
     1. Abra o terminal e edite o arquivo de configuração do shell (ex.: `~/.bashrc`, `~/.zshrc`, ou `~/.bash_profile`).
     2. Adicione a seguinte linha:  
        ```bash
        export PATH="$PATH:/caminho/para/ffmpeg/bin"
        ```
     3. Salve o arquivo e recarregue o shell com:  
        ```bash
        source ~/.bashrc
        ```

3. Para rodar o código da aplicação em sua IDE favorita, instale as seguintes bibliotecas:

- **yt_dlp**  
  ```bash
  pip install yt_dlp
  ```

- **requests**  
  ```bash
  pip install requests
  ```
  
- **custom tkinter**  
  ```bash
  pip install customtkinter
  ```

- **pillow**  
  ```bash
  pip install pillow
  ```

4. Após instalar todas as dependências necessárias, inicialize a aplicação.

5. **Utilização da aplicação**:
   - Insira o link do vídeo que deseja baixar.
   - Escolha entre as opções disponíveis:
     - **MP4**: Baixar o vídeo completo.
     - **MP3**: Extrair o áudio do vídeo.
   - Você será solicitado a selecionar um diretório para salvar o arquivo. Caso não escolha, o arquivo será salvo no diretório atual.
