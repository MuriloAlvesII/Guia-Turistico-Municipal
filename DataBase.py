#DataBase

import sqlite3 

DB_Path = "guia_turistico.db"


class DateBase:
    _conexao = None

    @classmethod
    def get_conexao(clas):
        """Vai abri e retorna uma conexão com o banco de dados para a api. nessa mesma conexao agora, nao muda ou abre outra toda vez."""
        if clas._conexao is None:
            clas._conexao = sqlite3.connect(DB_Path, check_same_thread=False)
            # vai permiti acessa as cololunas pelo nome deles(Row['usuarios'])
            clas._conexao.row_factory = sqlite3.Row

        return clas._conexao

    @classmethod
    def init_db(clas):
        """Ser não encontra uma tabela, ser ela ainda não existir, cria a mesma, a mesma mudaca fei ai em cima"""
        conexao = clas.get_conexao()
        conexao.executescript("""                
                
                CREATE TABLE IF NOT EXISTS Usuarios (
                    id        TEXT PRIMARY KEY,
                    email     TEXT NOT NULL UNIQUE,
                    nome      TEXT NOT NULL,
                    senha     TEXT NOT NULL,
                    administrador INTEGER NOT NULL DEFAULT 0
                );
                        
                CREATE TABLE IF NOT EXISTS Pontos_Turisticos (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    localizacao_mapa TEXT NOT NULL,
                    categoria TEXT NOT NULL
                );
            """)
        conexao.commit()
# cursor = conexao.cursor()
