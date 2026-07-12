import uuid
import BeseModels
import Seguranca

class UsuarioFactory:

    @staticmethod
    def criar(dados,administrador=0):
        return BeseModels.Usuario_BD(id=str(uuid.uuid4()), nome=dados.nome, email=dados.email, senha=Seguranca.gerar_hash(dados.senha), administrador=administrador)

class PontoFactory:

    @staticmethod
    def criar(dados):
        return BeseModels.Ponto_Turistico(id=str(uuid.uuid4()), nome=dados.nome, descricao=dados.descricao,
        localizacao_mapa=dados.localizacao_mapa, categoria=dados.categoria)