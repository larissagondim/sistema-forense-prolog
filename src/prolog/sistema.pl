% Onde foi o crime

local_crime(sala_principal).

% Quem estava na cena

presente(larissa, sala_principal).
presente(maria, sala_principal).
presente(laura, corredor).

% Status dos sensores

sensor_ativado(laser, sala_principal).
sensor_ativado(peso, sala_principal).

% Habilidades de quem estava na cena

habilidade(larissa, desativar_laser).
habilidade(maria, manipular_objetos).
habilidade(laura, limpeza).

% Confirmação dos álibis 

alibi_confirmado(laura).

% Habilidades necessárias para realizar o crime

habilidade_necessaria(desativar_laser).
habilidade_necessaria(manipular_objetos).

% REGRAS BASE

na_cena(X) :-
    local_crime(Local),
    presente(X, Local).

houve_evento :-
    local_crime(Local),
    sensor_ativado(laser, Local),
    sensor_ativado(peso, Local).

possui_habilidade_necessaria(X) :-
    habilidade(X, H),
    habilidade_necessaria(H).

sem_alibi(X) :-
    \+ alibi_confirmado(X).

% Sistema de pontuação

ponto_cena(X, 1) :- na_cena(X), !.
ponto_cena(_, 0).

ponto_evento(1) :- houve_evento, !.
ponto_evento(0).

ponto_habilidade(X, 1) :- possui_habilidade_necessaria(X), !.
ponto_habilidade(_, 0).

ponto_alibi(X, 1) :- sem_alibi(X), !.
ponto_alibi(_, 0).

% Soma total
pontuacao(X, Total) :-
    ponto_cena(X, P1),
    ponto_evento(P2),
    ponto_habilidade(X, P3),
    ponto_alibi(X, P4),
    Total is P1 + P2 + P3 + P4.

% Classificação

nivel_suspeita(X, alta) :-
    pontuacao(X, P),
    P >= 4.

nivel_suspeita(X, media) :-
    pontuacao(X, P),
    P >= 2,
    P < 4.

nivel_suspeita(X, baixa) :-
    pontuacao(X, P),
    P < 2.

% Mantém compatibilidade com "culpado"
culpado(X) :-
    nivel_suspeita(X, alta).

% Melhor explicação

explica_texto(X, Texto) :-
    pontuacao(X, P),
    nivel_suspeita(X, Nivel),
    findall(L, explicar_linha(X, L), Linhas),
    atomic_list_concat(Linhas, '\n', Base),
    format(atom(Texto),
        '~w\nPontuação: ~w\nNível de suspeita: ~w',
        [Base, P, Nivel]).

explicar_linha(X, Linha) :-
    format(atom(Linha), 'Análise do suspeito: ~w', [X]).

explicar_linha(X, Linha) :-
    (na_cena(X) ->
        Linha = '- Estava na cena do crime (+1)' ;
        Linha = '- NÃO estava na cena do crime (+0)').

explicar_linha(_, Linha) :-
    (houve_evento ->
        Linha = '- Evento confirmado pelos sensores (+1)' ;
        Linha = '- Nenhum evento detectado (+0)').

explicar_linha(X, Linha) :-
    (possui_habilidade_necessaria(X) ->
        Linha = '- Possui habilidade relevante (+1)' ;
        Linha = '- NÃO possui habilidade relevante (+0)').

explicar_linha(X, Linha) :-
    (sem_alibi(X) ->
        Linha = '- Não possui álibi (+1)' ;
        Linha = '- Possui álibi (+0)').