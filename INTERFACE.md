# Interface React — Sistema de Investigação Forense

Interface web alternativa ao Streamlit, construída com **React + Vite + Tailwind CSS** no frontend e **FastAPI** no backend, que se comunica com o motor Prolog (`sistema.pl`) via pyswip.

## Arquitetura

```
React (porta 5173)  →  FastAPI (porta 8000)  →  SWI-Prolog (sistema.pl)
```

O frontend React faz chamadas HTTP para a API FastAPI, que executa as queries no Prolog e retorna os resultados em JSON.

## Estrutura dos arquivos

```text
src/
├── api/
│   └── server.py          ← Backend FastAPI (endpoints REST)
├── react/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── index.css
│       ├── App.jsx
│       └── components/
│           ├── StorySection.jsx    ← Narrativa do caso
│           ├── CharacterCard.jsx   ← Cards dos suspeitos
│           └── ResultReveal.jsx    ← Resultado da análise
└── prolog/
    └── sistema.pl          ← Lógica Prolog (inalterado)
```

## Fluxo da aplicação

1. **História** — O usuário lê a narrativa do roubo no museu (local do crime, sensores ativados, contexto).
2. **Suspeitos** — São apresentados cards com o perfil de cada suspeita (localização, habilidade, álibi). O usuário seleciona quem acredita ser a culpada.
3. **Resultado** — O sistema consulta o Prolog via API, revela se o palpite estava correto e exibe a análise completa com pontuação de todas as suspeitas.

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/suspeitos` | Retorna todos os suspeitos com pontuação e nível de suspeita |
| GET | `/api/explicacao/{nome}` | Retorna a explicação detalhada da análise de um suspeito |

## Pré-requisitos

- **SWI-Prolog** instalado (`brew install swi-prolog`)
- **Python 3** com os pacotes: `pyswip`, `fastapi`, `uvicorn`
- **Node.js** (v18+) com npm

## Passo a passo para rodar

### 1. Instalar dependências Python

```bash
pip install pyswip fastapi uvicorn
```

### 2. Instalar dependências do React

```bash
cd src/react
npm install
```

### 3. Iniciar o backend (Terminal 1)

```bash
cd src/api
python -m uvicorn server:app --reload --port 8000
```

O servidor estará disponível em `http://localhost:8000`.

### 4. Iniciar o frontend (Terminal 2)

```bash
cd src/react
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

### 5. Acessar a aplicação

Abra o navegador em:

```
http://localhost:5173
```

## Tecnologias utilizadas

- **React** — Biblioteca para construção da interface
- **Vite** — Bundler e servidor de desenvolvimento
- **Tailwind CSS** — Framework de estilização utilitária
- **FastAPI** — Framework Python para a API REST
- **pyswip** — Ponte Python ↔ SWI-Prolog
- **SWI-Prolog** — Motor de inferência lógica
