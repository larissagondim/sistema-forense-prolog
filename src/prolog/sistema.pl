% Local onde foi realizado o crime
local_crime(sala_principal).

% Presença dos suspeitos
presente(larissa, sala_principal).
presente(maria, sala_principal).
presente(laura, corredor).

% Sensores ativados
sensor_ativado(laser, sala_principal).
sensor_ativado(peso, sala_principal).

% Habilidades
habilidade(larissa, desativar_laser).
habilidade(maria, manipular_objetos).
habilidade(laura, limpeza).

% Álibis
alibi_confirmado(laura).

% Habilidades necessárias para o crime
habilidade_necessaria(desativar_laser).
habilidade_necessaria(manipular_objetos).

% REGRAS

% Estava na cena do crime
na_cena(X) :-
    local_crime(Local),
    presente(X, Local).

% Evento confirmado
houve_evento :-
    local_crime(Local),
    sensor_ativado(laser, Local),
    sensor_ativado(peso, Local).

% Possui pelo menos uma habilidade relevante
possui_habilidade_necessaria(X) :-
    habilidade(X, H),
    habilidade_necessaria(H).

% Sem álibi
sem_alibi(X) :-
    \+ alibi_confirmado(X).

% Critérios separados (melhor debug)
criterio_cena(X) :- na_cena(X).
criterio_evento :- houve_evento.
criterio_habilidade(X) :- possui_habilidade_necessaria(X).
criterio_alibi(X) :- sem_alibi(X).

% Regra principal
culpado(X) :-
    criterio_cena(X),
    criterio_evento,
    criterio_habilidade(X),
    criterio_alibi(X).

% EXPLICAÇÃO 

explica_texto(X, Texto) :-
    findall(Linha, explicar_linha(X, Linha), Linhas),
    atomic_list_concat(Linhas, '\n', Texto).

explicar_linha(X, Linha) :-
    format(atom(Linha), 'Análise do suspeito: ~w', [X]).

explicar_linha(X, Linha) :-
    (na_cena(X) ->
        Linha = '- Estava na cena do crime' ;
        Linha = '- NÃO estava na cena do crime').

explicar_linha(_, Linha) :-
    (houve_evento ->
        Linha = '- Sensores confirmam ocorrência do crime' ;
        Linha = '- Nenhum evento detectado').

explicar_linha(X, Linha) :-
    (possui_habilidade_necessaria(X) ->
        Linha = '- Possui habilidades necessárias' ;
        Linha = '- NÃO possui habilidades necessárias').

explicar_linha(X, Linha) :-
    (sem_alibi(X) ->
        Linha = '- Não possui álibi confirmado' ;
        Linha = '- Possui álibi confirmado').

explicar_linha(X, Linha) :-
    (culpado(X) ->
        Linha = '   - Conclusão: CULPADO' ;
        Linha = '   - Conclusão: NÃO culpado').