import DataBase
import BeseModels
from fastapi import FastAPI, HTTPException

# ── helpers ─────────────

def encontrar_usurio(id: str) -> BeseModels.Usuario:
    with DataBase.get_conexao() as conexao:
        usuario = conexao.execute(
            """
            SELECT id FROM Usuarios
            WHERE id = ?
            """,(id)
        ).fetchone()

        if usuario is None:
            raise HTTPException(status_code=404, detail="Esse usuario não foi encontrado")
        
        #pega os dados colhidos do BD e os tranfoman em um objeto py.
        return BeseModels.Usuario(id=usuario["id"], nome=usuario["nome"], email=usuario["email"])
        
def encontrar_ponto_turistico(id: str) -> BeseModels.Ponto_Turistico:
    with DataBase.get_conexao() as conexao:
        ponto = conexao.execute(
            """
            SELECT id FROM Pontos_Turisticos
            WHERE id = ?
            """,(id)
        ).fetchone()

        if ponto is None:
            raise HTTPException(status_code=404, detail="Esse Ponto Turistico não foi encontrado")
        
        #pega os dados colhidos do BD e os tranfoman em um objeto py.
        return BeseModels.Ponto_Turistico(id=ponto["id"], nome=ponto["nome"], descricao=ponto["descricao"],
        localizacao_mapa=ponto["localizacao_mapa"], categoria=ponto["categoria"])
