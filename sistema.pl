% Analisando a presença dos suspeitos

presente(diego, sala_principal).
presente(maria, sala_principal).
presente(saulo, corredor).


% Verificando o status dos sensores

sensor_ativado(laser, sala_principal).
sensor_ativado(peso, sala_principal).


% Verificando que habilidades técnicas possuem os suspeitos

habilidade(diego, desativar_laser).
habilidade(maria, manipular_objetos).
habilidade(saulo, limpeza).

% Verificando quais são os álibis

alibi_confirmado(saulo).


% Regras auxiliares

% Verificando se o suspeito estava na cena onde ocorreu o crime 

na_cena(X) :-
    presente(X, sala_principal).

%  Verifica a ocorrência de crime com base nos sensores

houve_evento :-
    sensor_ativado(_, sala_principal).

% Verifica se o suspeito possui habilidades necessárias

possui_habilidade_necessaria(X) :-
    habilidade(X, desativar_laser);
    habilidade(X, manipular_objetos).

% Verifica ausência de álibi

sem_alibi(X) :-
    \+ alibi_confirmado(X).

% Regra principal

% Um suspeito é considerado culpado se:
% - estava na cena do crime
% - possui habilidades necessárias
% - não possui álibi
% - houve evento confirmado pelos sensores

culpado(X) :-
    na_cena(X),
    houve_evento,
    possui_habilidade_necessaria(X),
    sem_alibi(X).

% Explicação porquê um suspeito é considerado culpado

explica(X) :-
    write('Análise do suspeito: '), write(X), nl,

    (na_cena(X) ->
        write('- Estava na cena do crime'), nl ;
        write('- NÃO estava na cena do crime'), nl),

    (houve_evento ->
        write('- Sensores confirmam ocorrência do crime'), nl ;
        write('- Nenhum evento detectado pelos sensores'), nl),

    (possui_habilidade_necessaria(X) ->
        write('- Possui habilidades necessárias'), nl ;
        write('- NÃO possui habilidades necessárias'), nl),

    (sem_alibi(X) ->
        write('- Não possui álibi confirmado'), nl ;
        write('- Possui álibi confirmado'), nl),

    (culpado(X) ->
        write('=> Conclusão: Suspeito é considerado CULPADO'), nl ;
        write('=> Conclusão: Suspeito NÃO é considerado culpado'), nl).