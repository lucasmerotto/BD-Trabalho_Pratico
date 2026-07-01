# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import database
import queries

# Habilita sequências de escape ANSI no Windows
if sys.platform == 'win32':
    os.system('')

# Códigos de escape ANSI para estilização
LIMPAR_TELA = "\033[H\033[2J"
COR_RESET = "\033[0m"
COR_NEGRITO = "\033[1m"
COR_CABECALHO = "\033[1;36m"   # Ciano Negrito
COR_TITULO = "\033[1;35m"    # Magenta Negrito
COR_MENU = "\033[36m"       # Ciano
COR_SUCESSO = "\033[1;32m"  # Verde Negrito
COR_AVISO = "\033[1;33m"  # Amarelo Negrito
COR_ERRO = "\033[1;31m"    # Vermelho Negrito
COR_DESTAQUE = "\033[1;34m" # Azul Negrito

def exibir_banner(subtitulo=""):
    """Exibe o banner da aplicação."""
    print(f"{COR_CABECALHO}========================================================================={COR_RESET}")
    print(f"{COR_CABECALHO}   SISTEMA DE ACESSO À BASE DE DADOS - CAMPEONATOS DE FUTEBOL (FBD)      {COR_RESET}")
    print(f"{COR_CABECALHO}========================================================================={COR_RESET}")
    print(f" SGBD: {COR_NEGRITO}SQLite 3{COR_RESET} | Banco: {COR_NEGRITO}campeonato_db{COR_RESET}")
    if subtitulo:
        print(f" -> {COR_TITULO}{subtitulo}{COR_RESET}")
    print(f"{COR_CABECALHO}========================================================================={COR_RESET}")

def aguardar_tecla():
    """Solicita ao usuário que pressione Enter para continuar."""
    print(f"\nPressione {COR_AVISO}[ENTER]{COR_RESET} para voltar...")
    input()

def exibir_tabela(cabecalhos, linhas):
    """Exibe os resultados da consulta formatados como uma tabela ASCII."""
    if not cabecalhos:
        print(f"{COR_AVISO}Nenhuma coluna retornada.{COR_RESET}")
        return

    # Converte todas as células para strings
    linhas_str = []
    for linha in linhas:
        linha_str = []
        for valor in linha:
            if valor is None:
                linha_str.append("NULL")
            else:
                linha_str.append(str(valor))
        linhas_str.append(linha_str)

    # Calcula as larguras das colunas
    larguras = [len(c) for c in cabecalhos]
    for linha in linhas_str:
        for i, valor in enumerate(linha):
            if i < len(larguras):
                larguras[i] = max(larguras[i], len(valor))
            else:
                larguras.append(len(valor))

    # Constrói as bordas e formatadores ASCII
    linha_borda = "+" + "+".join("-" * (w + 2) for w in larguras) + "+"
    
    # Exibe a linha de cabeçalhos
    print(linha_borda)
    linha_cabecalho = "|" + "|".join(f" {COR_AVISO}{cabecalhos[i].ljust(larguras[i])}{COR_RESET} " for i in range(len(cabecalhos))) + "|"
    print(linha_cabecalho)
    print(linha_borda)

    # Exibe as linhas de dados
    if not linhas_str:
        largura_total = sum(larguras) + len(larguras) * 3 - 1
        msg_vazia = "Nenhum registro retornado."
        print(f"| {msg_vazia.center(largura_total - 2)} |")
    else:
        for linha in linhas_str:
            linha_dados = "|" + "|".join(f" {linha[i].ljust(larguras[i])} " for i in range(len(linha))) + "|"
            print(linha_dados)

    print(linha_borda)
    print(f"Total de registros: {COR_NEGRITO}{len(linhas)}{COR_RESET}")

def fluxo_executar_consulta(conexao, numero):
    """Fluxo para execução de uma consulta (pode ser estática ou parametrizada)."""
    consulta = queries.CONSULTAS[numero]
    print(LIMPAR_TELA)
    exibir_banner(f"Executando {consulta['titulo']}")
    print(f"\n{COR_NEGRITO}Enunciado:{COR_RESET}")
    print(f" {consulta['descricao']}")
    
    parametros = []
    # Se a consulta tiver parâmetros, pede para o usuário
    if "desc_params" in consulta:
        print(f"\n{COR_NEGRITO}Forneça os parâmetros para a consulta:{COR_RESET}")
        for rotulo, tipo_param, valor_padrao in consulta['desc_params']:
            while True:
                valor_str = input(f"  * {rotulo}: ").strip()
                if not valor_str:
                    # Se o usuário apenas apertou enter, usa o valor padrão
                    valor = valor_padrao
                    parametros.append(valor)
                    break
                
                if tipo_param == int:
                    try:
                        valor = int(valor_str)
                        parametros.append(valor)
                        break
                    except ValueError:
                        print(f"    {COR_ERRO}Erro: O valor deve ser um número inteiro.{COR_RESET}")
                else:
                    parametros.append(valor_str)
                    break

    print(f"\n{COR_NEGRITO}SQL executado:{COR_RESET}")
    # Indenta o código SQL para exibição
    sql_indentado = "\n".join("  " + linha for linha in consulta['sql'].strip().splitlines())
    print(f"{COR_DESTAQUE}{sql_indentado}{COR_RESET}")
    
    if parametros:
        print(f"{COR_NEGRITO}Parâmetros enviados (Bind):{COR_RESET} {tuple(parametros)}\n")
    else:
        print()
        
    print(f"{COR_NEGRITO}Resultado:{COR_RESET}")

    try:
        if parametros:
            # Passa a tupla de parâmetros para usar a parametrização do driver do banco (prepared statement)
            cabecalhos, linhas = database.executar_consulta_sql(conexao, consulta['sql'], tuple(parametros))
        else:
            cabecalhos, linhas = database.executar_consulta_sql(conexao, consulta['sql'])
        exibir_tabela(cabecalhos, linhas)
    except sqlite3.Error as erro:
        print(f"\n{COR_ERRO}Erro ao executar consulta no banco:{COR_RESET} {erro}")
    
    aguardar_tecla()

