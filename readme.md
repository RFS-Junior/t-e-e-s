# FAQ Assistente com Qdrant e Ollama

Este projeto implementa um assistente de FAQ utilizando Qdrant para armazenar perguntas e respostas, e Ollama para fornecer respostas baseadas em similaridade com as questões enviadas pelo usuário.

## Tecnologias

- **Qdrant**: Banco de dados vetorial.
- **Ollama**: Modelo de linguagem para gerar respostas.
- **Sentence-Transformers**: Para gerar embeddings e calcular similaridade.
- **FlashRank**: Para reordenar as perguntas encontradas.
- **Docker**: Para rodar o Qdrant em container.

## Como Configurar

### 1. Rodar o Qdrant com Docker

Para rodar o Qdrant em um container Docker, use o seguinte comando:

```bash
docker run -p 6333:6333 -p 6334:6334 -v /qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

Isso vai iniciar o Qdrant nas portas `6333` (API) e `6334` (cliente de pesquisa).

### 2. Configurar o Ambiente Virtual (venv)

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- **No Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```

- **No Windows**:
  ```bash
  venv\Scripts\activate
  ```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as dependências necessárias, como `qdrant-client`, `sentence-transformers`, `flashrank` e `ollama`.

### 4. Carregar o FAQ no Qdrant

Execute o script `script_save_qdrant.py` para carregar as perguntas e respostas no Qdrant:

```bash
python script_save_qdrant.py
```

### 5. Executar o Assistente

Execute o script `main.py` para iniciar o chat interativo:

```bash
python main.py
```

O assistente irá buscar as perguntas mais similares e fornecer respostas baseadas no FAQ armazenado.

## Personalizações

- **FAQ**: Edite o arquivo `data/faq_minecraft.json` para adicionar ou modificar perguntas e respostas.