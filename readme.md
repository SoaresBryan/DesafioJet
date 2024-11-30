# README

## Desafio JetSales - Chatbot com FastAPI e Gemini

Este projeto implementa um chatbot especializado em componentes de computadores, representando exclusivamente a loja JetSales. O chatbot auxilia clientes na escolha dos melhores produtos, garantindo uma experiência de compra prática em uma interação humano-máquina.
### Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Como Usar](#como-usar)
  - [Front-end](#front-end)
  - [API Endpoints](#api-endpoints)
    - [POST /api/chat](#post-apichat)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Observações](#observações)
- [Contato](#contato)

---

## Pré-requisitos

- **Python 3.8** ou superior
- **MongoDB** em execução (local ou em nuvem)
- **Chave de API** válida para o modelo **Gemini**

---

## Instalação

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/seu-usuario/desafiojetsales.git
   ```

2. **Acesse o diretório do projeto:**

   ```bash
   cd desafiojetsales
   ```


3. **Instale as dependências do projeto:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

1. **Configurar Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```env
   MONGO_URI=seu_mongo_uri
   GEMINI_API_KEY=sua_chave_de_api_do_gemini
   endpoint = "endpoint_do_modelo_gemini"
   ```

   - **MONGO_URI**: A URI de conexão com o MongoDB. Exemplo para MongoDB local:

     ```
     MONGO_URI=mongodb://localhost:27017
     ```

   - **GEMINI_API_KEY**: Sua chave de API para acessar o modelo Gemini.

2. **Verifique a Conexão com o MongoDB:**

   Certifique-se de que o MongoDB esteja em execução e acessível via `MONGO_URI`.

---

## Execução

1. **Inicie a Aplicação FastAPI:**
    
   - Você pode inicar a aplicação apenas digitando o comando "run" no terminal python ou digitando no bash:
   ```bash
   uvicorn main:app --reload
   ```

   - O parâmetro `--reload` faz com que o servidor recarregue automaticamente ao detectar mudanças no código.

2. **Acesse a Aplicação no Navegador:**

   Abra o navegador e acesse:

   ```
   http://localhost:8000/
   ```

   - Você verá a interface do chatbot.

---

## Como Usar

### Front-end

1. **Tela de Login:**

   - Insira um **ID de usuário** no campo indicado e clique em **Entrar**.
   - Este ID será usado para rastrear seu histórico de conversas.

2. **Tela de Chat:**

   - Digite sua mensagem no campo "Digite sua mensagem..." e clique em **Enviar** ou pressione **Enter**.
   - As mensagens enviadas e as respostas do chatbot aparecerão na janela de chat.
   - Para encerrar a sessão, clique em **Sair**.

### API Endpoints

#### POST /api/chat

Endpoint para interação direta com o chatbot via API.

- **URL:** `/api/chat`
- **Método:** `POST`
- **Headers:**
  - `user-id` (string): O ID do usuário que está interagindo.
- **Parâmetros de Query:**
  - `mensagem` (string): A mensagem ou pergunta enviada pelo usuário.


**Parâmetros Detalhados:**

- **`user-id` (Header):**

  - **Descrição:** Identificador único do usuário. Usado para manter o histórico de conversas.
  - **Exemplo:** `usuario123`

- **`mensagem` (Query Parameter):**

  - **Descrição:** Texto da mensagem enviada pelo usuário.
  - **Exemplo:** `Qual melhor processador para jogos?`

**Resposta:**

- **Código 200 OK**

  - Retorna a resposta gerada pela IA em formato de texto simples.

- **Exemplo de Resposta:**

  ```
  Se você busca alto desempenho em jogos, o Intel Core i9-12900K é uma excelente opção. Ele oferece velocidades impressionantes e suporta os jogos mais exigentes. Você prefere priorizar desempenho ou está buscando algo com melhor custo-benefício?
  ```



## Estrutura do Projeto

```
desafiojetsales/
├── db/
│   ├── auth.py
│   ├── conexao_mongo.py
│   ├── models.py
│   └── utils_db.py
├── gemini/
│   └── conexao_gemini.py
├── routers/
│   └── chat.py
├── utils/
│   ├── funcoes.py
│   └── mongo_message_history.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── index.html
├── logs.py
├── main.py
├── requirements.txt
└── README.md
```

- **db/**: Módulos relacionados ao banco de dados MongoDB.
- **gemini/**: Integração com o modelo de linguagem Gemini.
- **routers/**: Rotas da API FastAPI.
- **utils/**: Funções utilitárias e classes auxiliares.
- **static/**: Arquivos estáticos para o front-end (CSS, JS, HTML).
- **logs.py**: Configuração de logs.
- **main.py**: Ponto de entrada da aplicação FastAPI.
- **requirements.txt**: Dependências do Python.
- **README.md**: Documentação do projeto.

---



## Contato

- **Nome:** Bryan Santana Soares
- **E-mail:** bryan.santana@souunit.com.br
- **LinkedIn:** https://www.linkedin.com/in/bryan-santana-soares-851442235/


