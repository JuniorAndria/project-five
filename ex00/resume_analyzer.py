import chromadb
from chromadb.utils import embedding_functions
import os
import pdfplumber
import re

embedding_function  = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="./chromadb")
collection_name = "my_collection"
if collection_name in [c.name for c in client.list_collections()]:
    client.delete_collection(name=collection_name)
collection = client.create_collection(name=collection_name, embedding_function=embedding_function)

def extract_text_without_page_numbers(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text_page = page.extract_text()
            if text_page:
                page_number_pattern = r"Página\s+\d+\s+de\s+\d+\n+"
                text_page_cleaned = re.sub(page_number_pattern, '', text_page)
                if text_page_cleaned.strip():
                    text += text_page_cleaned + "\n"
    return text

def sort_key(filename):
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', filename)]


def process_pdf_directory():
    pdf_directory = "curriculos"
    pdfs = [os.path.abspath(os.path.join(root, f)) 
        for root, _, files in os.walk(pdf_directory) 
        for f in files if f.endswith(".pdf")]
    print("Encontrados %d arquivos PDF no diretório." % len(pdfs))
    pdfs = sorted(pdfs, key=sort_key)

    for index, pdf_file in enumerate(pdfs, start=1):
        name = pdf_file.split("/")[-1]
        print("Processando PDF %d/%d: %s" % (index, len(pdfs), name))
        pdf_path = os.path.join(pdf_directory, pdf_file)
        text = extract_text_without_page_numbers(pdf_path)
        if text.strip():
            collection.add(
                documents=[text],
                metadatas=[{"source": name}],
                ids=[f"pdf_{index}"]
            )
            print(f"    - Documento {name} processado e armazenado.")
    print("Processamento de todos os PDFs concluído.")
    print("Processamento concluído. Iniciando modo de consulta.")

def query_text(text):
    results = collection.query(
        query_texts=[text], 
        n_results=3,
    )
    returned_results = []
    for i in range(len(results['ids'][0])):
        document = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        returned_results.append((document, metadata))
    
    return returned_results

def  interactive_query_loop():
    print("Digite sua consulta ou 'sair' para encerrar.")
    while True:
        query = input("\nConsulta: ")
        if query.lower() == 'sair':
            break
        results = query_text(query)
        print("\nResultados:")
        for document, metadata in results:
            print(f"Documento: {metadata['source']}")
            print(f"Trecho: {document[:200]}...")
            print()

def main():
    process_pdf_directory()
    interactive_query_loop()


if __name__ == "__main__":
    main()
