# Sistema Especialista para Investigação Forense em Museu (Prolog)

Este projeto realizado por Larissa Gondim, Laura Morais e Maria Luiza Uchoa do segundo período de Ciência da Computação implementa um sistema especialista em Prolog para auxiliar na investigação de um roubo em museu.

## Objetivo
Simular o processo investigativo por meio da correlação de evidências, identificando suspeitos com base em:
- Presença no local (oportunidade)
- Eventos detectados por sensores
- Habilidades necessárias para o crime
- Ausência de álibi
- Sistema de pontuação para averiguar principais suspeitos

## Tecnologias
- Prolog (SWI-Prolog)
- Python
- Streamlit (interface web)

## Estrutura

## Estrutura

```text
src/
├── python/
│   ├── app.py
│   └── main.py
└── prolog/
    └── sistema.pl
```

- `sistema.pl`: código principal do sistema especialista
- `main.py`: verificação interativa via terminal
- `app.py`: interface web interativa com Streamlit

## Funcionalidades 
- Identificação automática de suspeitos (`culpado/1`)
- Verificação de habilidades e presença
- Exclusão de suspeitos com álibi
- Explicação detalhada da decisão do sistema
- Suporte a múltiplos crimes
- Múltiplas cenas do crime
- Análise temporal (Timeline)
- Sistema de pontuação avançado
- Inserir o nome de um suspeito
- Ranking de suspeitos
- Inferência reversa
- Visualizar a explicação completa da análise diretamente na tela

## Como executar

**Prolog**
1. Abrir o arquivo no SWI-Prolog
2. Executar consultas como:

```prolog
?- culpado(X).
?- culpado(saulo).
?- possui_habilidade_necessaria(maria).
```

**Verificação via Terminal**
1. Instale as dependências
```
pip install pyswip
```
2. Execute o código python
```
python main.py
```

**Interface web**

1. Instale as dependências
```
pip install pyswip streamlit
```
2. Execute a aplicação:
```
streamlit run app.py
```
3. Acesse no navegador: 
```
http://localhost:0000
```
## Exemplo de uso

Entrada: 
```
larissa
```

Saída: 
```
Estava na cena do crime
Sensores confirmam o crime
Possui habilidades necessárias
Não possui álibi confirmado

Conclusão: CULPADO
```

## Objetivos
Este projeto tem fins acadêmicos, com foco na aplicação de sistemas especialistas e lógica de programação em um cenário investigativo.