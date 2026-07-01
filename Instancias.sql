INSERT INTO CAMPEONATOS (codc, continente_pais, tipo, divisao) VALUES 
('C01', 'Brasil', 'Liga', 1),
('C02', 'Europa', 'Mata-mata', NULL),
('C03', 'América do Sul', 'Copa', NULL);

INSERT INTO ESTADIOS (code, nome, capacidade, cidade, pais) VALUES 
('E01', 'Arena do Grêmio', 55662, 'Porto Alegre', 'Brasil'),
('E02', 'Morumbi', 66795, 'São Paulo', 'Brasil'),
('E03', 'Santiago Bernabéu', 81044, 'Madrid', 'Espanha'),
('E04', 'Wembley', 90000, 'Londres', 'Inglaterra'),
('E05', 'El Cilindro', 42500, 'Avellaneda', 'Argentina');

INSERT INTO TIMES (codt, nome, pais, code) VALUES 
('T01', 'Grêmio', 'Brasil', 'E01'),
('T02', 'São Paulo', 'Brasil', 'E02'),
('T03', 'Real Madrid', 'Espanha', 'E03'),
('T04', 'Arsenal', 'Inglaterra', 'E04'),
('T05', 'Racing', 'Argentina', 'E05');

INSERT INTO JOGADORES (codj, nome, nacionalidade, altura, peso, idade, codt) VALUES 
('J01', 'Marlon', 'Brasil', 1.84, 78, 28, 'T01'), 
('J02', 'Carlos Vinícius', 'Brasil', 1.90, 83, 31, 'T01'),
('J03', 'Calleri', 'Argentina', 1.81, 76, 30, 'T02'),
('J04', 'Bobadilla', 'Paraguai', 1.78, 75, 25, 'T02'), 
('J05', 'Vini Jr', 'Brasil', 1.76, 73, 23, 'T03'),
('J06', 'Bellingham', 'Inglaterra', 1.86, 75, 20, 'T03'),
('J07', 'Saka', 'Inglaterra', 1.78, 72, 22, 'T04'),
('J08', 'Gabriel Jesus', 'Brasil', 1.75, 73, 27, 'T04'),
('J09', 'Juanfer Quintero', 'Colômbia', 1.69, 67, 31, 'T05'),
('J10', 'Adrián Martínez', 'Argentina', 1.81, 78, 31, 'T05');

INSERT INTO TECNICO (codtec, nome, nacionalidade, idade, codt) VALUES 
('TC1', 'Luís Castro', 'Portugal', 64, 'T01'), 
('TC2', 'Dorival Jr', 'Brasil', 62, 'T02'), 
('TC3', 'Xabi Alonso', 'Espanha', 44, 'T03'), 
('TC4', 'Mikel Arteta', 'Espanha', 42, 'T04'), 
('TC5', 'Gustavo Costas', 'Argentina', 61, 'T05'); 

INSERT INTO ARBITRAGEM (codtrio, arbitro, assistente1, assistente2, nacionalidade) VALUES 
('A01', 'Raphael Claus', 'Neuza Inês', 'Danilo Manis', 'Brasil'),
('A02', 'Wilton Sampaio', 'Bruno Boschilia', 'Bruno Pires', 'Brasil'),
('A03', 'Michael Oliver', 'Stuart Burt', 'Dan Cook', 'Inglaterra'),
('A04', 'Facundo Tello', 'Ezequiel Brailovsky', 'Gabriel Chade', 'Espanha');

INSERT INTO TRANSMISSAO (codtransmissao, canal, narrador, comentarista) VALUES 
('TR1', 'TV Globo', 'Luis Roberto', 'Caio Ribeiro'),
('TR2', 'CazeTV', 'Casimiro', 'Luis Felipe Freitas'),
('TR3', 'ESPN', 'Paulo Andrade', 'Paulo Calçade');

INSERT INTO JOGOS (codjogo, codtmandante, golsmandante, golsvisitante, codtvisitante, data, horario, codtransmissao, code, codc, codtrio) VALUES 
('JG1', 'T01', 2, 1, 'T02', '2026-05-10', '16:00:00', 'TR1', 'E01', 'C01', 'A01'),
('JG2', 'T03', 3, 0, 'T04', '2026-05-12', '16:45:00', 'TR2', 'E03', 'C02', 'A03'),
('JG3', 'T02', 0, 0, 'T01', '2026-08-15', '21:30:00', 'TR1', 'E02', 'C01', 'A02'),
('JG4', 'T04', 1, 2, 'T03', '2026-05-19', '16:00:00', 'TR3', 'E04', 'C02', 'A03'),
('JG5', 'T02', 1, 1, 'T05', '2026-09-10', '21:30:00', 'TR3', 'E02', 'C03', 'A04'),
('JG6', 'T05', 2, 0, 'T01', '2026-10-15', '21:30:00', 'TR3', 'E05', 'C03', 'A04');

INSERT INTO ESTATISTICAS_JOGOS (codjogo, codj, gols, cartao_amarelo, cartao_vermelho) VALUES 
-- JG1 (Grêmio 2x1 São Paulo)
('JG1', 'J02', 2, 0, 0), -- Carlos Vinícius fez 2 gols
('JG1', 'J01', 0, 1, 0), -- Marlon levou amarelo
('JG1', 'J03', 1, 0, 0), -- Calleri fez 1 gol

-- JG2 (Real Madrid 3x0 Arsenal)
('JG2', 'J05', 2, 0, 0), -- Vini Jr fez 2 gols
('JG2', 'J06', 1, 1, 0), -- Bellingham fez 1 gol e levou amarelo

-- JG3 (São Paulo 0x0 Grêmio)
('JG3', 'J04', 0, 1, 0), -- Bobadilla levou amarelo
('JG3', 'J02', 0, 1, 0), -- Carlos Vinícius levou amarelo

-- JG4 (Arsenal 1x2 Real Madrid)
('JG4', 'J07', 1, 0, 0), -- Saka fez 1 gol
('JG4', 'J05', 2, 0, 0), -- Vini Jr fez 2 gols
('JG4', 'J06', 0, 0, 1), -- Bellingham levou vermelho

-- JG5 (São Paulo 1x1 Racing)
('JG5', 'J03', 1, 0, 0), -- Calleri fez 1 gol
('JG5', 'J09', 1, 0, 0), -- Juanfer Quintero fez 1 gol
('JG5', 'J10', 0, 1, 0), -- Adrián Martínez levou amarelo

-- JG6 (Racing 2x0 Grêmio)
('JG6', 'J09', 1, 0, 0), -- Juanfer Quintero fez 1 gol
('JG6', 'J10', 1, 0, 0), -- Adrián Martínez fez 1 gol
('JG6', 'J01', 0, 1, 0); -- Marlon levou um amarelo