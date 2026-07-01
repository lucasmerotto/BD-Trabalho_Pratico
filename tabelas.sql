CREATE TABLE CAMPEONATOS (
    codc char(3) not null primary key,
    continente_pais varchar(20) not null,
    tipo varchar(20) not null,
    divisao int
);

CREATE TABLE ESTADIOS (
    code char(3) not null primary key,
    nome varchar(20) not null,
    capacidade int not null,
    cidade varchar(20) not null,
    pais varchar(20) not null
);

CREATE TABLE TIMES (
    codt char(3) not null primary key,
    nome varchar(20) not null,
    pais varchar(20) not null,
    code char(3) not null,
    foreign key (code)references estadios
);

CREATE TABLE JOGADORES (
    codj char(3) not null primary key,
    nome varchar(20) not null,
    nacionalidade varchar(20) not null,
    altura float not null,
    peso float not null,
    idade int not null,
    codt char(3),
    foreign key (codt)references times,
    CHECK (idade >= 15 AND idade <=150)
);

CREATE TABLE TECNICO (
    codtec char(5) not null primary key,
    nome varchar(20) not null,
    nacionalidade varchar(20) not null,
    idade int not null,
    codt char(3),
    foreign key (codt)references times,
    CHECK (idade > 18 AND idade <=150)
);


CREATE TABLE ARBITRAGEM (
    codtrio char(6) not null primary key,
    arbitro varchar(20) not null,
    assistente1 varchar(20) not null,
    assistente2 varchar(20) not null,
    nacionalidade varchar(20) not null
);

CREATE TABLE TRANSMISSAO (
    codtransmissao char(6) not null primary key,
    canal varchar(20) not null,
    narrador varchar(20) not null,
    comentarista varchar(20) not null
);

CREATE TABLE JOGOS (
    codjogo char(6) not null primary key,
    codtmandante char(3) not null,
    golsmandante int not null,
    golsvisitante int not null,
    codtvisitante char(3) not null,
    data date not null,
    horario time not null,
    codtransmissao char(6),
    code char(3) not null,
    codc char(3) not null,
    codtrio char(6) not null,
    foreign key (codtmandante)references times,
    foreign key (codtvisitante)references times,
    foreign key (codtransmissao)references transmissao,
    foreign key (code)references estadios,
    foreign key (codc)references campeonatos,
    foreign key (codtrio)references arbitragem,
    CHECK (golsmandante >= 0),
    CHECK (golsvisitante >= 0),
    CHECK (codtmandante != codtvisitante)
);

CREATE TABLE ESTATISTICAS_JOGOS (
    codjogo char(6) not null,
    codj char(3) not null,
    gols int default 0,
    cartao_amarelo int default 0,
    cartao_vermelho int default 0,
    primary key (codjogo, codj),
    foreign key (codjogo) references JOGOS,
    foreign key (codj) references JOGADORES,
    CHECK (gols >= 0)
);
