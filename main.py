#Main

# Remove-Item -Recurse -Force .venv apaga venv
# python -m venv .venv cria venv
#pip install pydantic  
# uv pip install fastapi uvicorn  
#pip install "pydantic[email]" 
#uvicorn main:app --reload

import DataBase  
import BeseModels
import Schemas
import Seguranca
import Factory

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uuid
import sqlite3

#recuso no py que e utilizdo para gerencia um recuso, aqui ele seve para cria o BD, ser nao tive feito, e as tabelas(na mesma situacao)
@asynccontextmanager
async def spawn(app: FastAPI):
    #ao inicializa a api, executa a criacao das tabelas.
    DataBase.DateBase.get_conexao()
    #ser necesario, o yield executa no enceramento.
    yield


app = FastAPI(title="API Guia Turístico Municipal", version="2.0.0", lifespan=spawn)


# ── Usuario ─────────────


@app.post("/Usuarios_Cadastro", response_model=BeseModels.Mensagem_Retorno, status_code=201)# Referente a RF001
def Cadastra_usuario(dados: BeseModels.Usuario_Cadastro):
    novo_usuario = Factory.UsuarioFactory.criar(dados)
    with DataBase.DateBase.get_conexao() as conexao:
        try:
            conexao.execute(
                """
                INSERT INTO usuarios (id, nome, email, senha, administrador)
                VALUES (?, ?, ?, ?, ?)
                """,(novo_usuario.id,novo_usuario.nome,novo_usuario.email,novo_usuario.senha, novo_usuario.administrador)
                )
            conexao.commit()

        except sqlite3.IntegrityError:
            raise HTTPException( status_code=409, detail="Este e-mail já está cadastrado.")
        
    return BeseModels.Mensagem_Retorno(status="Sucesso", mensagem="A Conta foi criada!!")

@app.post("/Usuarios_Login", response_model=BeseModels.Mensagem_Retorno)# Referente a RF002
def Login_usuario(dados: BeseModels.Usuario_Login):
    with DataBase.DateBase.get_conexao() as conexao:
        usuario = conexao.execute(
            """
            SELECT * FROM Usuarios
            WHERE email = ? AND senha = ?
            """,(dados.email, Seguranca.gerar_hash(dados.senha))
        ).fetchone()#ele retona o usuario encontrado ou none(nada)

        if usuario:#ser a senha entrege pelo usuario for igual a amazenada no servidor, sera um sucesso.
            return BeseModels.Mensagem_Retorno(status="Sucesso",mensagem="O Login foi realizado!!")
        
    raise HTTPException(status_code=401, detail="O E-mail ou a senha estao incorretos")

@app.post("/Administrador/Login")# Referente a RF007
def login_admin(dados: BeseModels.Usuario_Login):
    with DataBase.DateBase.get_conexao() as conexao:
        admin = conexao.execute(
        """
        SELECT * FROM Usuarios
        WHERE email = ? AND administrador = 1
        """,(dados.email,)
    ).fetchone()
        
    if admin is None:
        raise HTTPException( status_code=401, detail="Administrador não encontrado.")
    
    if admin["senha"] != Seguranca.gerar_hash(dados.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    return BeseModels.Adim_Mensagem_Retorno(status="Sucesso", mensagem="Administrador autenticado.", api_key=Seguranca.API_KEY)
    
@app.get("/Usuarios", response_model=List[BeseModels.Usuario])
def listar_usuarios():
    with DataBase.DateBase.get_conexao() as conexao:
        usuarios = conexao.execute(
            """
            SELECT id, nome, email FROM Usuarios
            """
        ).fetchall()
    
    resultado = []#amazena os objetos aqui.

    for usuario in usuarios:#pega os dados colhidos do BD e os tranfoman em um objeto py.
        resultado.append(BeseModels.Usuario(id=usuario["id"], nome=usuario["nome"], email=usuario["email"]))

    return resultado#e manda pa a api.

@app.get("/Usuarios/{id}", response_model=BeseModels.Usuario)
def buscar_usuario(id: str):
    return Schemas.encontrar_usurio(id)  # helper lança 404 se não existir

@app.put("/Usuarios/{id}", response_model=BeseModels.Usuario)
def editar_usuario(id: str, dados: BeseModels.Usuario_Cadastro):
    with DataBase.DateBase.get_conexao() as conexao:
        cursor = conexao.execute(
            """
            UPDATE Usuarios
            SET nome = ?, email = ?, senha = ?
            WHERE id = ?
            """,(dados.nome, dados.email, Seguranca.gerar_hash(dados.senha), id)
        )
        conexao.commit()

        if cursor.rowcount == 0:# ser o SQL nao detetica a atualizacao de um usuario da erro.
            raise HTTPException(status_code=404, detail="O Usuario não foi encontrado")
        
        return BeseModels.Usuario(id=id, nome=dados.nome, email=dados.email)

@app.delete("/Usuarios/{id}", status_code=204)
def remover_usuario(id: str):
    with DataBase.DateBase.get_conexao() as conexao:
        cursor = conexao.execute(
            """
            DELETE FROM usuarios
            WHERE id = ?
            """,(id,)
        )#remove esse usuario da lista permanentimente.
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="O Usuario não foi encontrado")


