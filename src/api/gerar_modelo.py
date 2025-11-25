import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import warnings

# Ignorar warnings de convergência do modelo, comum em exemplos simples
warnings.filterwarnings('ignore')

# Mapeamento para as classes de resolutividade
RESOLUTIVIDADE_CLASSES = {
    0: "Baixa",
    1: "Média",
    2: "Alta"
}
FEATURES = [
    'periodo_decorrido_dias', 'suspeito_conhecido', 'tem_testemunhas',
    'tem_imagens_cameras', 'suspeito_rastreavel', 'vestigios_preservados'
]
TARGET = 'resolutividade'
MODEL_FILENAME = "resolutividade_model.pkl"

def gerar_dados(data_size=3500):
    """Gera um DataFrame de dados sintéticos para o treinamento do modelo."""
    print("Iniciando a simulação de treinamento do modelo ...")

    np.random.seed(42)  

    # Gerar dados base
    data = pd.DataFrame({
        'periodo_decorrido_dias': np.random.randint(1, 60, data_size), # 1 a 60 dias
        'suspeito_conhecido': np.random.choice([0, 1], data_size, p=[0.7, 0.3]),
        'tem_testemunhas': np.random.choice([0, 1], data_size, p=[0.65, 0.35]),
        'tem_imagens_cameras': np.random.choice([0, 1], data_size, p=[0.75, 0.25]),
        'suspeito_rastreavel': np.random.choice([0, 1], data_size, p=[0.7, 0.3]),
        'vestigios_preservados': np.random.choice([0, 1], data_size, p=[0.6, 0.4]),
        # Variável Alvo inicial: 0=Baixa, 1=Média, 2=Alta
        TARGET: np.random.choice(list(RESOLUTIVIDADE_CLASSES.keys()), data_size, p=[0.4, 0.35, 0.25])
    })

    # Lógica para introduzir correlação entre features e o alvo
    evidencias_suficientes = (
        data['tem_testemunhas'] + data['tem_imagens_cameras'] + data['vestigios_preservados']
    )
    cond_alta = (
        (data['periodo_decorrido_dias'] <= 5) &
        (
            ((data['suspeito_conhecido'] == 1) & (evidencias_suficientes >= 1)) |
            ((data['suspeito_rastreavel'] == 1) & (evidencias_suficientes >= 2))
        )
    )
    cond_media = (
        (
            (data['periodo_decorrido_dias'] < 30) &
            ((data['suspeito_conhecido'] == 1) | ((data['suspeito_rastreavel'] == 1) & (evidencias_suficientes >= 1)))
        ) |
        ((evidencias_suficientes >= 3) & (data['periodo_decorrido_dias'] < 60))
    )
    
    # Aplica as regras para ajustar a variável alvo, da mais específica para a menos
    data.loc[cond_alta, TARGET] = 2
    data.loc[cond_media & ~cond_alta, TARGET] = 1
    
    return data

def treinar_avaliar_modelo(data):
    """Treina, avalia e salva o modelo de classificação."""
    print("Iniciando o treinamento do modelo...")

    X = data[FEATURES]
    y = data[TARGET]

    # Dividir os dados em treinamento e teste, mantendo a proporção das classes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Definição do Modelo RandomForestClassifier
    # 'class_weight' é crucial para dados desbalanceados.
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1 # Usa todos os processadores disponíveis
    )

    # Treinamento
    model.fit(X_train, y_train)
    print("Treinamento concluído.")

    # Avaliação
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n--- Avaliação do Modelo ---")
    print(f"Acurácia no conjunto de teste: {accuracy:.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(
        y_test, y_pred, target_names=list(RESOLUTIVIDADE_CLASSES.values())
    ))

    # Salvar o modelo treinado usando joblib
    with open(MODEL_FILENAME, "wb") as f:
        joblib.dump(model, f)
    print(f"\nModelo salvo em '{MODEL_FILENAME}'")
    
    return model

def prever_novo_caso(model):
    """Demonstra a previsão de um novo caso com o modelo treinado."""
    # Cenário otimista para teste
    novo_incidente = pd.DataFrame([{
        'periodo_decorrido_dias': 1, 
        'suspeito_conhecido': 1, 
        'tem_testemunhas': 1, 
        'tem_imagens_cameras': 0,
        'suspeito_rastreavel': 1,
        'vestigios_preservados': 1
    }], columns=FEATURES)

    # Previsão de classe e probabilidades
    previsao_classe = model.predict(novo_incidente)[0]
    previsao_proba = model.predict_proba(novo_incidente)[0]
    status = RESOLUTIVIDADE_CLASSES.get(previsao_classe, "Desconhecido")

    print("\n--- Exemplo de Previsão de Novo Incidente ---")
    print(f"Dados do Incidente: {novo_incidente.to_dict(orient='records')[0]}")
    print(f"Classe Prevista: {status}")
    print("\nProbabilidades por Classe:")
    for i, prob in enumerate(previsao_proba):
        print(f"  {RESOLUTIVIDADE_CLASSES[i]}: {prob * 100:.2f}%")

if __name__ == "__main__":
    # 1. Gerar dados
    dados_ocorrencias = gerar_dados()
    
    # 2. Treinar, avaliar e salvar o modelo
    modelo_treinado = treinar_avaliar_modelo(dados_ocorrencias)
    
    # 3. Demonstrar uma previsão
    prever_novo_caso(modelo_treinado)