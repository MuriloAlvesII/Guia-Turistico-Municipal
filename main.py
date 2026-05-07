def main():
    print("Hello from guia-turistico-municipal!")


if __name__ == "__main__":
    main()

# Remove-Item -Recurse -Force .venv apaga venv
# python -m venv .venv cria venv
#pip install pydantic  
# uv pip install fastapi uvicorn  
#pip install "pydantic[email]" 
#uvicorn main:app --reload  

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel , EmailStr
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="API Guia Turístico Municipal", version="1.0.0")

# ── Usuario ──────────────────────────

class Usuario_Base(BaseModel):
    email: EmailStr

class Usuario_Cadastro(Usuario_Base): # RF001
    nome: str
    senha: str

class Usuario_BD(Usuario_Cadastro):
    id: str

class Usuario_Login(Usuario_Base): # RF002
    senha: str

class Usuario(Usuario_Base):
    id: str
    nome: str

# ── Ponto Turistico ─────

class Ponto_Turistico_Entrada(BaseModel):#RF003, RF004, RF005 e RF006
    nome: str
    descricao: str
    localizacao_mapa: str
    categoria: str

class Ponto_Turistico(Ponto_Turistico_Entrada):
    id: str

# ── Resposta dos RFs ─────────────

class Mensagem_Retorno(BaseModel):
    status: str
    mensagem: str

# ── Dados em memoria ─────────────

usuarios_bd: List[Usuario_BD] = []
ponto_turistico_bd: List[Ponto_Turistico] = []

# ── helpers ─────────────

def encontrar_usurio(id: str) -> Usuario:
    for usuario in usuarios_bd:
        if usuario.id == id:
            return usuario
        
    raise HTTPException(status_code=404, detail="Esse usuario não foi encontrado")

def encontrar_ponto_turistico(id: str) -> Ponto_Turistico:
    for ponto_turistico in ponto_turistico_bd:
        if ponto_turistico.id == id:
            return ponto_turistico
        
    raise HTTPException(status_code=404, detail="Esse Ponto Turistico não foi encontrado")

# ── Usuario ─────────────

@app.post("/Usuarios_Cadastro", response_model=Mensagem_Retorno, status_code=201)# Referente a RF001
def Cadastra_usuario(dados: Usuario_Cadastro):
    novo_usuario = Usuario_BD(id=str(uuid.uuid4()), **dados.model_dump())
    usuarios_bd.append(novo_usuario)
    return Mensagem_Retorno(status="Sucesso", mensagem="A Conta foi criada!!")

@app.post("/Usuarios_Login", response_model=Mensagem_Retorno)# Referente a RF002
def Login_usuario(dados: Usuario_Login):
    for a in usuarios_bd:
        if a.email == dados.email and a.senha == dados.senha:#ser a senha entrege pelo usuario for igual a amazenada no servidor, sera um sucesso.
            return Mensagem_Retorno(status="Sucesso",mensagem="O Login foi realizado!!")
        
    raise HTTPException(status_code=401, detail="O E-mail ou a senha estao incorretos")

@app.get("/Usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios_bd

@app.get("/Usuarios/{id}", response_model=Usuario)
def buscar_usuario(id: str):
    return encontrar_usurio(id)  # helper lança 404 se não existir

@app.put("/Usuarios/{id}", response_model=Usuario)
def editar_usuario(id: str, dados: Usuario_Cadastro):
    for i, a in enumerate(usuarios_bd):
        #i= posicao do usuario na lista.
        # a= usuario e tudo que ele tem.
        if a.id == id:
            atualizado = Usuario_BD(id=id, **dados.model_dump())
            usuarios_bd[i] = atualizado
            return atualizado
        
    raise HTTPException(status_code=404, detail="O Usuario não foi encontrado")

@app.delete("/Usuarios/{id}", status_code=204)
def remover_usuario(id: str):
    for i, a in enumerate(usuarios_bd):
        if a.id == id:
            usuarios_bd.pop(i)#remove esse usuario da lista permanentimente.
            return
        
    raise HTTPException(status_code=404, detail="O Usuario não foi encontrado")

# ── Ponto Turistico ─────────────
@app.post("/Pontos_Turisticos", response_model=Ponto_Turistico, status_code=201)# Permiter cadastra Pontos Turisticos
def Cadastra_ponto_turisticos(dados: Ponto_Turistico_Entrada):
    novo_ponto = Ponto_Turistico(id=str(uuid.uuid4()), **dados.model_dump())
    ponto_turistico_bd.append(novo_ponto)
    return novo_ponto 

@app.get("/Pontos_Turisticos", response_model=List[Ponto_Turistico])# Referente ao RF003
def Listar_pontos_turisticos():
    return ponto_turistico_bd

@app.get("/Pontos_Turisticos/{id}", response_model= Ponto_Turistico) # Referente ao RF005 e um basico do RF004
def Buscar_detalhes_ponto_turistico(id: str):
    return encontrar_ponto_turistico(id)

@app.get("/Pontos_Turisticos/{id}/localizacao")# Referente ao RF006
def Visualizar_localizacao(id: str):
    ponto = encontrar_ponto_turistico(id)
    return{"nome":ponto.nome,"localizacao_mapa": ponto.localizacao_mapa}

@app.put("/Pontos_Turisticos/{id}", response_model=Ponto_Turistico)# Permiter Atualizar/Modifica esses Pontos Turisticos
def editar_ponto_turistico(id: str, dados: Ponto_Turistico_Entrada):
    for i, a in enumerate(ponto_turistico_bd):
        #i= posicao do usuario na lista.
        # a= usuario e tudo que ele tem.
        if a.id == id:
            atualizado = Ponto_Turistico(id=id, **dados.model_dump())
            ponto_turistico_bd[i] = atualizado
            return atualizado
        
    raise HTTPException(status_code=404, detail="O Ponto Turistico não foi encontrado")

@app.delete("/Pontos_Turisticos/{id}", status_code=204)# Permiter Apagar/Deleta esses Pontos Turisticos
def remover_ponto_turistico(id: str):
    for i, a in enumerate(ponto_turistico_bd):
        if a.id == id:
            ponto_turistico_bd.pop(i)#remove esse ponto turistico da lista permanentimente.
            return
        
    raise HTTPException(status_code=404, detail="O Ponto Turistico não foi encontrado")