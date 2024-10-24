import streamlit as st
import pdfplumber
import re
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import os
import time
import json 

embedding_function = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(name="curriculo", embedding_function=embedding_function)

groq_key = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=groq_key)

def send_groq_prompt(content):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente que responderá a perguntas sobre currículos. Obedeça exatamente as instruções fornecidas.",
            },
            {
                "role": "user",
                "content": content,
            },
            {
                "role": "assistant",
                "content": "Com base na análise dos currículos fornecidos, as seguintes informações podem ser úteis para responder à sua pergunta:",
            }
        ],
        model="llama3-8b-8192",
        stream=True
    )
    return chat_completion

def send_groq_metadata_prompt(content):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Você deverá fornecer a metadata do currículo e retornar em formato JSON. "
                ),
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

def create_prompt(question, curriculos):
    prompt = f"""
        Você é um especialista em análise de currículos para seleção de candidatos. Baseie suas respostas exclusivamente nas informações fornecidas nos currículos, seguindo as diretrizes abaixo.
        Você responderá a perguntas sobre os candidatos com base em suas experiências, habilidades e formação acadêmica. Seja objetivo e preciso em suas respostas.
        <specific_question>\n
        {question}\n
        </specific_question>\n
        <curriculos>\n
        {curriculos}\n
        </curriculos>\n
        <instructions>
        1. Responda exclusivamente com as informações que estão contidas nos currículos fornecidos dentro da tag <curriculos>. Não adicione informações externas ou suposições.
        2. Seja objetivo, direto e preciso em suas respostas. Não inclua explicações detalhadas ou justificativas.
        3. Evite qualquer forma de reescrever a pergunta. Responda diretamente com a informação solicitada.
        4. Caso a pergunta seja sobre a seleção de um candidato específico, não mencione ou compare com outros candidatos. Foque apenas no candidato mencionado ou no que melhor se encaixa, e explique brevemente o motivo sem citar outros.
        5. Não compartilhe informações pessoais, detalhes confidenciais ou irrelevantes. Apenas fatos relacionados à pergunta e ao perfil profissional dos candidatos.
        6. Mantenha o tom profissional e informativo em todas as respostas.
        7. Não resuma a pergunta ou forneça uma visão geral; limite-se a responder diretamente o que foi solicitado, com precisão.
        8. Ao tratar de escolhas ou preferências, mencione apenas o candidato que melhor se encaixa sem comparações implícitas ou explícitas com outros perfis.
        9. Não faça comparações, apenas responda oque foi perguntado.
        </instructions>
        <examples>
        Pergunta: Qual a experiência do candidato com Python?\n
        Resposta: O candidato possui 5 anos de experiência com Python.\n

        Pergunta: Qual a formação acadêmica do candidato?\n
        Resposta: O candidato possui graduação em Engenharia de Software.\n

        Pergunta: Qual o melhor candidato para a vaga de Python?\n
        Resposta: O candidato Albert é o mais adequado para a vaga de Python, devido à sua experiência abrangente na linguagem e projetos relevantes.\n

        Pergunta: O candidato João possui experiência com liderança?\n
        Resposta: Sim, o candidato João possui 3 anos de experiência em liderança de equipes de desenvolvimento.\n
        </examples>
    """
    return send_groq_prompt(prompt)

def process_pdf_file_to_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text_page = page.extract_text()
            if text_page:
                text_page_cleaned = clean_text(text_page)
                if text_page_cleaned.strip():
                    text += text_page_cleaned
    return text

def clean_text(text):
    page_number_pattern = r"Página\s+\d+\s+de\s+\d+\n"
    return re.sub(page_number_pattern, '', text)

def extract_metadata_from_text(text):
    prompt = f"""
    Você deverá retornar a resposta com a metadata do currículo em formato JSON.
    Siga o exemplo de como deve ser formatado:
    <example>
    {{
        "nome": "João da Silva",
        "email": "joao.silva@example.com",
        "telefone": "(11) 99999-9999",
        "endereco": "Rua dos Bobos, 0",
        "linguagens_programacao": "Python, JavaScript, Java",
        "formacao_academica": "Engenharia de Software, Ciência da Computação]"
        "experiencia_profissional": "Desenvolvedor Full Stack, Analista de Dados",
        "habilidades": "Comunicação, Trabalho em Equipe",
        "idiomas": "Inglês, Espanhol"
    }}
    </example>
    <instructions>
    1. Você deverá retornar somente a metadata do currículo em formato JSON.
    2. Nada mais. Sua resposta deve começar com {{ e terminar com }}.
    3. De maneira alguma deve ter [ ou ] na resposta. 
    4. Não adicione informações extras.
    5. O objeto deverá ser obrigatoriamente um JSON válido e não deverá conter listas apenas strings nas propriedades.
    </instructions>
    <curriculo>
    {text}
    </curriculo>
    """
    
    metadata_str = send_groq_metadata_prompt(prompt)
    try:
        metadata = json.loads(metadata_str)
        return metadata
    except json.JSONDecodeError as e:
        return {}


def add_curriculo_to_collection(text, file_id):
    existing_ids = [doc_id for doc_id in collection.get()["ids"]]
    if file_id not in existing_ids:
        try: 
            metadata = extract_metadata_from_text(text)
            metadata["source"] = file_id
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[file_id]
            )
        except Exception as e:
            metadata = {"source": file_id}
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[file_id]
            )
        st.success(f"Currículo {file_id} adicionado com sucesso!")
    else:
        st.warning(f"O currículo {file_id} já existe na coleção.")

def curriculo_upload():
    uploaded_files = st.file_uploader("Envie um currículo em PDF:", type="pdf", accept_multiple_files=True, key=None)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text = process_pdf_file_to_text(uploaded_file)
            if text.strip():
                file_id = uploaded_file.name
                add_curriculo_to_collection(text, file_id)

def query_curriculos(question):
    results = collection.query(
        query_texts=[question],
        include=["documents"],
        n_results=3
    )
    if results["documents"]:
        curriculos = "\n\n".join(results["documents"][0])
        response_stream = create_prompt(question, curriculos)
        stream_response(response_stream)
    else:
        st.write("Nenhum resultado encontrado.")

def stream_response(response_stream):
    response_placeholder = st.empty()
    response_text = ""

    for message_chunk in response_stream:
        part = getattr(message_chunk.choices[0].delta, 'content', None)
        if part:
            response_text += part
            response_placeholder.markdown(response_text)
        time.sleep(0.05)

def main():
    st.title("Análise de Currículos")
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox("Escolha uma ação:", ("Enviar Currículo", "Consultar Currículos"))

    if option == "Enviar Currículo":
        curriculo_upload()
    elif option == "Consultar Currículos":
        query_text = st.text_input("Faça uma pergunta sobre os candidatos:")
        if query_text:
            query_curriculos(query_text)

if __name__ == '__main__':
    main()
