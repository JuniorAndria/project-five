# Análise de currículos com RAG

## Visão geral do sistema
Este sistema é projetado para analisar currículos enviados em formato PDF e responder a perguntas sobre os candidatos. Utiliza técnicas de processamento de linguagem natural (NLP) e uma base de dados persistente para armazenar e consultar currículos.

## Componentes principais
1. **Interface do Usuário (Streamlit)**
   - Fornece uma interface web para os usuários enviarem currículos e fazerem perguntas sobre os candidatos.
   
2. **Processamento de PDF (pdfplumber)**
   - Extrai texto dos arquivos PDF enviados para análise posterior.

3. **Base de Dados (ChromaDB)**
   - Armazena os currículos processados e permite consultas eficientes.

4. **Função de Embedding (ChromaDB Embedding Functions)**
   - Converte o texto dos currículos em vetores numéricos para facilitar a comparação e a busca.

5. **API de Chat (Groq)**
   - Utiliza um modelo de linguagem para gerar respostas baseadas nos currículos armazenados.

## Conceitos principais
- **Processamento de Linguagem Natural (NLP)**: Técnicas usadas para processar e analisar grandes quantidades de dados de linguagem natural.
- **Embedding**: Representação de texto em forma de vetores numéricos que capturam o significado semântico.
- **Base de Dados Persistente**: Armazenamento de dados que mantém a integridade e a disponibilidade dos dados ao longo do tempo.

## Fluxo de funcionamento
1. **Envio de Currículo**: O usuário envia um ou mais arquivos PDF através da interface do Streamlit.
2. **Processamento de PDF**: Os arquivos PDF são processados para extrair o texto, que é então limpo e preparado.
3. **Armazenamento**: O texto extraído é armazenado na base de dados ChromaDB, com metadados associados.
4. **Consulta**: O usuário faz uma pergunta sobre os candidatos através da interface.
5. **Busca na Base de Dados**: A pergunta é usada para consultar a base de dados e recuperar currículos relevantes.
6. **Geração de Resposta**: Os currículos recuperados são usados para gerar uma resposta através da API de chat Groq.
7. **Exibição da Resposta**: A resposta gerada é exibida ao usuário na interface do Streamlit.