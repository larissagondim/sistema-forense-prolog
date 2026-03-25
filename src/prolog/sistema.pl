% Crimes
crime(roubo_quadro).
crime(furto_joia).

% Locais dos crimes
local_crime(roubo_quadro, sala_principal).
local_crime(furto_joia, sala_secundaria).

% Timeline da ocorrencia dum crime
evento(roubo_quadro, 10, sensor_laser).
evento(roubo_quadro, 12, sensor_peso).
evento(furto_joia, 20, sensor_peso).

% Presença (com tempo)
presente(larissa, sala_principal, 9).
presente(larissa, sala_principal, 11).
presente(maria, sala_principal, 10).
presente(laura, corredor, 10).
presente(laura, sala_secundaria, 20).

% Sensores com confiabilidade
sensor(sensor_laser, sala_principal, 0.9).
sensor(sensor_peso, sala_principal, 0.8).
sensor(sensor_peso, sala_secundaria, 0.7).

% Habilidades (nível)
habilidade(larissa, desativar_laser, 9).
habilidade(maria, manipular_objetos, 8).
habilidade(laura, manipular_objetos, 6).

% Álibis (tempo + confiança)
alibi(laura, 10, 0.9).
alibi(maria, 10, 0.3).

% Habilidades necessárias por crime
necessario(roubo_quadro, desativar_laser).
necessario(roubo_quadro, manipular_objetos).
necessario(furto_joia, manipular_objetos).

% REGRAS DE TIMELINE

% Pessoa estava na cena no momento do evento
na_cena(Crime, Pessoa) :-
    evento(Crime, Tempo, _),
    local_crime(Crime, Local),
    presente(Pessoa, Local, Tempo).

% Detecta coerência temporal
coerente_tempo(Pessoa, Crime) :-
    evento(Crime, TempoEvento, _),
    presente(Pessoa, _, TempoPessoa),
    Diff is abs(TempoEvento - TempoPessoa),
    Diff =< 2. % margem de erro

% EVENTO DO CRIME

grau_evento(Crime, Grau) :-
    findall(Conf,
        (evento(Crime, _, Sensor),
         sensor(Sensor, _, Conf)),
        Lista),
    media(Lista, Grau).

% HABILIDADE POR CRIME

grau_habilidade(Pessoa, Crime, Grau) :-
    findall(Peso,
        (necessario(Crime, H),
         habilidade(Pessoa, H, Nivel),
         Peso is Nivel / 10),
        Lista),
    (Lista = [] -> Grau = 0 ; media(Lista, Grau)).

% ÁLIBI TEMPORAL

grau_sem_alibi(Pessoa, Crime, Grau) :-
    evento(Crime, Tempo, _),
    (alibi(Pessoa, Tempo, Conf) ->
        Grau is 1 - Conf ;
        Grau = 1).

% MÉDIA

media(Lista, Media) :-
    sum_list(Lista, Soma),
    length(Lista, N),
    N > 0,
    Media is Soma / N.

% PONTUAÇÃO POR CRIME

pontuacao(Pessoa, Crime, Total) :-
    (na_cena(Crime, Pessoa) -> P1 = 1 ; P1 = 0),
    (coerente_tempo(Pessoa, Crime) -> P2 = 1 ; P2 = 0),

    grau_evento(Crime, P3),
    grau_habilidade(Pessoa, Crime, P4),
    grau_sem_alibi(Pessoa, Crime, P5),

    Total is (P1 * 0.25) +
             (P2 * 0.15) +
             (P3 * 0.2) +
             (P4 * 0.25) +
             (P5 * 0.15).

% CLASSIFICAÇÃO

nivel_suspeita(Pessoa, Crime, alta) :-
    pontuacao(Pessoa, Crime, P),
    P >= 0.7.

nivel_suspeita(Pessoa, Crime, media) :-
    pontuacao(Pessoa, Crime, P),
    P >= 0.4, P < 0.7.

nivel_suspeita(Pessoa, Crime, baixa) :-
    pontuacao(Pessoa, Crime, P),
    P < 0.4.

% RANKING POR CRIME

ranking(Crime, ListaOrdenada) :-
    setof((P, Pessoa),
        pontuacao(Pessoa, Crime, P),
        Lista),
    sort(0, @>=, Lista, ListaOrdenada).

% INFERÊNCIA REVERSA

% "Que tipo de pessoa conseguiria cometer esse crime?"

perfil_necessario(Crime, Perfil) :-
    findall(H, necessario(Crime, H), Habilidades),
    Perfil = perfil{
        habilidades: Habilidades,
        precisa_estar_na_cena: sim
    }.

% "Quem satisfaz parcialmente os requisitos?"
possivel_autor(Crime, Pessoa) :-
    habilidade(Pessoa, H, _),
    necessario(Crime, H).

% EXPLICAÇÃO AVANÇADA

explica(Pessoa, Crime, Texto) :-
    pontuacao(Pessoa, Crime, P),
    nivel_suspeita(Pessoa, Crime, Nivel),

    grau_evento(Crime, GE),
    grau_habilidade(Pessoa, Crime, GH),
    grau_sem_alibi(Pessoa, Crime, GA),

    format(atom(Texto),
'==== ANALISE FORENSE ====\n\
Crime: ~w\n\
Suspeito: ~w\n\
Pontuacao: ~2f\n\
Nivel: ~w\n\
\nDetalhes:\n\
- Presenca na cena: ~w\n\
- Coerencia temporal: ~w\n\
- Grau do evento: ~2f\n\
- Grau de habilidade: ~2f\n\
- Grau sem alibi: ~2f\n',
    [Crime, Pessoa, P, Nivel,
     (na_cena(Crime, Pessoa) -> 'SIM' ; 'NAO'),
     (coerente_tempo(Pessoa, Crime) -> 'SIM' ; 'NAO'),
     GE, GH, GA]).