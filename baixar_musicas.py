import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Erro: A biblioteca 'yt-dlp' não está instalada.")
    print("Por favor, instale executando: pip install yt-dlp")
    sys.exit(1)

def download_music(links_file='links.txt', output_folder='musicas_baixadas'):
    # Cria a pasta de destino se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta '{output_folder}' criada.")

    # Verifica se o arquivo de links existe
    if not os.path.exists(links_file):
        print(f"Erro: O arquivo '{links_file}' não foi encontrado.")
        print("Criando um arquivo 'links.txt' vazio para você.")
        with open(links_file, 'w', encoding='utf-8') as f:
            pass
        print("Coloque seus links dentro do arquivo 'links.txt' e execute o script novamente.")
        return

    # Lê os links do arquivo
    with open(links_file, 'r', encoding='utf-8') as f:
        # Pega as linhas, ignora vazias e comentários
        links = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    if not links:
        print(f"O arquivo '{links_file}' está vazio. Adicione os links e tente novamente.")
        return

    print(f"Encontrados {len(links)} links para baixar.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'ffmpeg_location': os.path.dirname(os.path.abspath(__file__)),
        'quiet': False,
        'no_warnings': True,
        'ignoreerrors': True, # Se der erro em um vídeo, continua pro próximo
        'noplaylist': True,   # Baixa apenas o vídeo, ignora a playlist
        'retries': 15,        # Tenta novamente em caso de falha de conexão
        'fragment_retries': 15, # Tenta novamente baixar os "pedaços" do vídeo se falharem
        'socket_timeout': 15, # Cancela e tenta novamente se a conexão ficar parada
        'http_chunk_size': 10485760, # Ajuda a driblar limitações de bloqueio do YouTube (10mb por vez)
        'sleep_interval': 5,  # Impede sua internet de dar 'getaddrinfo failed' (queda de DNS) por causa de acessos muito rápidos!
        'max_sleep_interval': 12, # Tempo máximo de espera aleatório entre um vídeo e outro.
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, link in enumerate(links, 1):
            print(f"\n{'='*50}")
            print(f"[{i}/{len(links)}] Processando: {link}")
            print(f"{'='*50}")
            try:
                ydl.download([link])
            except Exception as e:
                print(f"Erro ao tentar baixar {link}: {e}")

    print("\n" + "="*50)
    print("Processo finalizado! Suas músicas estão na pasta:", os.path.abspath(output_folder))
    print("="*50)

if __name__ == "__main__":
    download_music()
