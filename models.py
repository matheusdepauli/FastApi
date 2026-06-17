# Arquivo: models.py
from sqlalchemy import Column, Integer, String
from database import Base
class Componente(Base):
 # Nome exato da tabela no MySQL
 __tablename__ = "tb_componentes"
 # Colunas da tabela
 id = Column(Integer, primary_key=True, index=True, autoincrement=True)
 nome = Column(String(100), nullable=False)
 quantidade = Column(Integer, default=0)
 categoria = Column(String(50), nullable=False)
 conservacao = Column(String(50), nullable=False)
