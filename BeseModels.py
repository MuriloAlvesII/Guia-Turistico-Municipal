from pydantic import BaseModel , EmailStr

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