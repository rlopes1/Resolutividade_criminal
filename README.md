# API de Análise de Resolutividade Criminal

## 🎯 Objetivo

Esta API tem como objetivo prever o potencial de resolução (resolutividade) de uma ocorrência criminal com base em informações iniciais. A análise classifica a ocorrência em **Alta**, **Média** ou **Baixa** resolutividade, fornecendo um indicativo da probabilidade de sucesso na investigação.

A aplicação utiliza uma abordagem baseada em regras, mas também inclui um script para treinar um modelo de Machine Learning (Regressão Logística) que pode ser integrado futuramente para previsões mais robustas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**: Para a construção da API.
- **Pydantic**: Para validação de dados.
- **Scikit-learn**: Para o treinamento do modelo de Machine Learning.
- **Joblib**: Para salvar e carregar o modelo treinado.
- **Uvicorn**: Como servidor ASGI para a API.

## 📂 Estrutura do Projeto

```
template/
├── src/
│   ├── api/
│   │   └── main.py          # Endpoints da API
│   ├── models/
│   │   └── schemas.py       # Modelos Pydantic
│   └── config.py            # Configurações
├── tests/
│   └── test_template.py     # Testes automatizados
├── requirements.txt
└── .gitignore
```

## Como Usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar a API

```bash
uvicorn src.api.main:app --reload
```

### 3. Acessar documentação

http://localhost:8000/docs

### 4. Rodar testes

```bash
pytest tests/ -v
```

## 🔧 Customização

### Passo 1: Adapte os Schemas

Edite `src/models/schemas.py` com seus modelos de dados.

### Passo 2: Implemente sua Lógica

Edite `src/api/main.py` e substitua a lógica do endpoint `/calcular`.

### Passo 3: Crie Testes

Edite `tests/test_template.py` para testar sua lógica.

## Exemplo Atual

API de soma simples:
- **POST /calcular**: Soma dois números

Substitua isso pela sua lógica de negócio!
