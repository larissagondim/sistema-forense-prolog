# Sistema Especialista para Investigação Forense em Museu (Prolog)

Este projeto foi desenvolvido por Larissa Gondim, Laura Morais e Maria Luiza Uchoa, alunas do segundo período de Ciência da Computação na UFPB. O sistema utiliza lógica de programação para auxiliar na investigação de crimes em um cenário de museu.

## Objetivo
O sistema simula um processo investigativo correlacionando evidências para identificar suspeitos com base em:
* Presença no local e análise de oportunidade.
* Eventos detectados e vestígios digitais.
* Habilidades técnicas compatíveis com o crime.
* Ausência ou presença de álibi.
* Sistema de pontuação para classificação de níveis de suspeita.

## Tecnologias
* Prolog (SWI-Prolog) para o motor de inferência.
* Python para integração e lógica de sistema.
* Streamlit para a interface web interativa.
* PySwip para a comunicação entre Python e Prolog.

## Estrutura do projeto
O projeto está organizado na seguinte estrutura de diretórios:

```text
src/
├── python/
│   ├── app.py      (Interface Web)
│   └── main.py     (Interface CLI)
└── prolog/
    └── sistema.pl  (Base de Conhecimento e Regras)
```

## Funcionalidades
O sistema oferece ferramentas completas para a análise forense:
* **Ranking de Suspeitos**: Ordenação de indivíduos por nível de suspeita (Alta, Média ou Baixa) baseada em pontuação acumulada.
* **Explicação Detalhada**: O sistema gera um relatório textual explicando os motivos da pontuação de cada suspeito (Local, Digital, Profissão e Álibi).
* **Inferência Reversa**: Identifica quais habilidades são necessárias para um crime específico e quais pessoas as possuem.
* **Suporte a Múltiplos Crimes**: Capacidade de analisar diferentes tipos de ocorrências, como roubo de quadros ou furtos de joias.
* **Análise de Presença**: Cruzamento de dados de localização e horário para determinar a viabilidade da autoria.

## Como executar?

### Pré-requisitos
É necessário ter o SWI-Prolog instalado no sistema e as dependências Python:
```bash
pip install pyswip streamlit
```

### Interface de Terminal (CLI)
Para executar a verificação interativa via terminal:
```bash
python src/python/main.py
```

### Interface Web (Streamlit)
Para executar a aplicação no navegador:
```bash
streamlit run src/python/app.py
```

## Exemplo de Inferência
Ao consultar um suspeito como **Larissa**, o sistema analisa os fatos na base `sistema.pl`:
* **Entrada**: Seleção do crime e nome do suspeito.
* **Processamento**: O Prolog verifica que a pessoa estava na sala principal, possui a profissão de restauradora, tem mensagens apagadas e possui álibi confirmado.
* **Saída**: Gera uma pontuação total e classifica o nível de suspeita, fornecendo a justificativa detalhada de cada ponto.

## Objetivos acadêmicos
Este projeto foi desenvolvido com fins didáticos para a disciplina Lógica aplicada à Ciência da Computação, focando na aplicação de sistemas especialistas em cenários reais de tomada de decisão baseada em regras.

