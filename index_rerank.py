import os
import json
import numpy as np
from ollama import chat
from ollama import ChatResponse
from flashrank import Ranker, RerankRequest
from sentence_transformers import SentenceTransformer, util

FAQ_FILE = "data/faq_minecraft.json"
EMBEDDING_FILE = "data/faq_embeddings.npz"

# Função para carregar dados do FAQ
def load_faq_data():
    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Função para buscar perguntas mais similares
def get_top_k_similar_questions(model:SentenceTransformer, faq_data, user_input, top_k=3):
    top_results = []
    faq_embeddings = load_or_generate_embeddings(model, faq_data)
    user_question_embedding = model.encode(user_input, convert_to_tensor=True)
    results = util.semantic_search(user_question_embedding, faq_embeddings, top_k=top_k)
    for rank, result in enumerate(results[0]):
        if (result["score"] > 0.6):
            most_similar_idx = result["corpus_id"]
            most_similar_text = faq_data["faq"][most_similar_idx]["text"]
            most_similar_answer = faq_data["faq"][most_similar_idx]["answer"]
            top_results.append({"id": most_similar_idx, "text": most_similar_text, "answer": most_similar_answer})
    return top_results

# Função para carregar ou gerar embeddings
def load_or_generate_embeddings(model:SentenceTransformer, faq_data):
    if os.path.exists(EMBEDDING_FILE):
        data = np.load(EMBEDDING_FILE, allow_pickle=True)
        return data["embeddings"]
    
    faq_questions = [item["text"] for item in faq_data["faq"]]
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)
    np.savez_compressed(EMBEDDING_FILE, questions=faq_questions, embeddings=faq_embeddings)
    return faq_embeddings

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
        few_shot_string += f"Pergunta {rank + 1}: {result["text"]}\nResposta {rank + 1}: {result["answer"]}\n"
    
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

def main():
    # Carrega dados do json
    faq_data = load_faq_data()
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    ranker = Ranker()
        
    while True:
        user_input = input("O que você gostaria de saber? (digite '/sair' para finalizar): ")
        if user_input.strip().lower() == '/sair':
            print("Saindo do chat.")
            break
    
        # Buscar perguntas similares
        top_k_results = get_top_k_similar_questions(model, faq_data, user_input)
        
        # rerank as perguntas similares
        results = get_rerank(ranker, top_k_results, user_input)
        
        # Gerar o prompt para o modelo de chat
        prompt = generate_faq_prompt(results, user_input)
        
        print("*************** Exibindo o prompt gerado ***************")
        print(prompt)
        
        response: ChatResponse = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])

        if response and response.message:
            print(response.message.content)
        else:
            print("Desculpe, não consegui gerar uma resposta.")

if __name__ == "__main__":
    main()
