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

### 2. Instalar Ollama

Você precisa instalar o Ollama para interagir com os modelos de linguagem, como o Llama 3.2 ou outro modelo de sua preferência.

1. **Instalar o Ollama**: Siga as instruções de instalação na [página oficial do Ollama](https://ollama.com/).
   
2. **Rodar o Modelo**: Execute o modelo Llama 3.2 ou outro modelo de sua preferência. Caso queira usar outro modelo, altere o nome do modelo no código (veja o próximo passo).

### 3. Configurar o Ambiente Virtual (venv)

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

### 4. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as dependências necessárias, como `qdrant-client`, `sentence-transformers`, `flashrank` e `ollama`.

### 5. Carregar o FAQ no Qdrant

Execute o script `script_save_qdrant.py` para carregar as perguntas e respostas no Qdrant:

```bash
python script_save_qdrant.py
```

### 6. Executar o Assistente

Execute o script `main.py` para iniciar o chat interativo:

```bash
python main.py
```

O assistente irá buscar as perguntas mais similares e fornecer respostas baseadas no FAQ armazenado.

#### Alteração no Código para Rodar o Modelo Correto

No arquivo `main.py`, na linha onde a resposta é gerada, substitua o modelo Llama 3.2 ou outro modelo de sua preferência. A linha original:

```python
response: ChatResponse = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
```

Deve ser alterada para o modelo desejado, por exemplo, se você quiser usar um modelo diferente, como `gemma` (caso esteja disponível):

```python
response: ChatResponse = chat(model='gemma', messages=[{'role': 'user', 'content': prompt}])
```

## Personalizações

- **FAQ**: Edite o arquivo `data/faq_minecraft.json` para adicionar ou modificar perguntas e respostas.