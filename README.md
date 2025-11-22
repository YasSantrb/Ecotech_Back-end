# Ecotech_Back-end
Repositório destinado ao desenvolvimento do back-end do site ECOTECH.

## 🛠️ Etapas Necessárias para Configurar e Acessar a API Localmente

1.  **Clone o repositório:**
    ```
    git clone https://github.com/YasSantrb/Ecotech_Back-end.git
    ```

2.  **Crie o Ambiente Virtual (VEnv):**
    Entre no diretório do repositório clonado e execute o comando para criar o ambiente virtual:
    ```
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**
    Utilize o comando correspondente ao seu sistema operacional:
    * **Windows:**
        ```
        venv\Scripts\activate
        ```

4.  **Instale as Dependências:**
    Instale todos os pacotes necessários listados no `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```

5.  **Aplique as Migrações do Banco de Dados:**
    Execute este comando para criar as tabelas no banco de dados local (SQLite):
    ```
    python manage.py migrate
    ```

6.  **Inicie o Servidor de Desenvolvimento:**
    Execute o comando para iniciar o servidor do Django. O projeto estará acessível em **http://127.0.0.1:8000/**.
    ```
    python manage.py runserver
    ```
