#Seguraranca

#gerar o hash da senha e da API Key
import hashlib
#ler o conteúdo do arquivo
import os

#Carrega o arquivo .env.
from dotenv import load_dotenv
#Header pega informações enviadas no cabeçalho da requisição.
from fastapi import Header, HTTPException

#procura o .env e pega API_KEY_HASH
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_HASH = os.getenv("API_KEY_HASH")

def verificar_key(x_api_key: str = Header(...)): #verifica ser o usuario tem a key coreta, ser nao tive ele encera a rota que vai esta implemetado e responde com not autorizdo
    if API_KEY_HASH is None:
        raise HTTPException(status_code=500, detail="API_KEY_HASH não configurada.")
    
    hash_recebido = hashlib.sha256(x_api_key.encode()).hexdigest()

    if hash_recebido != API_KEY_HASH:
        raise HTTPException(status_code=401, detail="Key inválida.")

def gerar_hash(senha: str):
    return hashlib.sha256(senha.encode()).hexdigest()