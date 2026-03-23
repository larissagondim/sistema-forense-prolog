# Sistema Especialista para Investigação Forense em Museu (Prolog)

Este projeto implementa um sistema especialista em Prolog para auxiliar na investigação de um roubo em museu.

## Objetivo
Simular o processo investigativo por meio da correlação de evidências, identificando suspeitos com base em:
- Presença no local (oportunidade)
- Eventos detectados por sensores
- Habilidades necessárias para o crime
- Ausência de álibi

## Tecnologias
- Prolog (SWI-Prolog)

## Estrutura
- `sistema.pl`: código principal do sistema especialista

## Como executar
1. Abrir o arquivo no SWI-Prolog
2. Executar consultas como:

```prolog
?- culpado(X).
?- culpado(saulo).
?- possui_habilidade_necessaria(maria).