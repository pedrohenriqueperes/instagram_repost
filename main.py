import os
import instaloader
import time
import random


# Função para criar uma pasta se ela não existir
def criar_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)


# Função para obter a lista de arquivos em uma pasta
def obter_lista_arquivos(pasta):
    return [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]


# Número aleatório para o intervalo de espera
num_aleatorio = random.randint(10, 30)

# Informe seu nome de usuário e senha do Instagram
username = str(input("username: "))
password = str(input("senha: "))

# Logue na conta
try:
    loader = instaloader.Instaloader()
    loader.context.login(username, password)
except instaloader.exceptions.InstaloaderException as e:
    print(f"Erro ao fazer login: {e}")
    exit()

# Informe o nome de usuário do perfil que você deseja baixar
profile = str(input("target profile: "))

# Pasta para armazenar os arquivos
pasta_destino = 'pasta_destino'
criar_pasta(pasta_destino)

# Baixe o perfil (se já não foi baixado)
loader.download_profile(profile, profile_pic_only=False)

# Itere pelos arquivos na pasta de destino
for arquivo in obter_lista_arquivos(os.path.join(pasta_destino, profile)):
    # Ignore arquivos de legenda
    if arquivo.endswith('_legenda.txt'):
        continue

    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_destino, profile, arquivo)

    # Legenda do arquivo
    caminho_legenda = os.path.join(pasta_destino, profile,
                                   f"{arquivo.split('_')[0]}_{arquivo.split('_')[1]}_legenda.txt")
    with open(caminho_legenda, 'r', encoding='utf-8') as arquivo_legenda:
        legenda = arquivo_legenda.read()

    # Realize a postagem
    try:
        loader.context.upload_photo(caminho_arquivo, caption=legenda)
        print(f"Postagem realizada com sucesso para {arquivo}!")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"Erro ao realizar postagem para {arquivo}: {e}")

    # Aguarde um tempo aleatório
    time.sleep(num_aleatorio)
