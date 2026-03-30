:- dynamic presente/3.
:- dynamic situacao_digital/2.
:- dynamic profissao/2.
:- dynamic alibi_status/2.

crime(roubo_quadro).
local_crime(roubo_quadro, sala_principal).

suspeito(larissa).
suspeito(maria).
suspeito(laura).

pessoa(P) :- suspeito(P).

% Pesos de Evidência
peso_local(sala_principal, 3).
peso_local(sala_seguranca, 2).
peso_local(corredor, 1).

peso_digital(mensagens_apagadas, 3).
peso_digital(historico_apagado, 2).
peso_digital(fotos_recentes, 1).

peso_profissao(restauradora, 3).
peso_profissao(curadora, 2).
peso_profissao(historiadora, 1).

peso_alibi(nao, 4).
peso_alibi(sim, 0).

% Cálculos de Pontuação
pontuacao_local(Pessoa, _, Pontos) :-
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

pontuacao_total(Pessoa, Crime, Total) :-
    pontuacao_local(Pessoa, Crime, P1),
    pontuacao_digital(Pessoa, P2),
    pontuacao_profissao(Pessoa, P3),
    pontuacao_alibi(Pessoa, P4),
    Total is P1 + P2 + P3 + P4.

% Níveis de Suspeita
nivel_suspeita(Pessoa, Crime, alta) :- pontuacao_total(Pessoa, Crime, P), P >= 30.
nivel_suspeita(Pessoa, Crime, media) :- pontuacao_total(Pessoa, Crime, P), P >= 15, P < 30.
nivel_suspeita(Pessoa, Crime, baixa) :- pontuacao_total(Pessoa, Crime, P), P < 15.

ranking(Crime, ListaOrdenada) :-
    setof([P, Pessoa], (pessoa(Pessoa), pontuacao_total(Pessoa, Crime, P)), Lista),
    reverse(Lista, ListaOrdenada).

% Definições de Perfil Técnico
necessario(roubo_quadro, restauradora).
necessario(roubo_quadro, curadora).
necessario(roubo_quadro, historiadora).

perfil_necessario(Crime, Profissoes) :- findall(P, necessario(Crime, P), Profissoes).

% Ajustado: Verifica se a profissão da pessoa é UMA das necessárias para o crime
possivel_autor(Crime, Pessoa) :-
    pessoa(Pessoa),
    profissao(Pessoa, Prof),
    necessario(Crime, Prof).