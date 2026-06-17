from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import engine, obter_banco

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Inova Lab - Inventário Maker")

class ComponenteSchema(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do componente maker")
    quantidade: int = Field(..., ge=0, description="Quantidade em estoque (deve ser maior ou igual a zero)")
    categoria: str = Field(..., description="Categoria do item (ex: Atuadores, Microcontroladores)")
    conservacao: str = Field(..., description="Conservacao do item (ex: Boa, Ruim, Ok, Pessima)")

@app.get("/")
def raiz():
    return {"mensagem": "API do Laboratório Maker operante. Acesse /docs para ver a documentação."}

@app.get("/componentes")
def listar_componentes(banco: Session = Depends(obter_banco)):
    return banco.query(models.Componente).all()

@app.post("/componentes", status_code=201)
def adicionar_componente(novo_componente: ComponenteSchema, banco: Session = Depends(obter_banco)):
    componente = models.Componente(**novo_componente.model_dump())
    banco.add(componente)
    banco.commit()
    banco.refresh(componente)
    return {"mensagem": "Componente adicionado com sucesso!", "componente": componente}

@app.put("/componentes/{componente_id}")
def atualizar_componente(componente_id: int, dados_atualizados: ComponenteSchema, banco: Session = Depends(obter_banco)):
    item = banco.query(models.Componente).filter(models.Componente.id == componente_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Componente não encontrado no laboratório.")
    item.nome = dados_atualizados.nome
    item.quantidade = dados_atualizados.quantidade
    item.categoria = dados_atualizados.categoria
    item.conservacao = dados_atualizados.conservacao
    banco.commit()
    banco.refresh(item)
    return {"mensagem": "Componente atualizado com sucesso!", "componente": item}

@app.delete("/componentes/{componente_id}")
def remover_componente(componente_id: int, banco: Session = Depends(obter_banco)):
    item = banco.query(models.Componente).filter(models.Componente.id == componente_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Componente não encontrado no laboratório.")
    banco.delete(item)
    banco.commit()
    return {"mensagem": f"Componente com ID {componente_id} foi removido do estoque."}