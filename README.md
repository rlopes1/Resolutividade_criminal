# API de Análise de Resolutividade Criminal

## 🎯 Objetivo

Esta API tem como objetivo prever o potencial de resolução (resolutividade) de uma ocorrência criminal com base em informações iniciais. A análise classifica a ocorrência em **Alta**, **Média** ou **Baixa** resolutividade, fornecendo um indicativo da probabilidade de sucesso na investigação.

Atualmente, a API utiliza um conjunto de **regras de negócio** para fazer a classificação. O projeto também inclui um script para treinar um modelo de Machine Learning (`RandomForestClassifier`) que pode ser integrado futuramente para previsões mais robustas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**: Para a construção da API.
- **Pydantic V2**: Para validação de dados.
- **Uvicorn**: Como servidor ASGI para a API.
- **Pytest**: Para a execução dos testes automatizados.
- **Scikit-learn & Joblib**: Utilizados apenas no script de treinamento do modelo de ML.

## 📂 Estrutura do Projeto

```
.
├── src/
│   ├── api/
│   │   ├── main.py            # Lógica e endpoints da API (baseada em regras)
│   │   └── gerar_modelo.py    # Script para treinar o modelo de ML
│   └── models/
│       └── schemas.py         # Modelos de dados Pydantic
├── tests/
│   ├── test_main.py         # Testes para a API
│   └── test_modelo.py       # Testes para o script de treinamento
├── requirements.txt         # Dependências do projeto
└── README.md
```

## 🚀 Como Executar

### 1. Instalar Dependências

Certifique-se de que você está na pasta raiz do projeto e execute:
```bash
pip install -r requirements.txt
```

### 2. Rodar a API

Para iniciar o servidor da API em modo de desenvolvimento (com recarregamento automático):
```bash
uvicorn src.api.main:app --reload
```

### 3. Acessar a Documentação Interativa

Com o servidor rodando, acesse a documentação gerada automaticamente pelo FastAPI para interagir com os endpoints:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## ✅ Testes

Para garantir a qualidade e o funcionamento correto do código, execute os testes automatizados com o Pytest:

```bash
pytest
```

## 🤖 Treinamento do Modelo (Opcional)

Se desejar treinar uma nova versão do modelo de Machine Learning, execute o seguinte script a partir da pasta raiz:

```bash
python src/api/gerar_modelo.py
```

Isso irá gerar um novo arquivo `resolutividade_model.pkl` na raiz do projeto. Para que a API utilize este modelo, a lógica em `src/api/main.py` precisaria ser adaptada para carregá-lo e usá-lo nas previsões, em vez das regras de negócio atuais.