# ── Ponto Turistico ─────────────


@app.post("/Pontos_Turisticos", response_model=BeseModels.Ponto_Turistico, status_code=201)# Permiter cadastra Pontos Turisticos
def Cadastra_ponto_turisticos(dados: BeseModels.Ponto_Turistico_Entrada, api_key: str = Depends(Seguranca.verificar_key)):
    novo_ponto = Factory.PontoFactory.criar(dados)
    with DataBase.DateBase.get_conexao() as conexao:
        conexao.execute(
            """
            INSERT INTO Pontos_Turisticos
            (id, nome, descricao, localizacao_mapa, categoria)
            VALUES (?, ?, ?, ?, ?)
            """,(novo_ponto.id, novo_ponto.nome, novo_ponto.descricao, novo_ponto.localizacao_mapa, novo_ponto.categoria)
        )
        conexao.commit()
        
        return novo_ponto 

@app.get("/Pontos_Turisticos", response_model=List[BeseModels.Ponto_Turistico])# Referente ao RF003
def Listar_pontos_turisticos():
    with DataBase.DateBase.get_conexao() as conexao:
        pontos = conexao.execute(
            "SELECT * FROM pontos_turisticos"
        ).fetchall()

    resultado = []#amazena os objetos aqui.

    for ponto in pontos:#pega os dados colhidos do BD e os tranfoman em um objeto py.
        resultado.append(BeseModels.Ponto_Turistico(id=ponto["id"], nome=ponto["nome"],
        descricao=ponto["descricao"], localizacao_mapa=ponto["localizacao_mapa"], categoria=ponto["categoria"]))

    return resultado#e manda pa a api.

@app.get("/Pontos_Turisticos/{id}", response_model= BeseModels.Ponto_Turistico) # Referente ao RF005 e um basico do RF004
def Buscar_detalhes_ponto_turistico(id: str):
    return Schemas.encontrar_ponto_turistico(id)

@app.get("/Pontos_Turisticos/{id}/localizacao")# Referente ao RF006
def Visualizar_localizacao(id: str):
    ponto = Schemas.encontrar_ponto_turistico(id)
    return{"nome":ponto.nome,   "localizacao_mapa": ponto.localizacao_mapa}

@app.put("/Pontos_Turisticos/{id}", response_model=BeseModels.Ponto_Turistico)# Permiter Atualizar/Modifica esses Pontos Turisticos
def editar_ponto_turistico(id: str, dados: BeseModels.Ponto_Turistico_Entrada, api_key: str = Depends(Seguranca.verificar_key)):
    with DataBase.DateBase.get_conexao() as conexao:
        cursor = conexao.execute(
            """
            UPDATE Pontos_Turisticos
            SET nome = ?, descricao = ?, localizacao_mapa = ?, categoria = ?
            WHERE id = ?
            """,(dados.nome, dados.descricao, dados.localizacao_mapa, dados.categoria, id)
        )
        conexao.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="O Ponto Turistico não foi encontrado")
    
    return BeseModels.Ponto_Turistico(id=id, nome=dados.nome, descricao=dados.descricao,
    localizacao_mapa=dados.localizacao_mapa, categoria=dados.categoria)

@app.delete("/Pontos_Turisticos/{id}", status_code=204)# Permiter Apagar/Deleta esses Pontos Turisticos
def remover_ponto_turistico(id: str, api_key: str = Depends(Seguranca.verificar_key)):
    with DataBase.DateBase.get_conexao() as conexao:
        cursor = conexao.execute(
            """
            DELETE FROM pontos_turisticos
            WHERE id = ?
            """,(id,)
        )
        conexao.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="O Ponto Turistico não foi encontrado")