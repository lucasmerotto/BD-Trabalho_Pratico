# -*- coding: utf-8 -*-
import sqlite3
import os
from queries import CRIAR_VIEW

def obter_conexao(nome_bd="campeonato_db"):
    """Estabelece uma conexão com o banco de dados SQLite e habilita chaves estrangeiras."""
    # Caminho absoluto relativo ao script
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_bd = os.path.join(diretorio_script, nome_bd)
    
    conexao = sqlite3.connect(caminho_bd)
    # Habilita chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao

def tabelas_existem(conexao):
    """Verifica se a tabela principal (CAMPEONATOS) já existe no banco de dados."""
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMPEONATOS';")
    return cursor.fetchone() is not None

def inicializar_banco_dados(conexao, forcar=False):
    """
    Inicializa o banco de dados usando tabelas.sql e Instancias.sql.
    Se as tabelas já existirem, só reinicializa se forcar=True.
    """
    if not forcar and tabelas_existem(conexao):
        # Banco de dados já inicializado, garante que a view seja criada
        cursor = conexao.cursor()
        cursor.execute(CRIAR_VIEW)
        conexao.commit()
        return False

    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_tabelas = os.path.join(diretorio_script, "tabelas.sql")
    caminho_instancias = os.path.join(diretorio_script, "Instancias.sql")

    if not os.path.exists(caminho_tabelas):
        raise FileNotFoundError(f"Arquivo de esquema '{caminho_tabelas}' não encontrado.")
    if not os.path.exists(caminho_instancias):
        raise FileNotFoundError(f"Arquivo de instâncias '{caminho_instancias}' não encontrado.")

    cursor = conexao.cursor()

    # Remove tabelas existentes em ordem reversa de dependência se estiver forçando a reinicialização
    if forcar:
        tabelas_para_remover = [
            "ESTATISTICAS_JOGOS", "JOGOS", "TRANSMISSAO", "ARBITRAGEM", 
            "TECNICO", "JOGADORES", "TIMES", "ESTADIOS", "CAMPEONATOS"
        ]
        # Desabilita temporariamente chaves estrangeiras para remover tabelas facilmente
        conexao.execute("PRAGMA foreign_keys = OFF;")
        for tabela in tabelas_para_remover:
            cursor.execute(f"DROP TABLE IF EXISTS {tabela};")
        cursor.execute("DROP VIEW IF EXISTS V_RESUMO_PARTIDAS;")
        conexao.execute("PRAGMA foreign_keys = ON;")
        conexao.commit()

    # Lê e executa o esquema (tabelas.sql)
    with open(caminho_tabelas, "r", encoding="utf-8") as f:
        sql_esquema = f.read()
    cursor.executescript(sql_esquema)
    conexao.commit()

    # Lê e executa os dados de teste (Instancias.sql)
    with open(caminho_instancias, "r", encoding="utf-8") as f:
        sql_dados = f.read()
    cursor.executescript(sql_dados)
    conexao.commit()

    # Cria a View necessária
    cursor.execute(CRIAR_VIEW)
    conexao.commit()

    return True

def executar_consulta_sql(conexao, sql, parametros=None):
    """
    Executa uma consulta SQL e retorna os nomes das colunas e as linhas correspondentes.
    Usa execução parametrizada se parametros forem fornecidos.
    """
    cursor = conexao.cursor()
    if parametros:
        cursor.execute(sql, parametros)
    else:
        cursor.execute(sql)
    
    # Recupera os cabeçalhos das colunas
    cabecalhos = [col[0] for col in cursor.description] if cursor.description else []
    linhas = cursor.fetchall()
    return cabecalhos, linhas
