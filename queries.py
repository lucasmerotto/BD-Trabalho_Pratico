# -*- coding: utf-8 -*-

# Consulta para criar a visão base
# Descrição: Dados essenciais de uma partida. Substui os códigos pelos nomes dos times, o local e caracteristicas do campeonato:
CRIAR_VIEW = """
CREATE VIEW IF NOT EXISTS V_RESUMO_PARTIDAS AS
SELECT 
    j.codjogo,
    c.continente_pais AS competicao,
    c.tipo AS tipo_competicao,
    tm.nome AS time_mandante,
    j.golsmandante AS gols_mandante,
    j.golsvisitante AS gols_visitante,
    tv.nome AS time_visitante,
    j.data AS data_jogo,
    j.horario,
    e.nome AS estadio
FROM JOGOS j
JOIN TIMES tm ON j.codtmandante = tm.codt
JOIN TIMES tv ON j.codtvisitante = tv.codt
JOIN CAMPEONATOS c ON j.codc = c.codc
JOIN ESTADIOS e ON j.code = e.code;
"""

# As 10 consultas base do sistema (conforme consultas.sql)
# Duas delas (Consulta 3 e Consulta 9) foram adaptadas para receber parâmetros dinâmicos.
CONSULTAS = {
    1: {
        "titulo": "Consulta 1",
        "descricao": "Os jogadores e seus times e o total de gols que cada um fez, desde que tenha marcado pelo menos 2 gols, em ordem decrescente.",
        "sql": """
SELECT 
    JOGADORES.nome, 
    TIMES.nome, 
    SUM(ESTATISTICAS_JOGOS.gols) AS total_gols
FROM 
    JOGADORES
JOIN 
    TIMES ON JOGADORES.codt = TIMES.codt
JOIN 
    ESTATISTICAS_JOGOS ON JOGADORES.codj = ESTATISTICAS_JOGOS.codj
GROUP BY 
    JOGADORES.nome, 
    TIMES.nome
HAVING 
    SUM(ESTATISTICAS_JOGOS.gols) > 1
ORDER BY 
    total_gols DESC;
"""
    },
    2: {
        "titulo": "Consulta 2",
        "descricao": "Seleciona os árbitros, os jogadores aos quais ele aplicou cartões amarelos e a quantidade, desde que tenha aplicado ao menos um amarelo.",
        "sql": """
SELECT
    ARBITRAGEM.arbitro,
    JOGADORES.nome,
    SUM(ESTATISTICAS_JOGOS.cartao_amarelo) as total_amarelos
FROM
    ARBITRAGEM
join 
    JOGOS on ARBITRAGEM.codtrio = JOGOS.codtrio
join 
    ESTATISTICAS_JOGOS on ESTATISTICAS_JOGOS.codjogo = JOGOS.codjogo
join 
    JOGADORES on JOGADORES.codj = ESTATISTICAS_JOGOS.codj
WHERE
    ESTATISTICAS_JOGOS.cartao_amarelo > 0
GROUP BY 
    ARBITRAGEM.arbitro,
    JOGADORES.nome
order by
    total_amarelos DESC,
    ARBITRAGEM.arbitro;
"""
    },
    3: {
        "titulo": "Consulta 3",
        "descricao": "Seleciona técnicos, seus times e quantidade de jogos que jogaram em estádios com capacidade superior a um limite informado (parametrizada).",
        "desc_params": [("Capacidade Mínima do Estádio (Padrão: 50000)", int, 50000)],
        "sql": """
SELECT
    TECNICO.nome,
    TIMES.nome,
    COUNT(JOGOS.codjogo) as total_jogos_estadio_grandee
FROM
    TIMES
JOIN
    JOGOS on JOGOS.codtmandante = TIMES.codt or JOGOS.codtvisitante = TIMES.codt
JOIN
    TECNICO on TECNICO.codt = TIMES.codt
JOIN
    ESTADIOS on ESTADIOS.code = JOGOS.code
WHERE
    ESTADIOS.capacidade > ?
GROUP BY
    TECNICO.nome,
    TIMES.nome;
"""
    },
    4: {
        "titulo": "Consulta 4",
        "descricao": "Jogadores com idade maior que a média de jogadores, treinados por técnicos com idade maior que a média de idade de técnicos, e o time em que trabalham.",
        "sql": """
SELECT
    JOGADORES.nome,
    JOGADORES.idade,
    TECNICO.nome,
    TECNICO.idade,
    TIMES.nome
FROM
    JOGADORES
JOIN
    TIMES ON JOGADORES.codt = TIMES.codt
JOIN
    TECNICO ON TIMES.codt = TECNICO.codt
WHERE 
    JOGADORES.idade > (SELECT AVG(idade) FROM JOGADORES)
    AND
    TECNICO.idade > (SELECT AVG(idade) FROM TECNICO);
"""
    },
    5: {
        "titulo": "Consulta 5",
        "descricao": "Canais e narradores que participaram da transmissão dos jogos no estádio com a maior capacidade, apresentando também o nome do estádio.",
        "sql": """
SELECT 
    TRANSMISSAO.canal,
    TRANSMISSAO.narrador,
    ESTADIOS.nome
FROM
    TRANSMISSAO
JOIN
    JOGOS on JOGOS.codtransmissao = TRANSMISSAO.codtransmissao
JOIN
    ESTADIOS on ESTADIOS.code = JOGOS.code
WHERE
    capacidade = (SELECT MAX(capacidade) from ESTADIOS);
"""
    },
    6: {
        "titulo": "Consulta 6",
        "descricao": "Seleciona o nome de todos os integrantes do trio de arbitragem que trabalharam em todos os jogos das competições europeias.",
        "sql": """
SELECT
    ARBITRAGEM.arbitro,
    ARBITRAGEM.assistente1,
    ARBITRAGEM.assistente2
FROM
    ARBITRAGEM
where not EXISTS(
    SELECT 
        JOGOS.codjogo
    from 
        JOGOS
    JOIN
        CAMPEONATOS on CAMPEONATOS.codc = JOGOS.codc
    WHERE
        CAMPEONATOS.continente_pais = 'Europa'
    EXCEPT
    SELECT 
        JOGOS.codjogo
    from 
        JOGOS
    JOIN
        CAMPEONATOS on CAMPEONATOS.codc = JOGOS.codc
    WHERE
        CAMPEONATOS.continente_pais = 'Europa' and JOGOS.codtrio = ARBITRAGEM.codtrio);
"""
    },
    7: {
        "titulo": "Consulta 7",
        "descricao": "Seleciona todos os jogos empatados e seus dados de arbitragem e transmissão (usando a VIEW V_RESUMO_PARTIDAS).",
        "sql": """
SELECT 
    V_RESUMO_PARTIDAS.time_mandante,
    V_RESUMO_PARTIDAS.gols_mandante,
    V_RESUMO_PARTIDAS.gols_visitante,
    V_RESUMO_PARTIDAS.time_visitante,
    ARBITRAGEM.arbitro,
    TRANSMISSAO.canal
FROM 
    V_RESUMO_PARTIDAS
JOIN 
    JOGOS ON V_RESUMO_PARTIDAS.codjogo = JOGOS.codjogo
JOIN 
    ARBITRAGEM ON JOGOS.codtrio = ARBITRAGEM.codtrio
JOIN 
    TRANSMISSAO ON JOGOS.codtransmissao = TRANSMISSAO.codtransmissao
WHERE 
    V_RESUMO_PARTIDAS.gols_mandante = V_RESUMO_PARTIDAS.gols_visitante;
"""
    },
    8: {
        "titulo": "Consulta 8",
        "descricao": "Seleciona os jogos que tiveram gols, trazendo a quantidade de gols total, os jogadores que marcaram e quantos gols cada um fez (usando a VIEW).",
        "sql": """
SELECT
    V_RESUMO_PARTIDAS.time_mandante,
    V_RESUMO_PARTIDAS.time_visitante,
    V_RESUMO_PARTIDAS.estadio,
    (V_RESUMO_PARTIDAS.gols_mandante + V_RESUMO_PARTIDAS.gols_visitante) as gols_na_partida,
    JOGADORES.nome as jogador_que_marcou,
    ESTATISTICAS_JOGOS.gols as gols_do_jogador
FROM
    V_RESUMO_PARTIDAS
JOIN
    ESTATISTICAS_JOGOS on V_RESUMO_PARTIDAS.codjogo = ESTATISTICAS_JOGOS.codjogo
join
    JOGADORES on JOGADORES.codj = ESTATISTICAS_JOGOS.codj
WHERE
    ESTATISTICAS_JOGOS.gols > 0
ORDER BY
    gols_na_partida DESC,
    ESTATISTICAS_JOGOS.gols DESC;
"""
    },
    9: {
        "titulo": "Consulta 9",
        "descricao": "Nome do time, estádio e treinador para todos os times que jogam em estádios de uma determinada cidade (parametrizada).",
        "desc_params": [("Nome da Cidade (Padrão: Porto Alegre)", str, "Porto Alegre")],
        "sql": """
SELECT 
    TIMES.nome,
    TECNICO.nome,
    ESTADIOS.nome
FROM
    TIMES
join 
    ESTADIOS on ESTADIOS.code = TIMES.code
JOIN
    TECNICO on TECNICO.codt = TIMES.codt
WHERE	
    ESTADIOS.cidade = ?;
"""
    },
    10: {
        "titulo": "Consulta 10",
        "descricao": "Narradores que narram jogos noturnos de campeonatos do Brasil (a partir das 19h) e qual o estádio.",
        "sql": """
SELECT
    TRANSMISSAO.narrador,
    ESTADIOS.nome
FROM
    TRANSMISSAO
JOIN
    JOGOS on JOGOS.codtransmissao = TRANSMISSAO.codtransmissao
JOIN
    ESTADIOS on JOGOS.code = ESTADIOS.code
JOIN
    CAMPEONATOS ON CAMPEONATOS.codc = JOGOS.codc
WHERE
    JOGOS.horario >= '19:00:00'
    AND
    CAMPEONATOS.continente_pais = 'Brasil';
"""
    }
}
