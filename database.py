# Arquivo: database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# String de conexão:
# banco://usuario:senha@servidor:porta/nome_do_banco
# (Ajuste o root e a senha vazia conforme o padrão das máquinas do laboratório)
URL_BANCO_DADOS = "mysql+pymysql://root:@localhost:3306/inova_inventario"

# O Engine é o motor que traduz o Python para o dialeto do MySQL
engine = create_engine(URL_BANCO_DADOS)

# A Sessão é o "túnel" por onde os dados vão trafegar
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criar as tabelas
Base = declarative_base()

# Função auxiliar para injetar a sessão nas rotas (veremos na próxima aula)
def obter_banco():
    banco = SessaoLocal()
    try:
        yield banco
    finally:
        banco.close()