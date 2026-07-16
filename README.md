# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e PostgreSQL (pgVector)

Este repositório contém uma solução completa para **Ingestão de Documentos PDF** e **Busca Semântica (RAG - Retrieval-Augmented Generation)** utilizando o framework **LangChain**, banco de dados relacional **PostgreSQL** com a extensão de vetores **pgVector**, e modelos de Linguagem de Grande Porte (LLMs).

O objetivo principal é permitir que usuários façam perguntas através de uma interface de linha de comando (CLI) e recebam respostas precisas baseadas *exclusivamente* no conteúdo de um documento PDF fornecido, evitando alucinações por meio de diretrizes rígidas de contexto.


## 🎯 Objetivo do Projeto

1. **Ingestão Eficiente**: Ler e processar um arquivo PDF (`document.pdf`), segmentá-lo em blocos (chunks), gerar vetores de alta dimensão (embeddings) e armazená-los de forma estruturada no PostgreSQL usando `pgVector`.
2. **Busca Semântica Baseada em Contexto (RAG)**: Consultar o banco vetorial pelas sentenças mais semelhantes à pergunta do usuário ($k=10$) e submeter esse contexto a uma LLM (OpenAI ou Gemini) sob regras severas de restrição de domínio.


## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Framework de IA:** LangChain (`langchain-core`, `langchain-community`, `langchain-postgres`)
*   **Banco de Dados:** PostgreSQL + extensão `pgvector`
*   **Infraestrutura Local:** Docker & Docker Compose
*   **Provedores de LLM & Embeddings:** OpenAI (Embedding: `text-embedding-3-small` / LLM: `gpt-5-nano`) ou Google Gemini (Embedding: `models/embedding-001` / LLM: `gemini-2.5-flash-lite`)



## 📁 Estrutura do Repositório

```text
├── docker-compose.yml     # Orquestração do banco PostgreSQL + pgVector
├── requirements.txt       # Dependências do projeto (LangChain, psycopg, etc.)
├── .env.example           # Template de configuração das chaves de API e banco de dados
├── document.pdf           # Documento de origem para a base de conhecimento
├── README.md              # Instruções de execução (este arquivo)
└── src/
    ├── ingest.py          # Script responsável pelo processamento e armazenamento vetorial do PDF
    ├── search.py          # Módulo auxiliar para realizar buscas e consultas à LLM
    └── chat.py            # CLI iterativo para conversar com os dados em tempo real

```



## 🚀 Como Executar o Projeto

Siga os passos abaixo para preparar o ambiente e rodar a aplicação localmente:

### 1. Configurar o Ambiente Virtual (VirtualEnv)

Crie e ative um ambiente virtual isolado para evitar conflitos de dependências:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar no Linux/macOS:
source venv/bin/activate

# Ativar no Windows (PowerShell):
.\\\\venv\\\\Scripts\\\\Activate.ps1

```

### 2. Instalar as Dependências

Instale todos os pacotes obrigatórios e recomendados:

```bash
pip install -r requirements.txt

```

> **💡 Dica:** Para instalar uma nova biblioteca e já atualizar o `requirements.txt`, use:
> ```bash
> pip install <nome_da_lib> && pip freeze > requirements.txt
> ```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha com as suas credenciais de API (OpenAI ou Gemini):

```bash
cp .env.example .env

```

*Edite o arquivo `.env` inserindo sua `OPENAI_API_KEY` ou `GOOGLE_API_KEY`, bem como os dados de conexão do PostgreSQL.*

### 4. Subir o Banco de Dados

Certifique-se de ter o Docker instalado e execute o comando para iniciar o PostgreSQL com suporte a vetorização:

```bash
docker compose up -d

```

### 5. Executar a Ingestão do PDF

Alimente o banco de dados carregando o arquivo `document.pdf`:

```bash
python src/ingest.py

```

*Este script divide o documento em chunks de 1000 caracteres (com overlap de 150), gera as representações vetoriais e as salva no banco.*

### 6. Iniciar o Chat via CLI

Abra o terminal interativo para fazer perguntas ao documento:

```bash
python src/chat.py

```



## 💬 Exemplo de Uso no Terminal

**Interação Dentro do Contexto:**

```text
Faça sua pergunta:
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

```

**Interação Fora do Contexto (Tratamento de Alucinações):**

```text
Faça sua pergunta:
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

```



## 🔒 Regras de Negócio do Chat (Prompt Guardrails)

Para garantir respostas extremamente fiéis ao documento, o sistema utiliza uma engenharia de prompt restrita:

* **Exclusividade de Contexto:** A LLM responderá apenas com base nas informações contidas no bloco de contexto recuperado do banco.
* **Resposta Padrão para Desvios:** Qualquer pergunta cujo conteúdo não esteja explícito no documento, ou que solicite opiniões e conhecimentos externos, retornará obrigatoriamente a frase: *"Não tenho informações necessárias para responder sua pergunta."*
"""
