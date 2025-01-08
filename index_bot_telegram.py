from telegram import Update
from dotenv import DotEnv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from ollama import chat
from ollama import ChatResponse
from flashrank import Ranker, RerankRequest
from sentence_transformers import SentenceTransformer
from flashrank import Ranker, RerankRequest
from sentence_transformers import SentenceTransformer
from services.qdrant import QdrantDatabase, QdrantOperations

dotenv = DotEnv()
BOT_TOKEN = dotenv.get("BOT_TOKEN")

# Função para buscar perguntas mais similares
def get_top_k_similar_questions(model: SentenceTransformer, user_input: str, qdrantDatabase: QdrantDatabase, limit=3):
    top_results = []
    hits = qdrantDatabase._client.query_points(collection_name="faq_minecraft", query=model.encode(user_input).tolist(), limit=limit).points
    for hit in hits:
        id = hit.id
        text = hit.payload["text"]
        answer = hit.payload["answer"]
        top_results.append({"id": id, "text": text, "answer": answer})
    return top_results

# Função para rerank as perguntas mais similares
def get_rerank(ranker: Ranker, top_results, user_input):
    if not top_results: return []

    rerankrequest = RerankRequest(query=user_input, passages=top_results)
    results = ranker.rerank(rerankrequest)
    return results


# Função para gerar o prompt de FAQ
def generate_faq_prompt(results, user_input):
    few_shot_string = ""
    for rank, result in enumerate(results):
        few_shot_string += f"Pergunta {rank + 1}: {result['text']}\nResposta {rank + 1}: {result['answer']}\n"
    
    prompt = f"""
Você é um assistente de FAQ. Sua tarefa é fornecer respostas precisas e concisas com base nas perguntas e respostas armazenadas em nossa base de dados.

### Instruções:
1. Avalie as Perguntas e Respostas mais similares encontradas em nossa base de dados, então direto responda ao usuário.
2. Caso não encontre dados similares ou indadequados, responda ao usuário: Não sei.
3. Apenas forneça informações que estejam diretamente relacionadas às Perguntas e Respostas fornecidas.
4. Evite respostas fora do contexto da FAQ ou informações não solicitadas.

### Perguntas e Respostas mais similares encontradas:
{few_shot_string or "Nenhum dado similar encontrado"}

### Pergunta do Usuário:
"{user_input}"

### Resposta: """
    
    return prompt

# Função para lidar com mensagens recebidas pelo bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    qdrantDatabase = QdrantDatabase()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    ranker = Ranker()

    # Função para buscar perguntas mais similares
    top_k_results = get_top_k_similar_questions(model, user_input, qdrantDatabase)

    # rerank as perguntas similares
    results = get_rerank(ranker, top_k_results, user_input)
        
    # Gerar o prompt para o modelo de chat
    prompt = generate_faq_prompt(results, user_input)

    response: ChatResponse = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])

    if response and response.message:
        await update.message.reply_text(response.message.content)
    else:
        await update.message.reply_text("Desculpe, não consegui gerar uma resposta.")

# Função para lidar com o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context)
    await update.message.reply_text("Olá! Sou um assistente de FAQ sobre o jogo Minecraft. Envie uma pergunta para começar!")

# Função principal
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
