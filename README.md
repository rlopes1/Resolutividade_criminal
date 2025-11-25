# Análise de Potencial de Investigação

Esta aplicação funciona como uma ferramenta de apoio à decisão, projetada para auxiliar na avaliação do **potencial de investigação** de uma ocorrência recém-registrada. Com base nas informações iniciais, o sistema classifica a ocorrência em **Alta**, **Média** ou **Baixa** viabilidade, fornecendo um indicativo da probabilidade de uma investigação futura ser bem-sucedida. O objetivo é otimizar a alocação de recursos e direcionar o foco para os casos com maior potencial de avanço.

A aplicação permite a análise de duas formas distintas:
1.  **API REST**: Com endpoints separados para previsões baseadas em **regras de negócio** e em um **modelo de Machine Learning**.
2.  **Interface Web (UI)**: Uma aplicação interativa construída com Streamlit que permite ao usuário inserir os dados da ocorrência e obter a previsão de forma visual.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**: Para a construção da API.
- **Streamlit**: Para a criação da interface web.
- **Pydantic V2**: Para validação de dados.
- **Uvicorn**: Como servidor ASGI para a API.
- **Pytest**: Para a execução dos testes automatizados.
- **Scikit-learn & Joblib**: Para o treinamento e uso do modelo de ML.
- **Pandas**: Para manipulação de dados.

## 📂 Estrutura do Projeto

```
.
├── src/
│   ├── app.py                 # Aplicação principal da interface web (Streamlit)
│   ├── api/
│   │   ├── main_regras.py     # Endpoint da API (baseado em regras)
│   │   ├── main_modelo.py     # Endpoint da API (baseado em ML)
│   │   └── gerar_modelo.py    # Script para treinar o modelo de ML
│   ├── models/
│   │   └── schemas.py         # Modelos de dados Pydantic
│   └── pages/
│       ├── previsao_com_regras.py # Página da UI para previsão com regras
│       └── previsao_com_modelo.py # Página da UI para previsão com modelo
├── tests/
│   └── test_main.py           # Testes para a API
├── requirements.txt           # Dependências do projeto
└── README.md
```

## 🚀 Como Executar

### 1. Instalar Dependências

Certifique-se de que você está na pasta raiz do projeto e execute:
```bash
pip install -r requirements.txt
```

### 2. Rodando os Serviços Individualmente

Você pode iniciar cada serviço separadamente, o que é útil para focar em uma parte específica da aplicação.

**Para a Interface Web (Streamlit):**
```bash
streamlit run src/app.py
```
Acesse a interface em [http://localhost:8501](http://localhost:8501).

**Para a API de Regras:**
```bash
uvicorn src.api.main_regras:app --reload --port 8001
```
Acesse a documentação em [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).

**Para a API de Modelo ML:**
```bash
uvicorn src.api.main_modelo:app --reload --port 8002
```
Acesse a documentação em [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs).


### 3. Rodando o Ambiente Completo (Desenvolvimento)

Para ter a experiência completa da aplicação, com a interface web se comunicando com as APIs, você precisará rodar todos os serviços ao mesmo tempo. A forma mais simples de fazer isso é usando múltiplos terminais.

Abra três terminais separados na pasta raiz do projeto e execute um comando em cada um:

**Terminal 1 (Interface Web):**
```bash
streamlit run src/app.py
```

**Terminal 2 (API de Regras):**
```bash
uvicorn src.api.main_regras:app --reload --port 8001
```

**Terminal 3 (API de Modelo ML):**
```bash
uvicorn src.api.main_modelo:app --reload --port 8002
```

## ✅ Testes

Para garantir a qualidade e o funcionamento correto do código, execute os testes automatizados com o Pytest:

```bash
pytest
```

## 🤖 Treinamento do Modelo

Se desejar treinar uma nova versão do modelo de Machine Learning, execute o seguinte script a partir da pasta raiz:

```bash
python src/api/gerar_modelo.py
```

Isso irá gerar um novo arquivo `resolutividade_model.pkl` na raiz do projeto, que é utilizado pela API de Machine Learning e pela interface web.