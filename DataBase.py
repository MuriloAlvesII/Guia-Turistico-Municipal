import sqlite3 

DB_Path = "guia_turistico.db"

def get_conexao() -> sqlite3.Connection:
    """Vai abri e retorna uma conexão com o banco de dados para a api."""
    conexao = sqlite3.connect(DB_Path)
    # vai permiti acessa as cololunas pelo nome deles(Row['usuarios'])
    conexao.row_factory = sqlite3.Row
    return conexao

def init_db():
    """Ser não encontra uma tabela, ser ela ainda não existir, cria a mesma"""
    with get_conexao() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                id        TEXT PRIMARY KEY,
                email     TEXT NOT NULL,
                nome      TEXT NOT NULL,
                senha     TEXT NOT NULL
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