def menu_consultas(conexao):
    """Exibe o menu para as 10 consultas."""
    while True:
        print(LIMPAR_TELA)
        exibir_banner("Executar Consultas")
        
        # Exibe descrições curtas para cada uma das 10 consultas
        for chave, consulta in queries.CONSULTAS.items():
            sufixo = " (parametrizada)" if "desc_params" in consulta else ""
            print(f" {COR_AVISO}[{chave:2}]{COR_RESET} - {consulta['titulo']}: {consulta['descricao'][:80]}...{sufixo}")
            
        print(f"\n {COR_ERRO}[ 0]{COR_RESET} - Voltar ao Menu Principal")
        print(f"{COR_CABECALHO}-------------------------------------------------------------------------{COR_RESET}")
        
        try:
            opcao = input(f"Selecione uma consulta {COR_NEGRITO}(0-10){COR_RESET}: ").strip()
            if not opcao:
                continue
            escolha = int(opcao)
            if escolha == 0:
                break
            elif 1 <= escolha <= 10:
                fluxo_executar_consulta(conexao, escolha)
            else:
                print(f"{COR_ERRO}Opção inválida! Escolha de 0 a 10.{COR_RESET}")
                aguardar_tecla()
        except ValueError:
            print(f"{COR_ERRO}Entrada inválida! Digite um número inteiro.{COR_RESET}")
            aguardar_tecla()

def tratar_reinicializacao_banco(conexao):
    """Reinicializa o banco de dados executando os arquivos SQL."""
    print(LIMPAR_TELA)
    exibir_banner("Reinicializando base de dados")
    print(f"\n{COR_AVISO}Atenção: isso irá apagar e recriar todas as tabelas e dados.{COR_RESET}")
    confirmacao = input("Confirmar reinicialização? (s/N): ").strip().lower()
    
    if confirmacao == 's':
        try:
            database.inicializar_banco_dados(conexao, forcar=True)
            print(f"\n{COR_SUCESSO}Banco de dados reinicializado com sucesso!{COR_RESET}")
        except Exception as erro:
            print(f"\n{COR_ERRO}Erro ao inicializar banco de dados:{COR_RESET} {erro}")
    else:
        print("\nOperação cancelada.")
    aguardar_tecla()

def main():
    conexao = None
    try:
        # Estabelece a conexão
        conexao = database.obter_conexao()
        
        # Verifica e inicializa o esquema e dados do banco de dados
        inicializado = database.inicializar_banco_dados(conexao, forcar=False)
        
        if inicializado:
            print(f"{COR_SUCESSO}Banco de dados inicializado a partir de tabelas.sql e Instancias.sql.{COR_RESET}")
            
        # Loop principal da aplicação
        while True:
            print(LIMPAR_TELA)
            exibir_banner("Menu Principal")
            print(f" {COR_AVISO}[1]{COR_RESET} - Executar consultas (1 a 10)")
            print(f" {COR_AVISO}[2]{COR_RESET} - Reinicializar/Resetar base de dados")
            print(f" {COR_ERRO}[0]{COR_RESET} - Sair")
            print(f"{COR_CABECALHO}========================================================================={COR_RESET}")
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == '1':
                menu_consultas(conexao)
            elif opcao == '2':
                tratar_reinicializacao_banco(conexao)
            elif opcao == '0':
                print(f"\n{COR_SUCESSO}Programa encerrado.{COR_RESET}\n")
                break
            elif opcao == '':
                continue
            else:
                print(f"{COR_ERRO}Opção inválida! Escolha de 0 a 2.{COR_RESET}")
                aguardar_tecla()
                
    except Exception as erro:
        print(f"{COR_ERRO}Ocorreu um erro de inicialização:{COR_RESET} {erro}")
        aguardar_tecla()
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    main()
