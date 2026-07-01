-- Dados essenciais de uma partida. Substui os códigos pelos nomes dos times, o local e caracteristicas do campeonato:
CREATE VIEW V_RESUMO_PARTIDAS AS
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

-- Consulta 1: Os jogadores e seus times e o total de gols que cada um fez, desde que tenha marcado pelo menos 2 gols.
-- resultado apresentado de forma decrescente
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
--Consulta 2: Seleciona os árbitros, os jogadores aos quais ele aplicou cartões amarelos e a quantidade, desde que 
--tenha aplicado ao menos um amarelo.
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
	ESTATISTICAS_JOGOS.cartao_amarelo>0
GROUP BY 
	ARBITRAGEM.arbitro,
    JOGADORES.nome
order by
 	total_amarelos DESC,
    ARBITRAGEM.arbitro;
    
--Consulta 3: Seleciona técnicos, seus times e quantidade de jogos que jogaram em estádios com capacidade superior a
--50.000 espectadores

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
	ESTADIOS.capacidade>50000
GROUP BY
	TECNICO.nome,
    TIMES.nome;
    
--Consulta 4: Jogadores com idade maior que a média de jogadores, treinados por técnicos com idade maior que a média
-- de idade de técnicos e o time em que trabalham.
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

--Consulta 5: Canais e narradores que participaram da transmissão dos jogos no estádio com a maior capacidade,
--apresenta também o nome do estádio
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

--Consulta 6: Seleciona o nome de todos os integrantes do trio de arbitragem que trabalharam em todos os jogos das
--competições europeias
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
  CAMPEONATOS.continente_pais='Europa'
	EXCEPT
  SELECT 
  JOGOS.codjogo
 from 
  JOGOS
 JOIN
  CAMPEONATOS on CAMPEONATOS.codc = JOGOS.codc
 WHERE
  CAMPEONATOS.continente_pais='Europa' and JOGOS.codtrio = ARBITRAGEM.codtrio);
  
-- Consulta 7: Seleciona todos os jogos empatados e seus dados de arbitragem e transmissão
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
--Consulta 8: Seleciona os jogos que tiveram gols, traz a quantidade de gols que teve no jogo, os jogadores que
--marcaram e quantos gols ele fez
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
    
 --Consulta 9: Nome do time, estádio e treinador para todos os times que jogam em estádios de Porto Alegre
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
	ESTADIOS.cidade='Porto Alegre';
    
--Consulta 10: Narradores que narram jogos noturnos de campeonatos do Brasil (a partir da 19h) e qual o estádio 
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
    CAMPEONATOS.continente_pais='Brasil';