# Project 5

## Configuração do Projeto

1. Clone o repositório:

   ```bash
   git clone $repos-url project-five
   cd project-five
   ```

## Ex00 – Embeddings para Otimizar a Busca de Informações

1. Entre no diretório `ex00`:

   ```bash
   cd ex00
   ```

2. Crie um ambiente virtual Python:

    ```bash
    python3.10 -m venv myenv
    source ./myenv/bin/activate
    ```

3. Instale as dependências:

   ```bash
   pip install -r ./requirements.txt
   ```

4. Prepare os currículos:

   - Crie a pasta `curriculos`:
   
     ```bash
     mkdir curriculos
     cd curriculos
     ```
   
   - Extraia o conteúdo do arquivo `curriculos.zip` nesta pasta.

5. Volte para o diretório `ex00`:

   ```bash
   cd ..
   ```

6. Execute o analisador de currículos:

   ```bash
   python ./resume_analyzer.py
   ```

7. Aguarde o processamento dos PDFs.

8. Insira sua consulta quando solicitado.

9. Ao final, lembre-se de desativar o ambiente virtual:

   ```bash
   deactivate
   ```

## Observações

- Certifique-se de que todos os currículos estejam no formato PDF para que o processamento seja feito corretamente.
- Utilize uma chave válida da API do Gemini para garantir que o processo de análise funcione corretamente.

---

## Ex01 – RAG: Busca Semântica e LLMs Entram em um Bar

1. Verifique se você está em um ambiente virtual. Se sim, desative-o:

   ```bash
   deactivate
   ```

2. Entre no diretório `ex01`:

   ```bash
   cd ex01
   ```

3. Crie um ambiente virtual Python:

   ```bash
   python3.10 -m venv myenv
   source ./myenv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r ./requirements.txt
   ```

5. Exporte sua API key do Groq com o comando:

   ```bash
   export GROQ_API_KEY=$YOUR_API_KEY
   ```

6. Rode o aplicativo com Streamlit:

   ```bash
   streamlit run resume_analyzer_app.py
   ```

7. Acesse o endereço fornecido pelo Streamlit para interagir com a aplicação.

---

## Notas Finais

- Certifique-se de que você tenha as permissões necessárias e uma chave API válida para o Groq antes de rodar a aplicação.
- Para desativar o ambiente virtual ao final do uso:

   ```bash
   deactivate
   ```
