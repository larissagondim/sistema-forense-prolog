% CRIMES
crime(roubo_quadro).
crime(furto_joia).

% LOCAIS DOS CRIMES
local_crime(roubo_quadro, sala_principal).
local_crime(furto_joia, sala_secundaria).

% PRESENCA (PESSOA, LOCAL, HORA)
presente(larissa, sala_principal, 9).
presente(larissa, sala_principal, 11).
presente(maria, sala_principal, 10).
presente(laura, corredor, 10).
presente(laura, sala_secundaria, 20).

% DOMINIO DE PESSOAS
pessoa(P) :- presente(P, _, _).

% PESOS E CARACTERÍSTICAS:

% LOCAL
peso_local(sala_principal, 3).
peso_local(sala_seguranca, 2).
peso_local(corredor, 1).
peso_local(sala_secundaria, 0).

% SITUACAO DIGITAL
situacao_digital(larissa, mensagens_apagadas).
situacao_digital(maria, historico_apagado).
situacao_digital(laura, fotos_obra).

peso_digital(mensagens_apagadas, 3).
peso_digital(historico_apagado, 2).
peso_digital(fotos_obra, 1).

% PROFISSAO
profissao(larissa, restauradora).
profissao(maria, curadora).
profissao(laura, historiadora).

peso_profissao(restauradora, 3).
peso_profissao(curadora, 2).
peso_profissao(historiadora, 1).

% ALIBI
alibi_status(larissa, sim).
alibi_status(maria, sim).
alibi_status(laura, nao).

peso_alibi(nao, 4).
peso_alibi(sim, 0).

% REGRAS DE PONTUAÇÃO

pontuacao_local(Pessoa, Crime, Pontos) :-
    local_crime(Crime, Local),
    presente(Pessoa, Local, _),
    peso_local(Local, Pontos), !.
pontuacao_local(_, _, 0).

pontuacao_digital(Pessoa, Pontos) :-
    situacao_digital(Pessoa, Tipo),
    peso_digital(Tipo, Pontos), !.
pontuacao_digital(_, 0).

pontuacao_profissao(Pessoa, Pontos) :-
    profissao(Pessoa, Prof),
    peso_profissao(Prof, Pontos), !.
pontuacao_profissao(_, 0).

pontuacao_alibi(Pessoa, Pontos) :-
    alibi_status(Pessoa, Status),
    peso_alibi(Status, Pontos), !.
pontuacao_alibi(_, 0).

% HABILIDADES E REQUISITOS

habilidade(larissa, desativar_laser, 9).
habilidade(maria, manipular_objetos, 8).
habilidade(laura, manipular_objetos, 6).

necessario(roubo_quadro, desativar_laser).
necessario(roubo_quadro, manipular_objetos).
necessario(furto_joia, manipular_objetos).

% LOGICA DE INFERÊNCIA

pontuacao_total(Pessoa, Crime, Total) :-
    pontuacao_local(Pessoa, Crime, P1),
    pontuacao_digital(Pessoa, P2),
    pontuacao_profissao(Pessoa, P3),
    pontuacao_alibi(Pessoa, P4),
    Total is P1 + P2 + P3 + P4.

nivel_suspeita(Pessoa, Crime, alta) :-
    pontuacao_total(Pessoa, Crime, P), P >= 8.
nivel_suspeita(Pessoa, Crime, media) :-
    pontuacao_total(Pessoa, Crime, P), P >= 4, P < 8.
nivel_suspeita(Pessoa, Crime, baixa) :-
    pontuacao_total(Pessoa, Crime, P), P < 4.

% RANKING
ranking(Crime, ListaOrdenada) :-
    findall([P, Pessoa],
        (pessoa(Pessoa), pontuacao_total(Pessoa, Crime, P)),
        Lista),
    Lista \= [], 
    sort(1, @>=, Lista, ListaOrdenada).

% EXPLICACAO
explica(Pessoa, Crime, Texto) :-
    pontuacao_total(Pessoa, Crime, P),
    nivel_suspeita(Pessoa, Crime, Nivel),
    pontuacao_local(Pessoa, Crime, PL),
    pontuacao_digital(Pessoa, PD),
    pontuacao_profissao(Pessoa, PP),
    pontuacao_alibi(Pessoa, PA),
    format(atom(Texto),
'==== ANALISE FORENSE ====~n\
Crime: ~w~n\
Suspeito: ~w~n\
Pontuacao Total: ~w~n\
Nivel: ~w~n\
~nDetalhes:~n\
- Local: ~w~n\
- Digital: ~w~n\
- Profissao: ~w~n\
- Alibi: ~w~n',
    [Crime, Pessoa, P, Nivel, PL, PD, PP, PA]).

% INFERENCIA REVERSA
perfil_necessario(Crime, Habilidades) :-
    findall(H, necessario(Crime, H), Habilidades).

possivel_autor(Crime, Pessoa) :-
    pessoa(Pessoa),
    forall(necessario(Crime, H), habilidade(Pessoa, H, _)).